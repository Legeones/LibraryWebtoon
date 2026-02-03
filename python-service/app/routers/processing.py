from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
import aiofiles
import os
from pathlib import Path
from app.models.schemas import (
    ProcessingResult, ProcessRequest, ProcessingOptions,
    RerenderRequest
)
from app.services.pipeline import ProcessingPipeline

router = APIRouter(prefix="/api/v1", tags=["processing"])

# Initialize pipeline
pipeline = ProcessingPipeline()


@router.post("/process", response_model=ProcessingResult)
async def process_panel(
    file: UploadFile = File(...),
    job_id: Optional[str] = None,
    source_language: str = "ja",
    target_language: str = "en",
    ocr_engine: str = "tesseract",
    translation_engine: str = "mock",
    inpaint_method: str = "telea"
):
    """
    Process a panel image through the complete pipeline
    
    - Detects text regions
    - Performs OCR
    - Translates text
    - Cleans image (inpainting)
    - Renders translated text
    """
    if not job_id:
        import uuid
        job_id = str(uuid.uuid4())
    
    # Save uploaded file
    temp_dir = Path("/tmp/webtoon-uploads")
    temp_dir.mkdir(exist_ok=True)
    
    input_path = temp_dir / f"{job_id}_input.png"
    
    async with aiofiles.open(input_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Create processing options
    options = ProcessingOptions(
        source_language=source_language,
        target_language=target_language,
        ocr_engine=ocr_engine,
        translation_engine=translation_engine,
        inpaint_method=inpaint_method
    )
    
    # Process image
    result = await pipeline.process_image(str(input_path), job_id, options)
    
    return result


@router.post("/rerender", response_model=dict)
async def rerender_panel(request: RerenderRequest):
    """
    Re-render text on a clean image without running full pipeline
    
    Useful for manual corrections to text, translation, or styling
    """
    if not os.path.exists(request.clean_image_path):
        raise HTTPException(status_code=404, detail="Clean image not found")
    
    output_path = await pipeline.rerender(
        request.clean_image_path,
        request.regions,
        request.job_id
    )
    
    return {
        "job_id": request.job_id,
        "final_image_path": output_path
    }


@router.get("/result/{job_id}")
async def get_result(job_id: str):
    """Get processing result for a job"""
    job_dir = Path(pipeline.storage_path) / job_id
    
    if not job_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job_id,
        "files": [f.name for f in job_dir.iterdir() if f.is_file()]
    }


@router.get("/image/{job_id}/{image_type}")
async def get_image(job_id: str, image_type: str):
    """
    Get an image for a job
    
    image_type: original, debug_boxes, mask, clean, final
    """
    job_dir = Path(pipeline.storage_path) / job_id
    image_path = job_dir / f"{image_type}.png"
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path, media_type="image/png")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "webtoon-processing"}
