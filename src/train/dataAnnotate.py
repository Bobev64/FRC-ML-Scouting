from dataOrchestrate import DataOrchestrate
data = DataOrchestrate()

videoUrls = data.getPlaylistVideoLinks("https://www.youtube.com/playlist?list=PLrEBilNS0Pas73_4m5F837k-Ngc8Lh_Tp")

for url in videoUrls:
    data.youtubeFrameExtract(url)