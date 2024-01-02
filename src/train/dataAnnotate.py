from dataOrchestrate import DataOrchestrate
data = DataOrchestrate()

# Replace with link of desired playlist to pull frames from
playlistUrl = None
videoUrls = data.getPlaylistVideoLinks(playlistUrl)

for url in videoUrls:
    data.youtubeFrameExtract(url)

# Replace with absolute path to desired .pt YOLO model
modelDir = None
data.autoAnnotate(modelDir)