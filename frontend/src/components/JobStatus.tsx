import React, { useState, useEffect } from 'react';
import { Job } from '@/types';
import { jobApi } from '@/lib/api';

interface JobStatusProps {
  job: Job;
  onUpdate: (job: Job) => void;
}

export default function JobStatus({ job, onUpdate }: JobStatusProps) {
  const [polling, setPolling] = useState(true);

  useEffect(() => {
    if (job.status === 'DONE' || job.status === 'FAILED') {
      setPolling(false);
      return;
    }

    const interval = setInterval(async () => {
      try {
        const updatedJob = await jobApi.getJob(job.id);
        onUpdate(updatedJob);
        
        if (updatedJob.status === 'DONE' || updatedJob.status === 'FAILED') {
          setPolling(false);
        }
      } catch (error) {
        console.error('Failed to poll job status:', error);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [job.id, job.status, onUpdate]);

  const getStatusColor = () => {
    switch (job.status) {
      case 'QUEUED':
        return 'bg-yellow-100 text-yellow-800';
      case 'PROCESSING':
        return 'bg-blue-100 text-blue-800';
      case 'DONE':
        return 'bg-green-100 text-green-800';
      case 'FAILED':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Job Status</h2>
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor()}`}>
          {job.status}
        </span>
      </div>

      <div className="space-y-3">
        <div>
          <p className="text-sm text-gray-600">Job ID</p>
          <p className="font-mono text-sm">{job.id}</p>
        </div>

        {job.processingTime && (
          <div>
            <p className="text-sm text-gray-600">Processing Time</p>
            <p className="font-medium">{job.processingTime.toFixed(2)}s</p>
          </div>
        )}

        {job.errorMessage && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-700">{job.errorMessage}</p>
          </div>
        )}

        {polling && (
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <div className="animate-spin h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full"></div>
            <span>Checking for updates...</span>
          </div>
        )}
      </div>
    </div>
  );
}
