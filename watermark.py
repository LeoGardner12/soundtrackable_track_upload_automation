from pydub import AudioSegment
import os
import time
import sys
#watermarkbeta.py, or whatever name you want to use
#Python audio watermarking script that takes
#one argument (the name of the audio file being watermarked)
#overlays a second audio file over the beginning and outputs
#it to a destination folder/file
#requires Pydub and ffmpeg libraries/frameworks

def add_watermark(src_directory, dst_filename, watermark_file):
	if os.path.isdir(dst_filename) == False:
		os.mkdir(dst_filename + '/')

	for track in os.listdir(src_directory):
		if "-" not in track:
			if track[:-4]+ " - Watermark.mp3" not in os.listdir(dst_filename):
	
				print("Watermarking audio file : ", track)
				time.sleep (3)
				track_to_overlay = AudioSegment.from_mp3(src_directory+ "/" + track)
				watermrk = AudioSegment.from_mp3(watermark_file+".mp3")
	
				i = 0
				#initial start watermark
				output1 = track_to_overlay.overlay(watermrk, i)
				while i < 400000:
					output1 = output1.overlay(watermrk, i)
					i = i+10000
		
				dest = os.path.join(dst_filename, track[:-4]+ " - Watermark.mp3" )
				output1.export(dest, format = "mp3")
				# sys.exit()


add_watermark("mp3_128kbps", "watermarked_mp3_128kbps" ,"Sountrackable Watermark")