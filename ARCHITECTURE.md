# Architecture Documentation

## Overview

LibraryWebtoon is a three-tier application for automated webtoon panel translation with manual editing capabilities.

## System Architecture

```
┌─────────────────┐
│   Next.js       │
│   Frontend      │
│   (Port 3000)   │
└────────┬────────┘
         │
         │ HTTP/REST
         ▼
┌─────────────────┐
│  Spring Boot    │
│   Backend       │
│   (Port 8080)   │
└────────┬────────┘
         │
         │ HTTP/REST
         ▼
┌─────────────────┐
│   FastAPI       │
│ Python Service  │
│   (Port 8001)   │
└─────────────────┘
```

## Components

### 1. Frontend (Next.js)

**Location**: `frontend/`

**Technology Stack**:
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Zustand (state management)
- Axios (HTTP client)

**Key Features**:
- Image upload with drag-and-drop
- Job status monitoring with polling
- Multi-view image viewer (original, debug, mask, clean, final)
- Region editor for manual corrections
- Real-time preview of processing stages

**Components**:
- `ImageUpload.tsx` - File upload interface
- `JobStatus.tsx` - Job progress and status display
- `ImageViewer.tsx` - Multi-tab image viewer
- `RegionEditor.tsx` - Text region editing interface

### 2. Backend (Spring Boot)

**Location**: `backend/`

**Technology Stack**:
- Spring Boot 3.2
- Spring Data JPA
- Spring Security
- H2 Database (development)
- PostgreSQL support (production)
- Swagger/OpenAPI

**Key Features**:
- RESTful API for job management
- Authentication and authorization
- Job orchestration
- Image storage and serving
- Python service integration

**Main Components**:
- **Models**: `Job`, `User`
- **Repositories**: `JobRepository`, `UserRepository`
- **Services**: `JobService`
- **Controllers**: `JobController`
- **Client**: `PythonServiceClient`

**API Endpoints**:
- `POST /api/jobs` - Create and process new job
- `GET /api/jobs/{id}` - Get job by ID
- `GET /api/jobs/user/{userId}` - Get user's jobs
- `GET /api/jobs/{id}/image/{type}` - Get job image

### 3. Processing Service (Python FastAPI)

**Location**: `python-service/`

**Technology Stack**:
- FastAPI
- OpenCV
- Tesseract OCR
- Pillow (PIL)
- NumPy

**Key Features**:
- Text detection using OpenCV
- OCR with Tesseract
- Translation (mock/DeepL/Google)
- Image inpainting
- Text rendering (typesetting)

**Processing Pipeline**:

1. **Text Detection** (`text_detection.py`)
   - Uses OpenCV contour detection
   - Filters by size and aspect ratio
   - Returns bounding boxes with confidence

2. **OCR** (`ocr.py`)
   - Tesseract-based text extraction
   - Language support (Japanese, English, etc.)
   - Confidence scoring

3. **Translation** (`translation.py`)
   - Mock translation (development)
   - DeepL API support (future)
   - Google Translate support (future)

4. **Inpainting** (`inpainting.py`)
   - Creates binary mask of text regions
   - OpenCV inpainting (TELEA or NS)
   - Removes original text

5. **Typesetting** (`typesetting.py`)
   - PIL-based text rendering
   - Text wrapping and alignment
   - Stroke and color support
   - Font customization

**API Endpoints**:
- `POST /api/v1/process` - Process image through full pipeline
- `POST /api/v1/rerender` - Re-render with modified regions
- `GET /api/v1/result/{job_id}` - Get processing result
- `GET /api/v1/image/{job_id}/{type}` - Get generated image
- `GET /health` - Health check

## Data Flow

### Complete Processing Flow

```
1. User uploads image
   └─> Next.js Frontend

2. Frontend sends to backend
   └─> POST /api/jobs
   └─> Spring Boot Backend

3. Backend creates job record
   └─> Saves to database
   └─> Status: QUEUED

4. Backend calls Python service
   └─> POST /api/v1/process
   └─> Sends image + options

5. Python service processes
   ├─> Text Detection
   ├─> OCR
   ├─> Translation
   ├─> Inpainting
   └─> Typesetting

6. Python returns results
   └─> JSON + image paths
   └─> Spring Boot Backend

7. Backend updates job
   └─> Status: DONE
   └─> Stores result JSON

8. Frontend polls for updates
   └─> GET /api/jobs/{id}
   └─> Displays results
```

