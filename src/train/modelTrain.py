from ultralytics import YOLO
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
modelPath = "/home/bob/Code/FRC-ML-Scouting/res/dataset/data.yaml"
model = YOLO('yolov8m.yaml')
model.train(data=modelPath, epochs=150, imgsz=640)