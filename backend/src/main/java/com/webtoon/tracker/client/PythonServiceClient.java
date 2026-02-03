package com.webtoon.tracker.client;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.entity.mime.MultipartEntityBuilder;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ContentType;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.IOException;

@Component
public class PythonServiceClient {
    
    @Value("${python.service.url:http://localhost:8001}")
    private String pythonServiceUrl;
    
    private final ObjectMapper objectMapper = new ObjectMapper();
    
    public JsonNode processImage(File imageFile, String jobId, 
                                 String sourceLanguage, String targetLanguage,
                                 String ocrEngine, String translationEngine,
                                 String inpaintMethod) throws IOException {
        
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpPost uploadFile = new HttpPost(pythonServiceUrl + "/api/v1/process");
            
            MultipartEntityBuilder builder = MultipartEntityBuilder.create();
            builder.addBinaryBody(
                "file",
                imageFile,
                ContentType.IMAGE_PNG,
                imageFile.getName()
            );
            builder.addTextBody("job_id", jobId);
            builder.addTextBody("source_language", sourceLanguage);
            builder.addTextBody("target_language", targetLanguage);
            builder.addTextBody("ocr_engine", ocrEngine);
            builder.addTextBody("translation_engine", translationEngine);
            builder.addTextBody("inpaint_method", inpaintMethod);
            
            uploadFile.setEntity(builder.build());
            
            try (CloseableHttpResponse response = httpClient.execute(uploadFile)) {
                String responseString = EntityUtils.toString(response.getEntity());
                return objectMapper.readTree(responseString);
            }
        }
    }
    
    public boolean healthCheck() {
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpPost request = new HttpPost(pythonServiceUrl + "/health");
            try (CloseableHttpResponse response = httpClient.execute(request)) {
                return response.getCode() == 200;
            }
        } catch (IOException e) {
            return false;
        }
    }
}
