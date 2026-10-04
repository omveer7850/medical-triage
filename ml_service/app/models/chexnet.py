import torch
import torch.nn as nn
import torchvision.models as models
import os

class CheXNet(nn.Module):
    """
    CheXNet-style model based on DenseNet-121.
    Classifies 14 different thorax diseases from a chest X-ray.
    """
    def __init__(self, num_classes=14, pretrained=False):
        super(CheXNet, self).__init__()
        # Use standard DenseNet121 backbone
        self.backbone = models.densenet121(weights=models.DenseNet121_Weights.DEFAULT if pretrained else None)
        
        # Replace the classifier layer
        # DenseNet121 has classifier in self.backbone.classifier
        num_features = self.backbone.classifier.in_features
        self.backbone.classifier = nn.Sequential(
            nn.Linear(num_features, num_classes),
            nn.Sigmoid() # CheXNet outputs independent probabilities (multi-label)
        )

    def forward(self, x):
        return self.backbone(x)

def get_chexnet_model(weights_path: str = None) -> CheXNet:
    """Instantiates CheXNet and optionally loads state dict weights."""
    model = CheXNet(num_classes=14, pretrained=False)
    
    # Get last convolutional layer for Grad-CAM (features block of DenseNet121)
    # The last block in densenet121 is backbone.features.norm5
    target_layer = model.backbone.features.norm5
    
    if weights_path and os.path.exists(weights_path):
        try:
            model.load_state_dict(torch.load(weights_path, map_location="cpu"))
            print(f"Loaded CheXNet weights from {weights_path}")
        except Exception as e:
            print(f"Could not load weights from {weights_path}: {e}. Initialized with random weights.")
    else:
        print("CheXNet weights file not found. Initializing model with random weights.")
        
    return model, target_layer

# List of NIH ChestX-ray14 class names in correct order
CHEXNET_CLASSES = [
    "Atelectasis",
    "Cardiomegaly",
    "Effusion",
    "Infiltration",
    "Mass",
    "Nodule",
    "Pneumonia",
    "Pneumothorax",
    "Consolidation",
    "Edema",
    "Emphysema",
    "Fibrosis",
    "Pleural_Thickening",
    "Hernia"
]
