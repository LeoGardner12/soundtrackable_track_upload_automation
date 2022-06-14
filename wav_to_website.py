from file_organisation import create_product_files
from crop_artwork import crop_artwork
from wav_to_mp3 import embed_convert
from read_excel import read_excel
from aws_api import upload_to_aws,read_url_txt
import pprint
import wordpress_xmlrpc
from wordpress_xmlrpc import Client, WordPressPost
from upload_products import upload, upload_all_to_media, get_media_ids
import os
from mutagen.mp3 import MP3
from decimal import Decimal
import time
from mutagen.mp3 import MP3



excel_filename = 'track_information_to_add_final.xlsx'
# tracks_to_convert = "_ALL TRACKS"
url_txt = "url_list.txt"
watermark_url_txt = "watermark_url_list.txt"


# excel_filename = 'track_information.xlsx'
tracks_to_convert = "all_tracks"

product_variation_list = read_excel(excel_filename, tracks_to_convert)


track_list=[]
for product_variation in product_variation_list:
	track_list.append(product_variation[0][1])


license_agreement = 'License Agreement.pdf'
sections_instructions = 'Sections Instructions.pdf'
directory_128kbps = "mp3_128kbps"
#variables for cropping the artwork
artwork_directory = "artwork"
cropped_directory_name = "cropped_artwork"
size = 320, 320
quality = 80
cropped_file_prefix = "cropped_"
dest_directory = "result" 
bucket_name = "Removed for security"
watermark_directory = "watermarked_mp3_128kbps"


def add_aws_urls(product_variation_list, url_list):
	for list_of_products_and_variations in product_variation_list:
		for product_or_variation in list_of_products_and_variations:
			# dont set download url for products which dont have variations
			# a product with variations wont have a download_1_name
			if product_or_variation[1]["download_1_name"] != None:
				for url in url_list:
					if url[0][:-4] == product_or_variation[1]["download_1_name"][:-4]:
						product_or_variation[1]["download_1_url"] = url[1]
						break
	return product_variation_list


def add_watermark_aws_urls(product_variation_list, url_list):
	for list_of_products_and_variations in product_variation_list:
		for product_or_variation in list_of_products_and_variations:
			for url in url_list:
				if product_or_variation[0] == "Product":
					if url[0].split(" - ")[0] == product_or_variation[1]["name"]:
						product_or_variation[1]["watermark_url"] = url[1]

	return product_variation_list


def add_mp3_mins(product_variation_list):
	for list_of_products_and_variations in product_variation_list:
		for product_or_variation in list_of_products_and_variations:
			if product_or_variation[0] == "Product":
				for track in os.listdir(directory_128kbps):
					if product_or_variation[1]['name'] == str(track)[:-4]:
						duration = MP3(directory_128kbps+"/"+track)
						mins = duration.info.length//60
						seconds =  (duration.info.length % 60)
						product_or_variation[1]["mins_value(s)"] = "%02d:%02d" % (mins, seconds)
	return product_variation_list


# crop_artwork(artwork_directory,cropped_directory_name, size, quality, cropped_file_prefix)

# embed_convert(tracks_to_convert,tracks_to_convert,"mp3_128kbps",tracks_to_convert, track_list,cropped_directory_name,cropped_file_prefix)

# create_product_files(tracks_to_convert, dest_directory, track_list, license_agreement, sections_instructions)

# url_list = upload_to_aws(dest_directory, bucket_name, url_txt)
# watermark_url_list = upload_to_aws(watermark_directory, bucket_name, watermark_url_txt)





url_list = read_url_txt("url_list.txt")
watermark_url_list = read_url_txt("watermark_url_list.txt")


product_variation_list = add_aws_urls(product_variation_list, url_list)
product_variation_list = add_watermark_aws_urls(product_variation_list, watermark_url_list)

product_variation_list = add_mp3_mins(product_variation_list)

# # pprint.pprint(product_variation_list)

# # # image_mp3_id_list = upload_all_to_media("mp3_128kbps","cropped_artwork", "cropped_")
image_mp3_id_list = get_media_ids()
# # pprint.pprint(image_mp3_id_list)
upload(image_mp3_id_list, product_variation_list)


