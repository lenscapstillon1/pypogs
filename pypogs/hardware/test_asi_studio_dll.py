import zwoasi
import os
from pathlib import Path

def test_asi_dll():
    dll_path = r"C:\Program Files\ASIStudio\ASICamera2.dll"
    print(f"Testing DLL at: {dll_path}")
    
    # Verify DLL exists
    if not os.path.exists(dll_path):
        print(f"Error: DLL file not found at {dll_path}")
        return
    
    # Attempt to initialize zwoasi with the DLL
    try:
        zwoasi.init(dll_path)
        print("DLL initialized successfully")
    except Exception as e:
        print(f"Error initializing DLL: {str(e)}")
        return
    
    # Check number of connected cameras
    try:
        num_cameras = zwoasi.get_num_cameras()
        print(f"Number of cameras detected: {num_cameras}")
        if num_cameras > 0:
            camera_names = zwoasi.list_cameras()
            print(f"Detected cameras: {camera_names}")
            # Get properties of the first camera
            camera = zwoasi.Camera(0)
            properties = camera.get_camera_property()
            print(f"Camera properties: {properties}")
        else:
            print("No cameras detected. Ensure camera is connected and driver is installed.")
    except Exception as e:
        print(f"Error detecting cameras: {str(e)}")

if __name__ == "__main__":
    test_asi_dll()