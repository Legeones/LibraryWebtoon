import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import List
from app.models.schemas import TextRegion


class TypesettingService:
    """Service for rendering translated text on images"""
    
    def render_text(self, image_path: str, regions: List[TextRegion], 
                   output_path: str) -> None:
        """
        Render translated text on cleaned image
        
        Args:
            image_path: Path to cleaned image
            regions: List of text regions with translations
            output_path: Path to save final image
        """
        # Read image using OpenCV then convert to PIL for better text rendering
        cv_image = cv2.imread(image_path)
        if cv_image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        draw = ImageDraw.Draw(pil_image)
        
        for region in regions:
            if not region.translated_text:
                continue
            
            self._render_region(draw, region)
        
        # Convert back to OpenCV format and save
        result = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, result)
    
    def _render_region(self, draw: ImageDraw.Draw, region: TextRegion) -> None:
        """
        Render text for a single region
        
        Args:
            draw: PIL ImageDraw object
            region: Text region to render
        """
        bbox = region.bbox
        text = region.translated_text
        
        # Try to load font, fallback to default if not available
        try:
            font = ImageFont.truetype(region.font_family, region.font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        # Calculate text position based on alignment
        x = bbox.x
        y = bbox.y
        
        # Simple text wrapping
        wrapped_lines = self._wrap_text(text, font, bbox.width, draw)
        
        # Calculate vertical centering
        total_height = len(wrapped_lines) * region.font_size
        if total_height < bbox.height:
            y += (bbox.height - total_height) // 2
        
        # Draw each line
        for i, line in enumerate(wrapped_lines):
            line_y = y + i * region.font_size
            
            # Calculate horizontal position based on alignment
            if region.alignment == "center":
                bbox_width = draw.textbbox((0, 0), line, font=font)
                line_width = bbox_width[2] - bbox_width[0]
                line_x = x + (bbox.width - line_width) // 2
            elif region.alignment == "right":
                bbox_width = draw.textbbox((0, 0), line, font=font)
                line_width = bbox_width[2] - bbox_width[0]
                line_x = x + bbox.width - line_width
            else:  # left
                line_x = x
            
            # Draw stroke if specified
            if region.stroke_width > 0:
                for dx in range(-region.stroke_width, region.stroke_width + 1):
                    for dy in range(-region.stroke_width, region.stroke_width + 1):
                        if dx != 0 or dy != 0:
                            draw.text(
                                (line_x + dx, line_y + dy),
                                line,
                                font=font,
                                fill=region.stroke_color
                            )
            
            # Draw main text
            draw.text(
                (line_x, line_y),
                line,
                font=font,
                fill=region.text_color
            )
    
    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, 
                   max_width: int, draw: ImageDraw.Draw) -> List[str]:
        """
        Wrap text to fit within a maximum width
        
        Args:
            text: Text to wrap
            font: Font to use
            max_width: Maximum width in pixels
            draw: ImageDraw object for measuring text
            
        Returns:
            List of wrapped lines
        """
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Word is too long, add it anyway
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines if lines else [text]
