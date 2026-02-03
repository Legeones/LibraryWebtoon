package com.webtoon.tracker.controller;

import com.webtoon.tracker.dto.JobResponse;
import com.webtoon.tracker.dto.ProcessingRequest;
import com.webtoon.tracker.model.Job;
import com.webtoon.tracker.service.JobService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api/jobs")
@RequiredArgsConstructor
@Tag(name = "Jobs", description = "Job management API")
public class JobController {
    
    private final JobService jobService;
    
    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @Operation(summary = "Create and process a new job")
    public ResponseEntity<JobResponse> createJob(
            @RequestParam("file") MultipartFile file,
            @RequestParam(defaultValue = "default-user") String userId,
            @RequestParam(defaultValue = "ja") String sourceLanguage,
            @RequestParam(defaultValue = "en") String targetLanguage,
            @RequestParam(defaultValue = "paddleocr") String ocrEngine,
            @RequestParam(defaultValue = "mock") String translationEngine,
            @RequestParam(defaultValue = "telea") String inpaintMethod
    ) {
        try {
            ProcessingRequest request = new ProcessingRequest(
                sourceLanguage, targetLanguage, ocrEngine, 
                translationEngine, inpaintMethod
            );
            
            JobResponse job = jobService.createAndProcessJob(userId, file, request);
            return ResponseEntity.status(HttpStatus.CREATED).body(job);
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    @GetMapping("/{jobId}")
    @Operation(summary = "Get job by ID")
    public ResponseEntity<JobResponse> getJob(@PathVariable String jobId) {
        return jobService.getJob(jobId)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
    
    @GetMapping("/user/{userId}")
    @Operation(summary = "Get all jobs for a user")
    public ResponseEntity<List<JobResponse>> getUserJobs(@PathVariable String userId) {
        return ResponseEntity.ok(jobService.getUserJobs(userId));
    }
    
    @GetMapping("/status/{status}")
    @Operation(summary = "Get jobs by status")
    public ResponseEntity<List<JobResponse>> getJobsByStatus(@PathVariable Job.JobStatus status) {
        return ResponseEntity.ok(jobService.getJobsByStatus(status));
    }
    
    @GetMapping("/{jobId}/image/{type}")
    @Operation(summary = "Get job image")
    public ResponseEntity<Resource> getJobImage(
            @PathVariable String jobId,
            @PathVariable String type
    ) {
        return jobService.getJob(jobId)
            .map(job -> {
                String imagePath = switch (type) {
                    case "original" -> job.getOriginalImagePath();
                    case "debug" -> job.getDebugBoxesImagePath();
                    case "mask" -> job.getMaskImagePath();
                    case "clean" -> job.getCleanImagePath();
                    case "final" -> job.getFinalImagePath();
                    default -> null;
                };
                
                if (imagePath != null && new File(imagePath).exists()) {
                    Resource resource = new FileSystemResource(imagePath);
                    return ResponseEntity.ok()
                        .contentType(MediaType.IMAGE_PNG)
                        .body(resource);
                }
                return ResponseEntity.<Resource>notFound().build();
            })
            .orElse(ResponseEntity.notFound().build());
    }
}
