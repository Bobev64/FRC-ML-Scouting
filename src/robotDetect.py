import cv2
from ultralytics import YOLO
import numpy as np
import matplotlib.pyplot as plt

# TODO: Replace applicable variable assignments of None with robust path assignments
mode = 1

RED_ROBOT = 0.0
BLUE_ROBOT = 1.0

# Load the YOLOv8 model
modelPath = None
model = YOLO(modelPath)

# Open the video file
video_path = None
video = cv2.VideoCapture(video_path)

def outputInferenceVid(cap):
    # Loop through video frames
    while (True):
        # Read a frame from the video, return whether a frame can be read
        success, frame = cap.read()
    
        if success:
            # Run YOLOv8 inference on the frame
            results = model.predict(frame, conf=0.5)
    
            # Visualize the results on the frame
            annotated_frame = results[0].plot()
    
            cv2.imshow("output", annotated_frame)
        # Press the key "q" to quit program
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()
    # video.release()

def outputCenterPtPlot(cap):

    imgPath = None
    fig, ax = plt.subplots()
    ax.imshow(plt.imread(imgPath))

    i = 0
    while(True):
        success, frame = cap.read()
        i += 1
        if success:
            results=model(frame)

            # Retrieve x & y coordinates for opposing corners of all detected objects and convert them to a numpy array stored in the CPU
            npBoxArray = results[0].boxes.xyxy.cpu().numpy()

            # Retrieve alliances of robots present
            objClasses = results[0].boxes.cls.cpu().numpy()

            # Only process frame if there's actual detection going on
            if npBoxArray.size != 0:
                print(f"[+] Frame number: {i}\n[+] Results: {npBoxArray}\n[+] Classes: {objClasses}\n")

                # Get the bottom right corner of detected robot bounding box, plot on graph
                for box in npBoxArray:
                        ax.plot(box[2], box[3], 'r,')

                    # NOTE: Enable this later when distinction between red & blue alliance bots has become more accurate.
                    # for obj in objClasses:
                        # mdptX = np.divide(np.add(box[0], box[2]), 2.0)
                        # mdptY = np.divide(np.add(box[1], box[3]), 2.0)
                        # print(f"\t[+] Midpoint X: {mdptX}\tMidpoint Y: {mdptY}")

                        # Plot the midpoint as a red pixel or blue pixel depending on robot type
                        # if obj == RED_ROBOT:
                        #     ax.plot(box[2], box[3], 'r,')
                        # elif obj == BLUE_ROBOT:
                        #     ax.plot(box[2], box[3], 'b,')
                        # else:
                        #     print(f"[+] ERROR: Object class detected as: {obj}")
            else:
                print("[+] No robots detected")

        # If you can find the next frame, continue with loop
        if cap.grab() is True:
            continue
        else:
            break

    cap.release()
    plt.show()
   
if mode == 1:
    outputInferenceVid(video) 
elif mode == 2:
    outputCenterPtPlot(video)