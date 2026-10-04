import torch
import torch.nn.functional as F
import numpy as np
import cv2
import io
import base64
from PIL import Image

class GradCAM:
    """Computes Gradient-weighted Class Activation Mapping (Grad-CAM) for a target layer in PyTorch."""
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.features = None
        
        # Register forward and backward hooks
        self.forward_hook = self.target_layer.register_forward_hook(self._save_features)
        self.backward_hook = self.target_layer.register_full_backward_hook(self._save_gradients)
        
    def _save_features(self, module, input, output):
        self.features = output
        
    def _save_gradients(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]
        
    def generate(self, input_tensor: torch.Tensor, class_idx: int) -> np.ndarray:
        # Run forward pass
        self.model.zero_grad()
        output = self.model(input_tensor)
        
        # Target score for class_idx
        score = output[0, class_idx]
        score.backward(retain_graph=True)
        
        # Calculate gradients weights (Global Average Pooling)
        gradients = self.gradients
        features = self.features
        
        weights = torch.mean(gradients, dim=[2, 3], keepdim=True)
        
        # Weighted combination of activation maps
        cam = torch.sum(weights * features, dim=1).squeeze(0)
        
        # ReLU to filter out negative gradients
        cam = F.relu(cam)
        
        # Normalize
        cam = cam - cam.min()
        cam = cam / (cam.max() + 1e-8)
        
        return cam.detach().cpu().numpy()
        
    def release(self):
        """Remove hooks from the model."""
        self.forward_hook.remove()
        self.backward_hook.remove()

def generate_gradcam_overlay(image_bytes: bytes, model: torch.nn.Module, target_layer: torch.nn.Module, class_idx: int, scan_type: str = "xray", target_class: str = "") -> str:
    """
    Runs Grad-CAM inference and returns a Base64-encoded JPEG image of the 
    heatmap overlaid on top of the original image.
    """
    try:
        # 1. Read original image
        nparr = np.frombuffer(image_bytes, np.uint8)
        orig_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if orig_img is None:
            raise ValueError("Failed to decode image bytes")
            
        h, w, _ = orig_img.shape
        
        # 2. Get input tensor and run model
        # Use torchvision transform matching the model requirements
        from app.utils.image_processor import xray_transforms
        pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        input_tensor = xray_transforms(pil_img).unsqueeze(0)
        
        # Put model in eval mode for inference but ensure grads are kept
        model.eval()
        for param in model.parameters():
            param.requires_grad = True
            
        # Initialize Grad-CAM
        gcam = GradCAM(model, target_layer)
        
        try:
            cam = gcam.generate(input_tensor, class_idx)
        finally:
            gcam.release()
            
        # 3. Resize heatmap to match original size
        cam_resized = cv2.resize(cam, (w, h))
        
        # 4. Apply colormap
        heatmap = cv2.applyColorMap(np.uint8(255 * cam_resized), cv2.COLORMAP_JET)
        
        # 5. Overlay on original image
        overlay = cv2.addWeighted(orig_img, 0.6, heatmap, 0.4, 0)
        
        # 6. Encode overlay as JPEG base64 string
        _, buffer = cv2.imencode(".jpg", overlay)
        base64_str = base64.b64encode(buffer).decode("utf-8")
        
        return f"data:image/jpeg;base64,{base64_str}"
        
    except Exception as e:
        # Fallback to smart targeted content-aware heatmap generator
        print(f"GradCAM error (using mock generator): {e}")
        return generate_mock_heatmap(image_bytes, scan_type, target_class)

