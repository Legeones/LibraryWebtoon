import cv2
import numpy as np
from typing import List
from app.models.schemas import TextRegion


class InpaintingService:
    """Service for removing text from images using inpainting"""
    
    def create_mask(self, image_path: str, regions: List[TextRegion], 
                   output_path: str) -> None:
        """
        Create a binary mask of text regions
        
        Args:
            image_path: Path to original image
            regions: List of text regions to mask
            output_path: Path to save mask image
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Create empty mask
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        
        # Fill mask with regions
        for region in regions:
            bbox = region.bbox
            cv2.rectangle(
                mask,
                (bbox.x, bbox.y),
                (bbox.x + bbox.width, bbox.y + bbox.height),
                255,
                -1  # Filled rectangle
            )
        
        cv2.imwrite(output_path, mask)
    
    def inpaint_image(self, image_path: str, mask_path: str, 
                     output_path: str, method: str = "telea") -> None:
        """
        Remove text from image using inpainting
        
        Args:
            image_path: Path to original image
            mask_path: Path to mask image
            output_path: Path to save cleaned image
            method: Inpainting method (telea or ns)
        """
        # Read image and mask
        image = cv2.imread(image_path)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        
        if image is None or mask is None:
            raise ValueError("Could not read image or mask")
        
        # Choose inpainting algorithm
        if method == "telea":
            inpaint_flag = cv2.INPAINT_TELEA
        elif method == "ns":
            inpaint_flag = cv2.INPAINT_NS
        else:
            inpaint_flag = cv2.INPAINT_TELEA
        
        # Perform inpainting
        result = cv2.inpaint(image, mask, inpaintRadius=3, flags=inpaint_flag)
        
        cv2.imwrite(output_path, result)
