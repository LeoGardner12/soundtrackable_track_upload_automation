import openpyxl
from pathlib import Path
import os
import shutil
import zipfile 
import datetime
import pprint
from read_excel import read_excel
import shutil

def copy_file(src, dst):
	shutil.copy(src, dst)


def get_all_file_paths(directory): 
    # initializing empty file paths list 
    file_paths = [] 
  
    # crawling through directory and subdirectories 
    for root, directories, files in os.walk(directory): 
        for filename in files: 
            # join the two strings in order to form the full filepath. 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath) 
  
    # returning all file paths 
    return file_paths       

def zip_dir(directory, zipname):
    """
    Compress a directory (ZIP file).
    """
    if os.path.exists(directory):
        outZipFile = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)

        # The root directory within the ZIP file.
        rootdir = os.path.basename(directory)

        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:

                # Write the file named filename to the archive,
                # giving it the archive name 'arcname'.
                filepath   = os.path.join(dirpath, filename)
                parentpath = os.path.relpath(filepath, directory)
                arcname    = os.path.join(rootdir, parentpath)

                outZipFile.write(filepath, arcname)

    outZipFile.close()  

def only_tracks_with_full_info(track_list_dic, directory_of_wavs_mp3s):
	# returns a track list of track which have information in the spreadsheet and have wav and mp3 files
	directory_of_wavs_mp3s = directory_of_wavs_mp3s + "/"
	track_list = []
	for track in track_list_dic:
		if os.path.exists(directory_of_wavs_mp3s+ track["name"] + ".mp3") or os.path.exists(directory_of_wavs_mp3s+ track["name"] + ".wav"):
			track_list.append(track)
	return track_list

def write_cue_sheet(path_to_cue_sheet, track):
	f = open(path_to_cue_sheet, "w+")
	f.write("Cue Sheet Information\n") 	
	f.write("\n")
	f.write("Composer: Sam Gardner\n") 
	f.write("Copyright Holder: Sam Gardner\n") 
	f.write("Publisher: Sam Gardner\n") 
	f.write("PRO (Performing Rights Organization): PRS (Performing Rights Society)\n")
	f.write("CAE Number: 760723150\n") 
	f.write("\n")
	f.write("If you use either the 'Sections' or the 'Stems', just use the ISRC code below.\n") 
	f.write("\n")
	f.write("Track Title: " + track["name"]+"\n") 
	try:
		f.write("ISRC Code: " + track["isrc_code"]+"\n")
	except:
		print("no isrc_code") 
	try:
		f.write("PRS Tunecode: " + track["prs_tunecode"]+"\n") 
	except:
		print("no prs_tunecode")
	try:	
		f.write("ISWC Code: " + track["iswc_code"]+"\n") 
	except:
		print("no iswc_code")	
	f.close()

# 	A Bad Story
# Cue Sheet Information

# Composer: Sam Gardner
# Copyright Holder: Sam Gardner
# Publisher: Sam Gardner
# PRO (Performing Rights Organization): PRS (Performing Rights Society)
# CAE Number: 760723150

# If you use either the 'Segments' or the 'Stems', just use the ISRC code for the original track (the first in the list of tracks below).


# Track Title: A Bad Story
# ISRC Code: UKA492000502
# PRS Tunecode: 406482AS
# ISWC Code: T-932.551.020-1

def create_product_files_sections(src_track_directory, dst_directory, track, license_agreement, sections_instructions):
	
	track_title = track["name"]

	path_sections = dst_directory + "/" + track_title+" - Sections/"
	if not (os.path.isdir(path_sections)):
		os.mkdir(path_sections)
	
	path_sections_guides = dst_directory + "/" + track_title+" - Sections/Guides - Use These to Create a Rough Track Structure"
	if not (os.path.isdir(path_sections_guides)):
		os.mkdir(path_sections_guides)

	path_sections_sections = dst_directory + "/" + track_title+" - Sections/Sections - Use These to Create a Final Track Structure" 
	if not (os.path.isdir(path_sections_sections)):
		os.mkdir(path_sections_sections)

	for file in os.listdir("all_tracks/"):
		if "-" in file:
			if "Guide" in file and track_title in file.partition("-")[0].strip():
				copy_file(src_track_directory + "/" + file, path_sections_guides)
			if "Section" in file and track_title in file.partition("-")[0].strip():
				copy_file(src_track_directory + "/" + file, path_sections_sections)

	copy_file(src_track_directory + "/" + track_title + ".mp3", path_sections)
	copy_file(src_track_directory + "/" + track_title + ".wav", path_sections)
	
	copy_file(license_agreement, path_sections + license_agreement)
	copy_file(sections_instructions, path_sections + sections_instructions)
	write_cue_sheet(dst_directory + "/" + track_title+" - Sections/" + track_title + " - Cue Sheet Information.txt", track)
		

	zip_dir(dst_directory + "/" + track_title+" - Sections/", track_title+" - Sections.zip")
	shutil.move(track_title+" - Sections.zip", dst_directory + "/")

