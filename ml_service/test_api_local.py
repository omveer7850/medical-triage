import os
import sys

# Add current folder to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "AI" in data["service"]
    print("✓ Root endpoint test passed.")

def test_predict_xray_mock():
    import io
    from PIL import Image
    
    file_data = io.BytesIO()
    Image.new('RGB', (256, 256), color='red').save(file_data, 'JPEG')
    file_data.seek(0)
    
    response = client.post(
        "/api/predict/xray",
        files={"file": ("test.jpg", file_data, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert "severity" in data
    assert "visual_explainability" in data
    print("✓ X-ray prediction endpoint test passed.")

def test_predict_skin_mock():
    import io
    from PIL import Image
    
    file_data = io.BytesIO()
    Image.new('RGB', (256, 256), color='blue').save(file_data, 'JPEG')
    file_data.seek(0)
    
    response = client.post(
        "/api/predict/skin",
        files={"file": ("test.jpg", file_data, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert "severity" in data
    assert "visual_explainability" in data
    print("✓ Skin lesion prediction endpoint test passed.")

if __name__ == "__main__":
    print("Starting local API verification...")
    try:
        test_read_main()
        test_predict_xray_mock()
        test_predict_skin_mock()
        print("\nAll local ML Service API tests passed successfully!")
    except Exception as e:
        print(f"\nVerification failed: {e}")
        sys.exit(1)
