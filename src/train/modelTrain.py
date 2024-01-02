from ultralytics import YOLO
from torch import cuda
"""
import torch
cudaAvailability = torch.cuda.is_available()

if(cudaAvailability):
    deviceCount = torch.cuda.device_count()
    currentDevice = torch.cuda.current_device()
    currentDeviceName = torch.cuda.get_device_name(currentDevice)
    print(f"Number of cuda devices: {deviceCount}\nCurrent device name: {currentDeviceName}")
else:
    print("Cuda not available.")

"""

# TODO: Replace modelPath assignment of None with robust model path assignment
# modelPath assignment should be a .yaml including content for the dataset you want to train off of
dataPath = None
model = YOLO('yolov8l.pt')

# NOTE: Batch size set smaller currently for the larger model and hardware constraints. This should be changed back to its default later.
model.train(data=dataPath, epochs=150, imgsz=640, batch=12)