def create_product_files_stems(src_track_directory, dst_directory, track, license_agreement):

	track_title = track["name"]

	if os.path.isdir(dst_directory + "/" + track_title+" - Stems/"):
		shutil.rmtree(dst_directory + "/" + track_title+" - Stems/")


	os.mkdir(dst_directory + "/" + track_title+" - Stems/")
	os.mkdir(dst_directory + "/" + track_title+" - Stems/" + "Stems MP3/")
	os.mkdir(dst_directory + "/" + track_title+" - Stems/" + "Stems WAV/")

	#Copy both wav and mp3 files (Stems) 
	copy_file(src_track_directory + "/" + track_title + ".mp3", dst_directory + "/" + track_title+" - Stems/")
	copy_file(src_track_directory + "/" + track_title + ".wav", dst_directory + "/" + track_title+" - Stems/")
	copy_file(license_agreement, dst_directory + "/" + track_title +" - Stems/" + "/" + license_agreement)
	
	write_cue_sheet(dst_directory + "/" + track_title+" - Stems/" + track_title+ " - Cue Sheet Information.txt", track)

	#seperate the stem mp3 files from the wav files 
	mp3_and_wav_list = os.listdir(src_track_directory+'/')
	for file in mp3_and_wav_list:
		if "-" in file and track_title == file.partition("-")[0].strip() and "Guide" not in file and "Section" not in file:
			if file[-3:] == "mp3":
				copy_file(src_track_directory + "/" +file, dst_directory + "/" + track_title+" - Stems/" + "Stems MP3")
			
			elif file[-3:] == "wav":
				copy_file(src_track_directory + "/" +file, dst_directory + "/" + track_title+" - Stems/" + "Stems WAV")

	zip_dir(dst_directory + "/" + track_title+" - Stems/", track_title+" - Stems"+".zip")
	shutil.move(track_title+" - Stems"+".zip", dst_directory + "/")



def create_product_files_base(src_track_directory, dst_directory, track, license_agreement):
	track_title = track["name"]
	if os.path.isdir(dst_directory + "/" + track_title+'/'):
		shutil.rmtree(dst_directory + "/" + track_title+'/')


	os.mkdir(dst_directory + "/" + track_title+'/')
	#Copy both wav and mp3 files 
	copy_file(src_track_directory + "/" + track_title + ".mp3", dst_directory + "/" + track_title)
	copy_file(src_track_directory + "/" + track_title + ".wav", dst_directory + "/" + track_title)

	#create Cue Sheet 
	write_cue_sheet(dst_directory + "/" + track_title + '/' + track_title +" - Cue Sheet Information.txt", track)

	#Copy license agreement 
	copy_file(license_agreement, dst_directory + "/" + track_title + "/" + license_agreement)
	
	zip_dir(dst_directory + "/" + track_title+"/", track_title+".zip")
	shutil.move(track_title+".zip", dst_directory + "/")


def create_product_files(src_track_directory, dst_directory, track_list, license_agreement, sections_instructions):
	if not (os.path.isdir(dst_directory)):
		os.mkdir(dst_directory)

	

	track_list = only_tracks_with_full_info(track_list, src_track_directory)
	
	for track in track_list:
		track_title = track["name"]
		print("Creating directorys and zipping: " + track_title)
		# pprint.pprint(track)
	
		#create directorys

		# print(any('A Gentle Theme - Guide' in filename for filename in os.listdir(all_tracks)))
	# try:
		if any(track_title + " - Guide" in filename for filename in os.listdir(src_track_directory)):
			if track_title + " - Sections.zip" not in os.listdir(dst_directory):
				create_product_files_sections(src_track_directory, dst_directory, track, license_agreement, sections_instructions)		
	# except:
		# print("couldnt create_product_files_sections")
	# try:
		if track_title + ".zip" not in os.listdir(dst_directory):
			create_product_files_base(src_track_directory, dst_directory, track, license_agreement)
	# except:
		# print("couldnt create_product_files_base")
	# try:
		if any((track_title + " -" in filename) and (track_title + " - Guide" not in filename and track_title + " - Section" not in filename) for filename in os.listdir(src_track_directory)):
			if track_title + " - Stems.zip" not in os.listdir(dst_directory):
				create_product_files_stems(src_track_directory, dst_directory, track, license_agreement)
		# except:
			# print("couldnt create_product_files_stems")

# excel_filename = 'track_information.xlsx'
# license_agreement = 'License Agreement.pdf'
# all_tracks = "all_tracks"
