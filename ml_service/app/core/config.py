import os

class Settings:
    PROJECT_NAME: str = "AI Medical Image Triage API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    CHEXNET_WEIGHTS_PATH: str = os.getenv("CHEXNET_WEIGHTS_PATH", "weights/chexnet.pth")
    SKIN_WEIGHTS_PATH: str = os.getenv("SKIN_WEIGHTS_PATH", "weights/skin_model.pth")

settings = Settings()
