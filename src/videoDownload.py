import os
from functools import partial
from multiprocessing.pool import Pool
from random import randint

import cv2
import yt_dlp

def process_video_parallel(url, skip_frames, process_number):
    path = os.path.dirname(os.path.realpath(__name__))+"/"
    cap = cv2.VideoCapture(url)
    num_processes = os.cpu_count()
    frames_per_process = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) // num_processes
    cap.set(cv2.CAP_PROP_POS_FRAMES, frames_per_process * process_number)
    x = 0
    count = 0
    while x < 10 and count < frames_per_process:
        ret, frame = cap.read()
        if not ret:
            break
        filename=str(x)+"_"+str(randint(1,100000))+".png"
        x += 1
        cv2.imwrite(filename.format(count), frame)
        count += skip_frames  # Skip 300 frames i.e. 10 seconds for 30 fps
        cap.set(1, count)
    cap.release()

video_url = None  # The Youtube URL
ydl_opts = {}
ydl = yt_dlp.YoutubeDL(ydl_opts)
info_dict = ydl.extract_info(video_url, download=False)

formats = info_dict.get('formats', None)

print("Obtaining frames")
for f in formats:
    if f.get('format_note', None) == '1080p':
        url = f.get('url', None)
        cpu_count = os.cpu_count()
        with Pool(cpu_count) as pool:
            pool.map(partial(process_video_parallel, url, 600), range(cpu_count))