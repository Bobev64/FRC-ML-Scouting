import cv2
from ultralytics import YOLO
# TODO: Replace all variable assignments of None with robust path assignments

# Load the YOLOv8 model
modelPath = None
model = YOLO(modelPath)

# Open the video file
video_path = None
cap = cv2.VideoCapture(video_path)

videoOut= None
video = cv2.VideoWriter(videoOut,cv2.VideoWriter_fourcc(*'MPEG'),30,(1080,1920))
# Loop through the video frames
while (True):
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # write the annotated frame to mp4 file
        video.write(annotated_frame)
        cv2.imshow("output", annotated_frame)
    if cv2.waitKey(33) == ord('a'):
        break

cv2.destroyAllWindows()
video.release()
cap.release()