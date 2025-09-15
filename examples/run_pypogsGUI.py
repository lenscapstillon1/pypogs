# -*- coding: utf-8 -*-
"""
Run the pypogs GUI
==================
Run this script (i.e., type python run_pypogsGUI.py in a terminal window) to start the pypogs Graphical User Interface.
Tailored for dual-camera setup with ZWO ASI120MM Mini (coarse, monochrome, 1280x960, 3.75 µm, 120 mm focal length)
and ZWO ASI678MC (fine, color, 3840x2160, 2.0 µm, 135 mm focal length) using zwoasi library.
Image saving enabled; supports coarse-to-fine camera alignment and plate solving with tetra3 submodule.
"""

import sys
from pathlib import Path
sys.path.append('..')
sys.path.append(r'C:\Users\meeks\Documents\pypogs\pypogs')  # Add pypogs module path
sys.path.append(r'C:\Users\meeks\Documents\pypogs\tetra3')  # Add tetra3 submodule path for plate solving
import pypogs
import time

# CLEAR LOGS:
# Initialize debug logs for pypogs and GUI
open('../pypogs/debug/pypogs.txt', 'w').close()
open('../pypogs/debug/gui.txt', 'w').close()

# INITIALIZE PYPOGS SYSTEM:
sys = pypogs.System()

# DUAL CAMERA CONFIGURATION:
# Detect cameras to handle variable USB connection order
import zwoasi
try:
    zwoasi.init(r'C:\Program Files\ASIStudio\ASICamera2.dll')  # Initialize zwoasi with ASI Studio DLL
    camera_names = zwoasi.list_cameras()  # Get list of connected cameras
    print("Detected cameras:", camera_names)
    coarse_identity = camera_names.index('ZWO ASI120MM Mini') if 'ZWO ASI120MM Mini' in camera_names else 1  # ASI120MM Mini as coarse
    fine_identity = camera_names.index('ZWO ASI678MC') if 'ZWO ASI678MC' in camera_names else 0  # ASI678MC as fine
except Exception as e:
    print(f"Error initializing zwoasi: {e}")
    coarse_identity = 1  # Fallback
    fine_identity = 0

# Configure coarse camera: ZWO ASI120MM Mini (monochrome, 1280x960, 3.75 µm, 120 mm focal length)
coarsePlateScale = 206 * 3.75 / 120  # Plate scale (arcsec/pixel) = 6.438 arcsec/pixel
sys.add_coarse_camera(
    model="zwoasi",
    identity=coarse_identity,
    exposure_time=100,  # milliseconds
    plate_scale=round(coarsePlateScale, 3),  # 6.438 arcsec/pixel
    binning=1,  # Full resolution, no binning
    size_readout=(1280, 960),  # Full resolution for ASI120MM Mini
    rotation=0.0  # Adjust based on Star Field Test results (degrees)
)

# Configure fine camera: ZWO ASI678MC (color, 3840x2160, 2.0 µm, 135 mm focal length)
finePlateScale = 206 * 2.0 / 135  # Plate scale (arcsec/pixel) = 3.052 arcsec/pixel
sys.add_fine_camera(
    model="zwoasi",
    identity=fine_identity,
    exposure_time=50,  # milliseconds
    plate_scale=round(finePlateScale, 3),  # 3.052 arcsec/pixel
    binning=1,  # Full resolution, no binning
    size_readout=(3840, 2160),  # Full resolution with color_bin=False
    rotation=0.0  # Adjust based on Star Field Test results (degrees)
)

# ENABLE SAVING IMAGES FOR COARSE CAMERA (ASI120MM Mini):
sys.coarse_track_thread.img_save_frequency = 1  # Save every frame (1 = every frame, 2 = every second frame, etc.)
sys.coarse_track_thread.image_folder = Path(r'C:\Users\meeks\Documents\pypogs\images\coarse')  # Folder for coarse camera images

# ENABLE SAVING IMAGES FOR FINE CAMERA (ASI678MC):
sys.fine_track_thread.img_save_frequency = 1  # Save every frame
sys.fine_track_thread.image_folder = Path(r'C:\Users\meeks\Documents\pypogs\images\fine')  # Folder for fine camera images

# SET TARGET:
sys.target.get_and_set_tle_from_sat_id(25544)  # ISS = 25544

# APPLICATION LINKS:
# Connect to Stellarium and SkyTrack
sys.stellarium_telescope_server.start(address='127.0.0.1', port=10001, poll_period=1)
sys.target_server.start(address='127.0.0.1', port=12345, poll_period=1)

# START GUI:
try:
    pypogs.GUI(sys, 50)
except Exception:
    raise
finally:
    sys.deinitialize()