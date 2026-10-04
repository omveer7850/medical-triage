import torch
import torch.nn as nn
import torchvision.models as models
import os

class TeethClassifier(nn.Module):
    """
    Teeth Problems Classifier based on ResNet-18.
    Classifies dental images into 6 distinct dental/oral conditions:
    1. Calculus
    2. Caries (Tooth Decay)
    3. Gingivitis
    4. Mouth Ulcer
    5. Tooth Discoloration
    6. Hypodontia
    """
    def __init__(self, num_classes=6, pretrained=False):
        super(TeethClassifier, self).__init__()
        self.backbone = models.resnet18(weights=models.ResNet18_Weights.DEFAULT if pretrained else None)
        
        # Replace fully connected layer
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Linear(num_features, num_classes)
        )

    def forward(self, x):
        return self.backbone(x)

def get_teeth_model(weights_path: str = None) -> tuple:
    """Instantiates the teeth problems classifier and returns it along with the target layer for Grad-CAM."""
    model = TeethClassifier(num_classes=6, pretrained=False)
    
    # Target layer for Grad-CAM (last convolutional layer of ResNet18 is layer4)
    target_layer = model.backbone.layer4
    
    if weights_path and os.path.exists(weights_path):
        try:
            model.load_state_dict(torch.load(weights_path, map_location="cpu"))
            print(f"Loaded teeth classifier weights from {weights_path}")
        except Exception as e:
            print(f"Could not load weights from {weights_path}: {e}. Initialized with random weights.")
    else:
        print("Teeth classifier weights file not found. Initializing model with random weights.")
        
    return model, target_layer

# List of dental pathology categories in dataset
TEETH_CLASSES = [
    "Dental Calculus",
    "Dental Caries (Tooth Decay)",
    "Gingivitis (Gum Inflammation)",
    "Mouth Ulcer",
    "Tooth Discoloration",
    "Hypodontia (Missing Teeth)"
]

TEETH_CLASSES_SHORT = [
    "calculus",
    "caries",
    "gingivitis",
    "ulcer",
    "discoloration",
    "hypodontia"
]
