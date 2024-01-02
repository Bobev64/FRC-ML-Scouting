"""
Acquire data from specified video, annotate, and export.
"""

import cv2
import os
from random import randint
import yt_dlp
from multiprocessing.pool import Pool
from functools import partial
from ultralytics.data.annotator import auto_annotate
from pathlib import Path
from ultralytics import SAM, YOLO

class DataOrchestrate():
    def __init__(self):
        # TODO: Make this assignment work in places other than the repository root dir
        self.path = os.path.dirname(os.path.realpath(__name__))+"/res/autoAnnotate/"

    def newFrameExtract(self, url: str, frameCount: int, processNum: int):
        cap = cv2.VideoCapture(url)

    # Extract frames using an OpenCV stream 
    def frameExtract(self, url: str, skipFrames: int, processNumber: int):
        cap = cv2.VideoCapture(url)

        num_processes = 3 # NOTE: this acts as an effective lower bound for number of frames output by the program. Should figure out later.
        frames_per_process = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) // num_processes
        cap.set(cv2.CAP_PROP_POS_FRAMES, frames_per_process * processNumber)

        x = 0
        count = 0

        while x < 10 and count < frames_per_process:
            ret, frame = cap.read()
            if not ret:
                break
            filename=self.path+str(randint(1,100000))+".png"
            print(f"[+] FILE WRITEOUT: {filename}")
            x += 1
            cv2.imwrite(filename.format(count), frame)
            count += skipFrames  # Skip specified number of frames i.e. 10 seconds for 30 fps in the case of 300
            cap.set(1, count)

        cap.release()

    def youtubeFrameExtract(self, videoUrl: str):
        ydl_opts = {}
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        info_dict = ydl.extract_info(videoUrl, download=False)

        # This number is seemingly arbitrary right now. Outputs 3 frames no matter what. Should look into later.
        framesToSkip = 19000

        formats = info_dict.get('formats', None)

        print("[+] Obtaining frames")
        for f in formats:
            if f.get('format_note', None) == '1080p':
                url = f.get('url', None)
                cpu_count = os.cpu_count()
                with Pool(cpu_count) as pool:
                    pool.map(partial(self.frameExtract, url, framesToSkip), range(cpu_count))

    # Shamelessly ripped and modified from the Ultralytics implementation here:
    # https://github.com/ultralytics/ultralytics/blob/main/ultralytics/data/annotator.py 
    def autoAnnotate(self, modelDir: str, dataDir=None, outputDir=None):

        device = ''

        # Python argument values are evaled at function define-time.
        # a self.<varName> var is only available at function call time though, therefore this workaround
        # More details here: https://stackoverflow.com/questions/1802971/nameerror-name-self-is-not-defined
        det_model = YOLO(modelDir)
        if dataDir is None:
            data = Path(self.path)
        else:
            data=Path(dataDir)

        if not outputDir:
            outputDir = data.parent / f'{data.stem}_auto_annotate_labels'
        Path(outputDir).mkdir(exist_ok=True, parents=True)

        det_results = det_model(data, stream=True, device=device)

        for result in det_results:
            class_ids = result.boxes.cls.int().tolist()  # noqa
            if len(class_ids):
                nBoxes = result.boxes.xywhn # Normalized boxes for annotation output

                with open(f'{str(Path(outputDir) / Path(result.path).stem)}.txt', 'w') as f:
                    for i in range(len(nBoxes)):
                        s = nBoxes[i]
                        if len(s) == 0:
                            continue
                        box = map(str, nBoxes[i].reshape(-1).tolist())
                        f.write(f'{class_ids[i]} ' + ' '.join(box) + '\n')

    # Probably could be compressed into youtubeFrameExtract at some point.
    # For now we just feed the links from a list in a for loop to youtubeFrameExtract
    def getPlaylistVideoLinks(self, playlistUrl):
        ydlOpts = {}
        ytDLP = yt_dlp.YoutubeDL(ydlOpts)
        videoUrls = []

        with ytDLP:
            result = ytDLP.extract_info(playlistUrl, download=False)

            if 'entries' in result:
                video = result['entries']

            for i, item in enumerate(video):
                videoUrls.append(result['entries'][i]['webpage_url'])
            
        return videoUrls