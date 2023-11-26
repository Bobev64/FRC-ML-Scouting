import cv2
from ultralytics import YOLO
import numpy as np
import matplotlib.pyplot as plt

# TODO: Replace all variable assignments of None with robust path assignments

mode = 2

# Load the YOLOv8 model
modelPath = None
model = YOLO(modelPath)

# Open the video file
video_path = None
cap = cv2.VideoCapture(video_path)

# videoOut = None
# video = cv2.VideoWriter(videoOut,cv2.VideoWriter_fourcc(*'MPEG'),30,(1080,1920))

if mode == 1:
    # Loop through the video frames
    while (True):
        # Read a frame from the video, return whether a frame can be read
        success, frame = cap.read()
    
        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame)
    
            # Visualize the results on the frame
            annotated_frame = results[0].plot()
    
            # write the annotated frame to mp4 file
            # video.write(annotated_frame)
            cv2.imshow("output", annotated_frame)
        # Press the key "q" to quit program
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()
    # video.release()

# Run through all frames, make heat map.
elif mode == 2:
    i = 0


    while(True):
        success, frame = cap.read()
        i += 1

        if success:

            results=model(frame)
            npBoxArray = results[0].boxes.xyxy.cpu().numpy()

            if npBoxArray.size != 0:
                print(f"[+] Frame number: {i}\n[+] Results: {npBoxArray}\n")
                for box in npBoxArray:
                    mdptX = np.divide(np.add(box[0], box[2]), 2.0)
                    mdptY = np.divide(np.add(box[1], box[3]), 2.0)
                    print(f"\t[+] Midpoint X: {mdptX}\tMidpoint Y: {mdptY}")
                    plt.plot(mdptX, mdptY, 'r,')
            else:
                print("[+] No robots detected")

        if cap.grab() is True:
            continue
        else:
            plt.show()

cap.release()