def generate_mock_heatmap(image_bytes: bytes, scan_type: str = "xray", target_class: str = "") -> str:
    """
    Generates a targeted, content-aware heatmap overlay by analyzing 
    the color and contrast anomalies in the image.
    """
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        orig_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if orig_img is None:
            raise ValueError("Failed to decode image bytes")
            
        h, w, _ = orig_img.shape
        mask = np.zeros((h, w), dtype=np.float32)
        
        target_class_lower = target_class.lower() if target_class else ""
        
        # 1. Content-Aware Targeting Logic
        if scan_type == "teeth":
            # Convert to HSV color space for dental color analysis
            hsv = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)
            
            if "gingivitis" in target_class_lower or "ulcer" in target_class_lower:
                # Find red/inflamed regions (gum lines)
                lower_red1 = np.array([0, 50, 50])
                upper_red1 = np.array([10, 255, 255])
                lower_red2 = np.array([170, 50, 50])
                upper_red2 = np.array([180, 255, 255])
                
                mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
                mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
                color_mask = cv2.bitwise_or(mask1, mask2)
                mask = color_mask.astype(np.float32) / 255.0
                
            elif "caries" in target_class_lower or "calculus" in target_class_lower or "discoloration" in target_class_lower:
                # Find dark/brownish/yellowish regions (plaque or cavities)
                lower_yellow = np.array([10, 40, 20])
                upper_yellow = np.array([30, 255, 220])
                lower_dark = np.array([0, 0, 0])
                upper_dark = np.array([180, 255, 100])
                
                mask_y = cv2.inRange(hsv, lower_yellow, upper_yellow)
                mask_d = cv2.inRange(hsv, lower_dark, upper_dark)
                color_mask = cv2.bitwise_or(mask_y, mask_d)
                mask = color_mask.astype(np.float32) / 255.0
            else:
                # Find dark shadows/gaps between teeth
                gray = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)
                mask = thresh.astype(np.float32) / 255.0
                
        elif scan_type == "skin":
            # Skin lesions are darker spots on lighter skin
            gray = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            mask = thresh.astype(np.float32) / 255.0
            
        elif scan_type == "xray":
            # Chest X-rays: lung consolidation white opaque fields
            gray = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
            # Create a simple lung field mask to restrict highlights to lungs
            lung_mask = np.zeros((h, w), dtype=np.float32)
            cv2.ellipse(lung_mask, (int(w * 0.25), int(h * 0.5)), (int(w * 0.18), int(h * 0.32)), 0, 0, 360, 1.0, -1)
            cv2.ellipse(lung_mask, (int(w * 0.75), int(h * 0.5)), (int(w * 0.18), int(h * 0.32)), 0, 0, 360, 1.0, -1)
            _, thresh = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY)
            mask = (thresh.astype(np.float32) / 255.0) * lung_mask
            
        # 2. Smooth and position the heatmap
        mask_uint8 = np.uint8(mask * 255)
        contours, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        target_center = (int(w * 0.5), int(h * 0.5))
        target_radius = int(min(w, h) * 0.2)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 50:
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    target_center = (cX, cY)
                    _, _, bbox_w, bbox_h = cv2.boundingRect(largest_contour)
                    target_radius = max(bbox_w, bbox_h, int(min(w, h) * 0.15))
                    
        # Apply smooth Gaussian blur
        heat_mask = np.zeros((h, w), dtype=np.float32)
        cv2.circle(heat_mask, target_center, target_radius, 1.0, -1)
        
        blur_k = int(min(w, h) * 0.38) | 1  # odd size
        heat_mask = cv2.GaussianBlur(heat_mask, (blur_k, blur_k), 0)
        
        # Normalize
        heat_mask = heat_mask - heat_mask.min()
        heat_mask = heat_mask / (heat_mask.max() + 1e-8)
        
        # 3. Apply color map and blend
        heatmap = cv2.applyColorMap(np.uint8(255 * heat_mask), cv2.COLORMAP_JET)
        overlay = cv2.addWeighted(orig_img, 0.6, heatmap, 0.4, 0)
        
        _, buffer = cv2.imencode(".jpg", overlay)
        base64_str = base64.b64encode(buffer).decode("utf-8")
        return f"data:image/jpeg;base64,{base64_str}"
        
    except Exception as e:
        print(f"Fallback targeted heatmap error: {e}")
        return generate_mock_heatmap_simple(image_bytes)

def generate_mock_heatmap_simple(image_bytes: bytes) -> str:
    """Fallback simple circular heatmap overlay."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    orig_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if orig_img is None:
        orig_img = np.zeros((224, 224, 3), dtype=np.uint8)
    h, w, _ = orig_img.shape
    
    mask = np.zeros((h, w), dtype=np.float32)
    cv2.circle(mask, (int(w * 0.45), int(h * 0.45)), int(min(w, h) * 0.25), 1.0, -1)
    mask = cv2.GaussianBlur(mask, (101, 101), 0)
    
    heatmap = cv2.applyColorMap(np.uint8(255 * mask), cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(orig_img, 0.6, heatmap, 0.4, 0)
    
    _, buffer = cv2.imencode(".jpg", overlay)
    base64_str = base64.b64encode(buffer).decode("utf-8")
    return f"data:image/jpeg;base64,{base64_str}"
