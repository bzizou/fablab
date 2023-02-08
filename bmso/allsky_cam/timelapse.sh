# Creates a timelapse from all frames of the BMSO allsky cam into the current directory
ffmpeg -framerate 24 -pattern_type glob -i 'BMSO*.jpg' -q:v 0 -vf "eq=contrast=1.5:brightness=0.1,colorbalance=bh=+0.1,unsharp=luma_msize_x=5:luma_msize_y=5:luma_amount=2,owdenoise" -vcodec libx264 timelapse.avi
