import io
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2

# Preprocessing transforms for Chest X-ray (CheXNet-style)
# CheXNet uses DenseNet121 trained on ImageNet (224x224, normalized with ImageNet mean/std)
xray_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Preprocessing transforms for Skin Lesions
skin_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def preprocess_xray_image(image_bytes: bytes) -> torch.Tensor:
    """Preprocess raw chest X-ray image bytes into a PyTorch tensor."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = xray_transforms(image)
    return tensor.unsqueeze(0)  # Add batch dimension: [1, 3, 224, 224]

def preprocess_skin_image(image_bytes: bytes) -> torch.Tensor:
    """Preprocess raw skin lesion image bytes into a PyTorch tensor."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = skin_transforms(image)
    return tensor.unsqueeze(0)  # Add batch dimension: [1, 3, 224, 224]

def preprocess_teeth_image(image_bytes: bytes) -> torch.Tensor:
    """Preprocess raw teeth image bytes into a PyTorch tensor."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = skin_transforms(image) # Uses standard ImageNet 224x224 transforms
    return tensor.unsqueeze(0)

