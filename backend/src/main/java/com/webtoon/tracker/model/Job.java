package com.webtoon.tracker.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "jobs")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Job {
    
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private String id;
    
    @Column(nullable = false)
    private String userId;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private JobStatus status = JobStatus.QUEUED;
    
    @Column(length = 500)
    private String originalImagePath;
    
    @Column(length = 500)
    private String debugBoxesImagePath;
    
    @Column(length = 500)
    private String maskImagePath;
    
    @Column(length = 500)
    private String cleanImagePath;
    
    @Column(length = 500)
    private String finalImagePath;
    
    @Column(columnDefinition = "TEXT")
    private String resultJson;
    
    @Column
    private String sourceLanguage = "ja";
    
    @Column
    private String targetLanguage = "en";
    
    @Column
    private String ocrEngine = "paddleocr";
    
    @Column
    private String translationEngine = "mock";
    
    @Column
    private String inpaintMethod = "telea";
    
    @Column
    private Double processingTime;
    
    @Column(columnDefinition = "TEXT")
    private String errorMessage;
    
    @Column(nullable = false)
    private LocalDateTime createdAt = LocalDateTime.now();
    
    @Column
    private LocalDateTime completedAt;
    
    @Column
    private Integer version = 1;
    
    public enum JobStatus {
        QUEUED,
        PROCESSING,
        DONE,
        FAILED
    }
}
