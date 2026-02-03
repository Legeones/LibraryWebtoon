# Quick Start Guide

Get up and running with LibraryWebtoon in 5 minutes!

## Prerequisites Check

```bash
# Check Java version (need 17+)
java -version

# Check Node.js version (need 18+)
node --version

# Check Python version (need 3.9+)
python3 --version

# Check Tesseract (required for OCR)
tesseract --version
```

If any are missing, see [SETUP.md](SETUP.md) for installation instructions.

## Quick Setup

### 1. Clone and Navigate

```bash
git clone https://github.com/Legeones/LibraryWebtoon.git
cd LibraryWebtoon
```

### 2. Start Python Service (Terminal 1)

```bash
cd python-service
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

✅ Service running at: http://localhost:8001

### 3. Start Spring Boot Backend (Terminal 2)

```bash
cd backend
./mvnw spring-boot:run  # On Windows: mvnw.cmd spring-boot:run
```

✅ Service running at: http://localhost:8080

### 4. Start Next.js Frontend (Terminal 3)

```bash
cd frontend
npm install
npm run dev
```

✅ Application running at: http://localhost:3000

## Test It Out!

1. **Open** http://localhost:3000 in your browser
2. **Drag & drop** a manga/webtoon panel image (or click to select)
3. **Watch** the automated processing:
   - Text detection ✓
   - OCR extraction ✓
   - Translation ✓
   - Background cleaning ✓
   - Text rendering ✓
4. **Edit** any text or styling in the Region Editor
5. **Download** your translated panel!

## Common Issues

### Tesseract Not Found
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-jpn

# macOS
brew install tesseract tesseract-lang

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### Port Already in Use
```bash
# Check what's using port 8080
lsof -i :8080

# Kill the process or change the port in application.properties
```

### Python Dependencies Fail
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Try installing again
pip install -r requirements.txt
```

## Docker Alternative

If you prefer Docker:

```bash
docker-compose up
```

All services will start automatically!

## What's Next?

- Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
- Check [SETUP.md](SETUP.md) for detailed configuration
- Explore the API docs at:
  - Python: http://localhost:8001/docs
  - Spring: http://localhost:8080/swagger-ui.html

## Need Help?

- Check logs in each terminal window
- Review troubleshooting in [SETUP.md](SETUP.md)
- Open an issue on GitHub

Happy translating! 🎉
