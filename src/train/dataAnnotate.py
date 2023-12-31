from dataOrchestrate import DataOrchestrate
data = DataOrchestrate()

data.youtubeFrameExtract("https://www.youtube.com/watch?v=lHt-GOEVaoY")
data.autoAnnotate("INSERT_MODEL_DIR_HERE")