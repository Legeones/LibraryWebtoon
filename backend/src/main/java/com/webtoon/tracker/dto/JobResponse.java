package com.webtoon.tracker.dto;

import com.webtoon.tracker.model.Job;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class JobResponse {
    private String id;
    private Job.JobStatus status;
    private String originalImagePath;
    private String debugBoxesImagePath;
    private String maskImagePath;
    private String cleanImagePath;
    private String finalImagePath;
    private String resultJson;
    private Double processingTime;
    private String errorMessage;
    private LocalDateTime createdAt;
    private LocalDateTime completedAt;
    private Integer version;
}
