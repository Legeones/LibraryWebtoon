package com.webtoon.tracker.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.webtoon.tracker.client.PythonServiceClient;
import com.webtoon.tracker.dto.JobResponse;
import com.webtoon.tracker.dto.ProcessingRequest;
import com.webtoon.tracker.model.Job;
import com.webtoon.tracker.repository.JobRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class JobService {
    
    private final JobRepository jobRepository;
    private final PythonServiceClient pythonClient;
    private final ObjectMapper objectMapper = new ObjectMapper();
    
    private static final String UPLOAD_DIR = "uploads";
    
    @Transactional
    public JobResponse createAndProcessJob(String userId, MultipartFile file, 
                                          ProcessingRequest request) throws IOException {
        // Create job
        Job job = new Job();
        job.setId(UUID.randomUUID().toString());
        job.setUserId(userId);
        job.setStatus(Job.JobStatus.QUEUED);
        job.setSourceLanguage(request.getSourceLanguage());
        job.setTargetLanguage(request.getTargetLanguage());
        job.setOcrEngine(request.getOcrEngine());
        job.setTranslationEngine(request.getTranslationEngine());
        job.setInpaintMethod(request.getInpaintMethod());
        
        job = jobRepository.save(job);
        
        // Save uploaded file
        Path uploadPath = Paths.get(UPLOAD_DIR);
        Files.createDirectories(uploadPath);
        
        String filename = job.getId() + "_original.png";
        Path filePath = uploadPath.resolve(filename);
        file.transferTo(filePath.toFile());
        
        job.setOriginalImagePath(filePath.toString());
        job = jobRepository.save(job);
        
        // Process asynchronously
        processJobAsync(job, filePath.toFile());
        
        return toJobResponse(job);
    }
    
    private void processJobAsync(Job job, File imageFile) {
        // In production, use @Async or a message queue
        new Thread(() -> {
            try {
                job.setStatus(Job.JobStatus.PROCESSING);
                jobRepository.save(job);
                
                JsonNode result = pythonClient.processImage(
                    imageFile,
                    job.getId(),
                    job.getSourceLanguage(),
                    job.getTargetLanguage(),
                    job.getOcrEngine(),
                    job.getTranslationEngine(),
                    job.getInpaintMethod()
                );
                
                // Update job with results
                job.setStatus(Job.JobStatus.valueOf(result.get("status").asText()));
                job.setResultJson(objectMapper.writeValueAsString(result));
                
                if (result.has("original_image_path")) {
                    job.setOriginalImagePath(result.get("original_image_path").asText());
                }
                if (result.has("debug_boxes_image_path")) {
                    job.setDebugBoxesImagePath(result.get("debug_boxes_image_path").asText());
                }
                if (result.has("mask_image_path")) {
                    job.setMaskImagePath(result.get("mask_image_path").asText());
                }
                if (result.has("clean_image_path")) {
                    job.setCleanImagePath(result.get("clean_image_path").asText());
                }
                if (result.has("final_image_path")) {
                    job.setFinalImagePath(result.get("final_image_path").asText());
                }
                if (result.has("processing_time")) {
                    job.setProcessingTime(result.get("processing_time").asDouble());
                }
                
                job.setCompletedAt(LocalDateTime.now());
                jobRepository.save(job);
                
            } catch (Exception e) {
                job.setStatus(Job.JobStatus.FAILED);
                job.setErrorMessage(e.getMessage());
                job.setCompletedAt(LocalDateTime.now());
                jobRepository.save(job);
            }
        }).start();
    }
    
    public Optional<JobResponse> getJob(String jobId) {
        return jobRepository.findById(jobId).map(this::toJobResponse);
    }
    
    public List<JobResponse> getUserJobs(String userId) {
        return jobRepository.findByUserIdOrderByCreatedAtDesc(userId)
            .stream()
            .map(this::toJobResponse)
            .collect(Collectors.toList());
    }
    
    public List<JobResponse> getJobsByStatus(Job.JobStatus status) {
        return jobRepository.findByStatus(status)
            .stream()
            .map(this::toJobResponse)
            .collect(Collectors.toList());
    }
    
    private JobResponse toJobResponse(Job job) {
        JobResponse response = new JobResponse();
        response.setId(job.getId());
        response.setStatus(job.getStatus());
        response.setOriginalImagePath(job.getOriginalImagePath());
        response.setDebugBoxesImagePath(job.getDebugBoxesImagePath());
        response.setMaskImagePath(job.getMaskImagePath());
        response.setCleanImagePath(job.getCleanImagePath());
        response.setFinalImagePath(job.getFinalImagePath());
        response.setResultJson(job.getResultJson());
        response.setProcessingTime(job.getProcessingTime());
        response.setErrorMessage(job.getErrorMessage());
        response.setCreatedAt(job.getCreatedAt());
        response.setCompletedAt(job.getCompletedAt());
        response.setVersion(job.getVersion());
        return response;
    }
}
