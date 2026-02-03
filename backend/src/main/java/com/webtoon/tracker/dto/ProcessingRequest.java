package com.webtoon.tracker.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProcessingRequest {
    private String sourceLanguage = "ja";
    private String targetLanguage = "en";
    private String ocrEngine = "paddleocr";
    private String translationEngine = "mock";
    private String inpaintMethod = "telea";
}
