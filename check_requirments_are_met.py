import os

def check_requirments_artwork(directory_of_wavs_mp3s):
	# returns a track list of track which have information in the spreadsheet and have wav and mp3 files
	directory_of_wavs_mp3s = directory_of_wavs_mp3s + "/"
	for track in os.listdir(directory_of_wavs_mp3s):
		if "-" not in track and track[-3:] == "wav":
			has_artwork = False
			for art in os.listdir("artwork"):
				if track[:-4].lower().replace("'", "") in art.lower().replace("'", ""):
					has_artwork = True
					break

			if has_artwork == False:
				print("No artwork found for: "+track[:-4])
			# else:
				# print(track[:-4] + " has artwork")

# def check_requirments_excel(directory_of_wavs_mp3s):
# 	directory_of_wavs_mp3s = directory_of_wavs_mp3s + "/"
# 	for track in os.listdir(directory_of_wavs_mp3s):

check_requirments_artwork("all_tracks")