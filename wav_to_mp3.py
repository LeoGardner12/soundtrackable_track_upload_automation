from pydub import AudioSegment
import os
from pathlib import Path
import openpyxl
from PIL import Image
from crop_artwork import crop_artwork
import datetime
from read_excel import read_excel
import pprint

def get_full_artwork_name(cropped_directory_name, cropped_file_prefix, filename_title):
	for artwork in os.listdir(cropped_directory_name):
		if filename_title.lower().replace("'", "") == artwork.lower().replace("'", "").partition(cropped_file_prefix)[2].strip()[:-4]:
			return cropped_directory_name+'/' + artwork

def embed_convert(src_directory, dst_directory_320k, dst_directory_128k, dst_directory_wav, list_of_track_dics,cropped_directory_name,cropped_file_prefix):
	#tasks a source directory of wav tracks and
	if not (os.path.isdir(dst_directory_128k)):
		os.mkdir(dst_directory_128k + '/')

	if not (os.path.isdir(dst_directory_320k)):
		os.mkdir(dst_directory_320k + '/')

		
	for filename in os.listdir(src_directory):
		if "Guide" in filename or "Section" in filename:
			continue

		print("Embed and convert: " + filename)

		if filename[-3:] != "wav":
			continue

		filename_title = str(filename).partition("-",)[0].strip()
		if "." in filename:
				filename_title = str(filename_title).partition(".",)[0].strip()
		
		tags = {}
		# print(list_of_track_dics)
		for dic in list_of_track_dics:
			if dic["name"] == filename_title:
				dic["title"] = filename[:-4]
				try:
					dic["genre"] = ", ".join(dic["genre_value(s)"])
				except:
					print("Error - wav_to_mp3.py line 44")
			# try:
				dic["comment"] = ", ".join(dic["mood_value(s)"]) + ", " + ", ".join(dic["instrument_value(s)"]) + ", " + dic["tempo_value(s)"]+ ", " + dic["bpm_value(s)"]
			# except:
				# print("Error - wav_to_mp3.py line 48")
				tags = dic

				# break
		# print("Metadata: ")
		pprint.pprint(tags)

		if tags == {}:
			print("unable to embed "+filename+" with meta data")
			continue
		# AudioSegment.from_wav(dst_directory_wav+ "/" + filename).export(dst_directory_wav+ "/" + filename[:-3] + "wav", format="wav", tags = tags, cover = cropped_directory_name+'/'+ cropped_file_prefix + filename_title +'.jpg')
		full_artwork_name = get_full_artwork_name(cropped_directory_name, cropped_file_prefix, filename_title)
		# print(full_artwork_name)
		try:
			if filename[:-4] + ".mp3" not in os.listdir(dst_directory_128k):
				AudioSegment.from_wav(src_directory+ "/" + filename).export(dst_directory_128k + '/' + filename[:-3] + "mp3", format="mp3", bitrate="128k", tags= tags, cover = full_artwork_name)
			
			if filename[:-4] + ".mp3" not in os.listdir(dst_directory_320k):
				AudioSegment.from_wav(src_directory+ "/" + filename).export(dst_directory_320k + "/" + filename[:-3] + "mp3", format="mp3", bitrate="320k", tags = tags, cover = full_artwork_name)
		except:
			print("Error couldnt convert to MP3"+filename)




# track_list = read_excel('track_information.xlsx')
# print(track_list)
# artwork_directory = "artwork"

# artwork_directory = "artwork"
# cropped_directory_name = "cropped_artwork"
# size = 320, 320
# quality = 80
# cropped_file_prefix = "cropped_"
# tracks_to_convert = "all_tracks"

# crop_artwork(artwork_directory,cropped_directory_name, size, quality, cropped_file_prefix)

# embed_convert(tracks_to_convert,tracks_to_convert,"mp3_128kbps",tracks_to_convert, track_list)
