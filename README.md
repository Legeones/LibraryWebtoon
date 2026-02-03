# LibraryWebtoon

A comprehensive webtoon panel translation application with OCR, translation, and manual editing capabilities.

## Architecture

This project follows a three-tier architecture:

### 1. Frontend (Next.js)
- User interface for image upload and editing
- Preview of processing stages (original, boxes, mask, clean, final)
- Interactive panel editor with overlays
- Text and translation editing
- Zone manipulation (drag/resize)
- Typographic controls
- Export functionality

**Location**: `frontend/`

### 2. Backend (Java Spring Boot)
- Application core and API gateway
- Authentication and authorization
- Job management and tracking
- Image storage
- Orchestration between frontend and Python service
- Webtoon tracking features

**Location**: `backend/`

### 3. Processing Service (Python FastAPI)
- Text detection in panels
- OCR (Optical Character Recognition)
- Translation
- Image inpainting (text removal)
- Typesetting (text rendering)
- Complete processing pipeline

**Location**: `python-service/`

## Workflow

1. **Upload**: User uploads a panel image via Next.js frontend
2. **Job Creation**: Spring Boot creates a job and sends it to Python service
3. **Processing**: Python service performs:
   - Text detection
   - OCR
   - Translation
   - Image cleaning (inpainting)
   - Text rendering (typesetting)
4. **Results**: JSON results + intermediate images sent back to Spring
5. **Manual Editing**: User can correct OCR, translation, zones, and styling
6. **Re-render**: Modified results can be re-processed without full pipeline
7. **Export**: Final image can be downloaded

## Quick Start

### Prerequisites
- Java 17+
- Node.js 18+
- Python 3.9+
- Docker (optional)

### Setup

#### 1. Python Service
```bash
cd python-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

#### 2. Spring Boot Backend
```bash
cd backend
./mvnw spring-boot:run
```

#### 3. Next.js Frontend
```bash
cd frontend
npm install
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- Python Service: http://localhost:8001

## Docker Setup

```bash
docker-compose up
```

## Features

- **Automated Processing**: Detect, read, translate, and clean panels automatically
- **Manual Editing**: Correct OCR errors, adjust translations, modify zones
- **Version Control**: Track different versions of processed panels
- **Job Management**: Async processing with status tracking
- **Multi-language**: Support for various source and target languages
- **Flexible Rendering**: Customize fonts, sizes, alignment, stroke

## API Documentation

- Backend API: http://localhost:8080/swagger-ui.html
- Python Service API: http://localhost:8001/docs

## Development

### Project Structure
```
LibraryWebtoon/
├── frontend/              # Next.js application
├── backend/              # Spring Boot application
├── python-service/       # FastAPI service
├── docker-compose.yml    # Docker orchestration
└── README.md
```

## License

MIT