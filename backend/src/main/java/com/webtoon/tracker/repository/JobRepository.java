package com.webtoon.tracker.repository;

import com.webtoon.tracker.model.Job;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface JobRepository extends JpaRepository<Job, String> {
    
    List<Job> findByUserIdOrderByCreatedAtDesc(String userId);
    
    List<Job> findByStatus(Job.JobStatus status);
    
    List<Job> findByUserIdAndStatus(String userId, Job.JobStatus status);
}
