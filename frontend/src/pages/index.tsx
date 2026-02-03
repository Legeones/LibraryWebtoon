import React, { useState } from 'react';
import Head from 'next/head';
import ImageUpload from '@/components/ImageUpload';
import JobStatus from '@/components/JobStatus';
import ImageViewer from '@/components/ImageViewer';
import RegionEditor from '@/components/RegionEditor';
import { Job } from '@/types';

export default function Home() {
  const [currentJob, setCurrentJob] = useState<Job | null>(null);

  return (
    <>
      <Head>
        <title>Webtoon Panel Translator</title>
        <meta name="description" content="Automated webtoon panel translation with manual editing" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <main className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Webtoon Panel Translator
            </h1>
            <p className="text-gray-600">
              Upload a panel image to automatically detect, translate, and clean text
            </p>
          </div>

          {/* Upload Section */}
          {!currentJob && (
            <div className="max-w-2xl mx-auto">
              <ImageUpload onJobCreated={setCurrentJob} />
            </div>
          )}

          {/* Processing and Results */}
          {currentJob && (
            <div className="space-y-6">
              {/* Action Bar */}
              <div className="flex justify-between items-center">
                <button
                  onClick={() => setCurrentJob(null)}
                  className="px-4 py-2 text-gray-600 hover:text-gray-900 transition-colors"
                >
                  ← Upload New Image
                </button>
                {currentJob.status === 'DONE' && currentJob.finalImagePath && (
                  <a
                    href={`http://localhost:8080/api/jobs/${currentJob.id}/image/final`}
                    download={`panel_${currentJob.id}.png`}
                    className="px-6 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition-colors"
                  >
                    Download Final Image
                  </a>
                )}
              </div>

              {/* Job Status */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-1">
                  <JobStatus job={currentJob} onUpdate={setCurrentJob} />
                </div>

                {/* Image Viewer */}
                <div className="lg:col-span-2">
                  <ImageViewer job={currentJob} />
                </div>
              </div>

              {/* Region Editor */}
              {currentJob.status === 'DONE' && currentJob.resultJson && (
                <div>
                  <RegionEditor job={currentJob} />
                </div>
              )}

              {/* Processing Info */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <h3 className="font-semibold text-blue-900 mb-2">Processing Pipeline</h3>
                <ol className="list-decimal list-inside space-y-1 text-sm text-blue-800">
                  <li>Text Detection - Locate text regions in the panel</li>
                  <li>OCR - Extract original text from each region</li>
                  <li>Translation - Translate text to target language</li>
                  <li>Inpainting - Remove original text from image</li>
                  <li>Typesetting - Render translated text with styling</li>
                </ol>
              </div>
            </div>
          )}

          {/* Features Section */}
          {!currentJob && (
            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="text-blue-500 mb-3">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="font-semibold text-lg mb-2">Automated Processing</h3>
                <p className="text-gray-600 text-sm">
                  Automatically detect text, perform OCR, translate, clean, and render new text
                </p>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="text-green-500 mb-3">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </div>
                <h3 className="font-semibold text-lg mb-2">Manual Editing</h3>
                <p className="text-gray-600 text-sm">
                  Correct OCR errors, adjust translations, and customize text styling
                </p>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="text-purple-500 mb-3">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <h3 className="font-semibold text-lg mb-2">High Quality Output</h3>
                <p className="text-gray-600 text-sm">
                  Export professional-quality translated panels with clean backgrounds
                </p>
              </div>
            </div>
          )}
        </div>
      </main>
    </>
  );
}