### Manual Editing Flow

```
1. User edits region in UI
   └─> Modifies OCR text, translation, or style

2. User clicks "Re-render"
   └─> Frontend sends updated regions

3. Backend receives update
   └─> Creates new job version

4. Backend calls Python re-render
   └─> POST /api/v1/rerender
   └─> Only performs typesetting

5. Python renders new image
   └─> Uses existing clean image
   └─> Applies updated regions

6. Results returned to user
   └─> New final image available
```

## Database Schema

### Job Table

```sql
CREATE TABLE jobs (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    status VARCHAR(20) NOT NULL,
    original_image_path VARCHAR(500),
    debug_boxes_image_path VARCHAR(500),
    mask_image_path VARCHAR(500),
    clean_image_path VARCHAR(500),
    final_image_path VARCHAR(500),
    result_json TEXT,
    source_language VARCHAR(10),
    target_language VARCHAR(10),
    ocr_engine VARCHAR(50),
    translation_engine VARCHAR(50),
    inpaint_method VARCHAR(50),
    processing_time DOUBLE,
    error_message TEXT,
    created_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    version INTEGER DEFAULT 1
);
```

### User Table

```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    enabled BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    last_login TIMESTAMP
);
```

## Result JSON Schema

```json
{
  "job_id": "uuid",
  "status": "DONE",
  "regions": [
    {
      "id": "region_0",
      "bbox": {
        "x": 100,
        "y": 50,
        "width": 200,
        "height": 80
      },
      "confidence": 0.95,
      "orientation": 0.0,
      "ocr_text": "こんにちは",
      "ocr_confidence": 0.92,
      "translated_text": "Hello",
      "font_size": 24,
      "font_family": "Arial",
      "alignment": "center",
      "stroke_width": 2,
      "stroke_color": "#000000",
      "text_color": "#FFFFFF"
    }
  ],
  "original_image_path": "/tmp/webtoon-processing/uuid/original.png",
  "debug_boxes_image_path": "/tmp/webtoon-processing/uuid/debug_boxes.png",
  "mask_image_path": "/tmp/webtoon-processing/uuid/mask.png",
  "clean_image_path": "/tmp/webtoon-processing/uuid/clean.png",
  "final_image_path": "/tmp/webtoon-processing/uuid/final.png",
  "processing_time": 3.45,
  "metadata": {}
}
```

## Configuration

### Environment Variables

**Python Service** (`.env`):
```
STORAGE_PATH=/tmp/webtoon-processing
UPLOAD_PATH=/tmp/webtoon-uploads
DEEPL_API_KEY=your_api_key
GOOGLE_TRANSLATE_API_KEY=your_api_key
TESSERACT_CMD=/usr/bin/tesseract
```

**Spring Boot** (`application.properties`):
```
spring.datasource.url=jdbc:h2:file:./data/webtoon-tracker
python.service.url=http://localhost:8001
spring.servlet.multipart.max-file-size=50MB
```

**Next.js** (`.env.local`):
```
NEXT_PUBLIC_API_URL=http://localhost:8080
```

## Deployment

### Local Development

1. **Python Service**:
   ```bash
   cd python-service
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8001
   ```

2. **Spring Boot**:
   ```bash
   cd backend
   ./mvnw spring-boot:run
   ```

3. **Next.js**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Docker Deployment

```bash
docker-compose up
```

## Security Considerations

1. **Authentication**: Basic security configured, should be enhanced for production
2. **CORS**: Currently allows localhost, configure for production domains
3. **File Upload**: Size limits configured (50MB)
4. **API Keys**: Store securely in environment variables
5. **HTTPS**: Should be used in production

## Future Enhancements

1. **Advanced Translation**:
   - DeepL API integration
   - LLM-based translation with context
   - Text fitting optimization

2. **Advanced Vision**:
   - Better text detection (deep learning models)
   - EasyOCR integration
   - Advanced inpainting (LaMa model)

3. **Features**:
   - Batch processing
   - Webtoon tracking system
   - User authentication
   - Version history
   - Collaborative editing

4. **Performance**:
   - Async processing with message queue
   - Caching
   - CDN for images
   - Database optimization

5. **UI/UX**:
   - Drag-and-drop region editing
   - Live preview
   - Keyboard shortcuts
   - Mobile support
