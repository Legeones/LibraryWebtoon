# Setup Guide

## Prerequisites

- **Java**: 17 or higher
- **Node.js**: 18 or higher
- **Python**: 3.9 or higher
- **Maven**: 3.6+ (or use included wrapper)
- **Tesseract OCR**: Required for Python service
- **Docker** (optional): For containerized deployment

## Installation

### 1. Install System Dependencies

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-jpn tesseract-ocr-eng
```

#### macOS
```bash
brew install tesseract tesseract-lang
```

#### Windows
Download and install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki

### 2. Clone Repository

```bash
git clone https://github.com/Legeones/LibraryWebtoon.git
cd LibraryWebtoon
```

## Running Locally

### Option A: Run All Services Separately

#### 1. Python Processing Service

```bash
cd python-service

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (optional)
cp .env.example .env

# Run the service
uvicorn app.main:app --reload --port 8001
```

The Python service will be available at: http://localhost:8001
- API documentation: http://localhost:8001/docs

#### 2. Spring Boot Backend

```bash
cd backend

# Build and run
./mvnw spring-boot:run

# Or on Windows:
mvnw.cmd spring-boot:run
```

The backend will be available at: http://localhost:8080
- Swagger UI: http://localhost:8080/swagger-ui.html
- H2 Console: http://localhost:8080/h2-console

#### 3. Next.js Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Run development server
npm run dev
```

The frontend will be available at: http://localhost:3000

### Option B: Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Testing the Application

### 1. Access the Frontend

Open your browser and navigate to: http://localhost:3000

### 2. Upload a Test Image

1. Prepare a test panel image (PNG, JPG, or JPEG)
2. Drag and drop it onto the upload area or click to select
3. Wait for processing to complete

### 3. View Results

Once processing is complete, you'll see:
- Original uploaded image
- Detected text boxes (debug view)
- Mask showing text areas
- Clean image (text removed)
- Final image (with translated text)

### 4. Edit and Re-render

1. In the Region Editor, modify:
   - OCR text if incorrectly detected
   - Translation text
   - Font size and alignment
   - Text and stroke colors
2. Click "Re-render with Changes" to generate a new final image

### 5. Export

Click "Download Final Image" to save the translated panel

## API Testing

### Python Service

```bash
# Health check
curl http://localhost:8001/health

# Process an image
curl -X POST "http://localhost:8001/api/v1/process" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test-panel.png" \
  -F "job_id=test-123" \
  -F "source_language=ja" \
  -F "target_language=en"
```

### Spring Boot Backend

```bash
# Create a job
curl -X POST "http://localhost:8080/api/jobs" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test-panel.png" \
  -F "userId=test-user" \
  -F "sourceLanguage=ja" \
  -F "targetLanguage=en"

# Get job status
curl http://localhost:8080/api/jobs/{job-id}

# Get job image
curl http://localhost:8080/api/jobs/{job-id}/image/final -o final.png
```

## Troubleshooting

### Python Service Won't Start

**Issue**: ModuleNotFoundError or import errors
**Solution**: Make sure virtual environment is activated and dependencies installed
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Issue**: Tesseract not found
**Solution**: Install Tesseract and ensure it's in your PATH
```bash
# Check if tesseract is installed
tesseract --version

# If not found, install it (see Installation section)
```

### Spring Boot Backend Won't Start

**Issue**: Port 8080 already in use
**Solution**: Change port in `application.properties`:
```properties
server.port=8081
```

**Issue**: Cannot connect to Python service
**Solution**: Make sure Python service is running on port 8001, or update:
```properties
python.service.url=http://localhost:8001
```

### Next.js Frontend Won't Start

**Issue**: Cannot find module errors
**Solution**: Delete node_modules and reinstall
```bash
rm -rf node_modules package-lock.json
npm install
```

**Issue**: Cannot connect to backend
**Solution**: Check `.env.local` has correct backend URL:
```
NEXT_PUBLIC_API_URL=http://localhost:8080
```

### Processing Fails

**Issue**: OCR returns empty text
**Solution**: 
- Ensure Tesseract language packs are installed
- Check image quality and contrast
- Try adjusting image preprocessing

**Issue**: Images not displaying in frontend
**Solution**:
- Check that all three services are running
- Verify backend can access Python service
- Check browser console for CORS errors

## Development Tips

### Hot Reload

All services support hot reload in development mode:
- **Python**: `--reload` flag enabled
- **Spring Boot**: DevTools enabled
- **Next.js**: Built-in hot reload

### Debugging

#### Python Service
Add print statements or use Python debugger:
```python
import pdb; pdb.set_trace()
```

#### Spring Boot
Use IDE debugger or add logging:
```java
log.debug("Debug message");
```

#### Next.js
Use browser DevTools and React Developer Tools

### Database Access

H2 Console is available at: http://localhost:8080/h2-console
- JDBC URL: `jdbc:h2:file:./data/webtoon-tracker`
- Username: `sa`
- Password: (empty)

## Production Deployment

### Environment Variables

Create production environment files:

**Python** (`python-service/.env`):
```
STORAGE_PATH=/var/webtoon/storage
UPLOAD_PATH=/var/webtoon/uploads
DEEPL_API_KEY=your_production_key
```

**Spring Boot** (`application-prod.properties`):
```
spring.datasource.url=jdbc:postgresql://localhost:5432/webtoon
spring.datasource.username=webtoon_user
spring.datasource.password=secure_password
python.service.url=http://python-service:8001
```

**Next.js** (`.env.production`):
```
NEXT_PUBLIC_API_URL=https://api.yourdom ain.com
```

### Security Checklist

- [ ] Enable CSRF protection in Spring Security
- [ ] Configure proper CORS origins
- [ ] Use HTTPS for all communications
- [ ] Set up proper authentication
- [ ] Secure API keys in environment variables
- [ ] Use production database (PostgreSQL)
- [ ] Enable request rate limiting
- [ ] Set up proper logging and monitoring

### Docker Production

Use production docker-compose configuration:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Support

For issues and questions:
- Check the [ARCHITECTURE.md](ARCHITECTURE.md) for system details
- Review API documentation at `/docs` endpoints
- Check application logs for error messages
