import torch
import torch.nn as nn
import torchvision.models as models
import os

class SkinLesionClassifier(nn.Module):
    """
    Skin Lesion Classifier model based on ResNet-50.
    Classifies 7 different dermatoscopic skin lesion classes (HAM10000).
    """
    def __init__(self, num_classes=7, pretrained=False):
        super(SkinLesionClassifier, self).__init__()
        self.backbone = models.resnet50(weights=models.ResNet50_Weights.DEFAULT if pretrained else None)
        
        # Replace the final fully connected layer
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Linear(num_features, num_classes)
            # Softmax is applied during inference / API response
        )

    def forward(self, x):
        return self.backbone(x)

def get_skin_model(weights_path: str = None) -> SkinLesionClassifier:
    """Instantiates the skin lesion classifier and optionally loads weights."""
    model = SkinLesionClassifier(num_classes=7, pretrained=False)
    
    # Get last convolutional layer for Grad-CAM (layer4 for ResNet50)
    target_layer = model.backbone.layer4
    
    if weights_path and os.path.exists(weights_path):
        try:
            model.load_state_dict(torch.load(weights_path, map_location="cpu"))
            print(f"Loaded skin lesion classifier weights from {weights_path}")
        except Exception as e:
            print(f"Could not load weights from {weights_path}: {e}. Initialized with random weights.")
    else:
        print("Skin lesion classifier weights file not found. Initializing model with random weights.")
        
    return model, target_layer

# List of HAM10000 categories and descriptive names
SKIN_CLASSES = [
    "Actinic Keratoses (Bowen's disease)",
    "Basal Cell Carcinoma",
    "Benign Keratosis-like Lesions",
    "Dermatofibroma",
    "Melanoma",
    "Melanocytic Nevi",
    "Vascular Lesions"
]

SKIN_CLASSES_SHORT = [
    "akiec",
    "bcc",
    "bkl",
    "df",
    "mel",
    "nv",
    "vasc"
]
