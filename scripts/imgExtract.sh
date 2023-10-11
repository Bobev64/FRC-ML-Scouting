#!/bin/bash

# USAGE: ./image_extract.sh [file_name] [number of images to sample (optional)]
#if [[ "$1"=="*/" ]]; then
find "$1" -type f \( -name "*.mp4" -o -name "*.mkv" -o -name "*.webm" \) -exec sh -c '
	file=${1##*/}
	fileName=${file%%.*}
	echo "$file"
	echo "$fileName"
' find-sh {} \;

# Get filename without extension
# # Default num of images to extract is 30 if no argument provided
# if [[ "$2" -eq "" ]]; then
# 	imgCount=30
# else
# 	imgCount="$2"
# fi
# 
# 
# # Make folder to dump images to if it doesn't exist
# destinationDir=./"$fileName"_imgs
# mkdir -p $destinationDir
# 
# # -count_packets is way faster than -count_frames, although it *technically* doesn't count frames
# totalFrames="$(ffprobe -v error -select_streams v:0 -count_packets \
# 				-show_entries stream=nb_read_packets -of csv=p=0 $1)"
# 
# echo "TOTAL FRAME COUNT: $totalFrames"
# 
# # Calc num of frames to step by for desired image count
# # NOTE: Occasionally outputs one more frame than desired.
# frameStep=$((totalFrames / imgCount))
# 
# # Output frames from video with frame number
# ffmpeg -i "$1" -vf "select=not(mod(n\,$frameStep))" -fps_mode \
# 				passthrough "${destinationDir}/${fileName}_frame_%d.jpg"