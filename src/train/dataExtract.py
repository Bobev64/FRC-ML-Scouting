"""
Class to make acquiring and annotating data easier.
"""

import cv2
import ultralytics
import os
from random import randint
import yt_dlp
from multiprocessing.pool import Pool
from functools import partial

class DataExtract():
    def __init__(self):
        pass

    def parallelVideoProcess(self, url: str, skipFrames: int, processNumber: int):
        path = os.path.dirname(os.path.realpath(__name__))+"/"
        cap = cv2.VideoCapture(url)
        num_processes = os.cpu_count()
        frames_per_process = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) // num_processes
        cap.set(cv2.CAP_PROP_POS_FRAMES, frames_per_process * processNumber)
        x = 0
        count = 0
        while x < 10 and count < frames_per_process:
            ret, frame = cap.read()
            if not ret:
                break
            filename=str(x)+"_"+str(randint(1,100000))+".png"
            x += 1
            cv2.imwrite(filename.format(count), frame)
            count += skipFrames  # Skip specified number of frames i.e. 10 seconds for 30 fps in the case of 300
            cap.set(1, count)
        cap.release()

    def parallelFrameExtract(self, videoUrl: str):
        ydl_opts = {}
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        info_dict = ydl.extract_info(videoUrl, download=False)

        formats = info_dict.get('formats', None)

        print("[+] Obtaining frames")
        for f in formats:
            if f.get('format_note', None) == '1080p':
                url = f.get('url', None)
                cpu_count = os.cpu_count()
                with Pool(cpu_count) as pool:
                    pool.map(partial(self.parallelVideoProcess, url, 600), range(cpu_count))
    
    def autoAnnotate(self, frameDir):
        pass
