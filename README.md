# LibraryWebtoon

> A comprehensive webtoon panel translation application with automated OCR, translation, and manual editing capabilities.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/Legeones/LibraryWebtoon.git
cd LibraryWebtoon

# 2. Start all services (3 terminals)
# Terminal 1 - Python Service
cd python-service && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8001

# Terminal 2 - Spring Boot Backend
cd backend && ./mvnw spring-boot:run

# Terminal 3 - Next.js Frontend
cd frontend && npm install && npm run dev
```

**Or use Docker:**
```bash
docker-compose up
```

Open http://localhost:3000 and start translating! 🎉

📖 **New here?** Check out the [Quick Start Guide](QUICKSTART.md)

## ✨ Features

- 🤖 **Automated Processing**: Detect text, OCR, translate, clean, and render automatically
- ✏️ **Manual Editing**: Correct OCR errors, adjust translations, customize styling
- 🎨 **Rich Editor**: Font controls, alignment, colors, stroke width
- 📊 **Real-time Preview**: View all processing stages (original, boxes, mask, clean, final)
- 💾 **Version Control**: Track different versions of processed panels
- 🔄 **Smart Re-rendering**: Re-render only what changed, skip full pipeline
- 🌐 **Multi-language**: Support for Japanese, English, Korean, Chinese, and more

## 🏗️ Architecture

This project follows a three-tier architecture:

```
┌─────────────────┐
│   Next.js       │  ← User Interface & Experience
│   Frontend      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Spring Boot    │  ← Business Logic & Orchestration
│   Backend       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │  ← Image Processing & ML
│ Python Service  │
└─────────────────┘
```

**Frontend (Next.js)**: User interface for uploading, editing, and viewing results
- Location: `frontend/`
- Tech: Next.js 14, React 18, TypeScript, Tailwind CSS
- Port: 3000

**Backend (Spring Boot)**: Application core, authentication, data management
- Location: `backend/`
- Tech: Spring Boot 3.2, JPA, H2/PostgreSQL
- Port: 8080

**Processing Service (Python FastAPI)**: Vision, OCR, translation, image processing
- Location: `python-service/`
- Tech: FastAPI, PaddleOCR, OpenCV, PIL
- Port: 8001

📚 **Learn more**: [Architecture Documentation](ARCHITECTURE.md)

## 🔧 Technology Stack

### Frontend
- **Framework**: Next.js 14 with TypeScript
- **UI**: Tailwind CSS, custom components
- **State**: Zustand
- **HTTP**: Axios

### Backend
- **Framework**: Spring Boot 3.2
- **Database**: H2 (dev), PostgreSQL (prod)
- **Security**: Spring Security
- **API Docs**: Swagger/OpenAPI

### Processing Service
- **Framework**: FastAPI
- **Text Detection**: PaddleOCR
- **OCR**: PaddleOCR
- **Inpainting**: OpenCV
- **Typesetting**: Pillow (PIL)
- **Translation**: Mock, DeepL, Google Translate

## 📋 Prerequisites

- **Java**: 17 or higher
- **Node.js**: 18 or higher  
- **Python**: 3.9 or higher
- **Docker** (optional): For containerized deployment

## 📖 Documentation

- [**Quick Start**](QUICKSTART.md) - Get running in 5 minutes
- [**Setup Guide**](SETUP.md) - Detailed installation and configuration
- [**Architecture**](ARCHITECTURE.md) - System design and data flow
- **API Docs**:
  - Python Service: http://localhost:8001/docs
  - Spring Backend: http://localhost:8080/swagger-ui.html

## 🎯 Workflow

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

## 🚀 Deployment

### Local Development
See [QUICKSTART.md](QUICKSTART.md) for quick setup.

### Docker
```bash
docker-compose up
```

### Production
See [SETUP.md](SETUP.md) for production deployment guide.

## 🛠️ Development

### Project Structure
```
LibraryWebtoon/
├── frontend/              # Next.js application
├── backend/               # Spring Boot application
├── python-service/        # FastAPI service
├── docker-compose.yml     # Docker orchestration
├── ARCHITECTURE.md        # Architecture documentation
├── SETUP.md              # Setup guide
└── QUICKSTART.md         # Quick start guide
```

### Running Tests

```bash
# Python tests
cd python-service
pytest

# Backend tests
cd backend
./mvnw test

# Frontend tests
cd frontend
npm test
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- PaddleOCR for text detection and OCR
- OpenCV for image inpainting
- Spring Boot for robust backend framework
- Next.js for excellent frontend experience
- FastAPI for high-performance Python API

## 📧 Support

For issues and questions:
- 📝 Open an issue on GitHub
- 📖 Check the documentation
- 🔍 Review existing issues

---

Made with ❤️ for the webtoon translation community