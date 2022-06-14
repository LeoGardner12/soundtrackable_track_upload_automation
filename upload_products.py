from woocommerce import API
import csv
import numpy as np
import pprint
from pathlib import Path
import openpyxl
import pandas
import json
from json_excel_converter import Converter 
from json_excel_converter.xlsx import Writer
from correc_data_types import find_all_dict
import os
import requests
import string 
import wordpress_xmlrpc
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import mimetypes
import sys
from read_excel import read_excel


wcapi = API(
    url = "https://www.soundtrackable.com",
    consumer_key="Removed for security",
    consumer_secret="Removed for security",
    version="wc/v3"
)

def get_media_ids():
	client = Client('Removed for security','Removed for security', 'Removed for security')

	# pprint.pprint(wordpress_xmlrpc.methods.media.GetMediaLibrary([10]))
	# wordpress_xmlrpc.methods.media.GetMediaLibrary([10])
	allwp_media = client.call(wordpress_xmlrpc.methods.media.GetMediaLibrary([]))
	# print(allwp_media)
	image_mp3_id_list = []
	for m in allwp_media:
		# print(str(m.date_created)[:7].replace("-", "/"))
		title_id_dic = {}
		title_id_dic["metadata"] = m.metadata
		title_id_dic["title"] = m.title
		title_id_dic["id"] = m.id
		title_id_dic["date_created"] = str(m.date_created)[:7].replace("-", "/")
		image_mp3_id_list.append(title_id_dic)
	return image_mp3_id_list


# get_media_ids()

def upload_to_media(filename_path, data, client):
	 try:
	 	with open(filename_path, 'rb') as img:
	 		data['bits'] = xmlrpc_client.Binary(img.read())
	 	response = client.call(media.UploadFile(data))
	 	attachment_id = response
	 	return attachment_id
	 except:
	 	e = sys.exc_info()[0]
	 	print("counldnt upload: " + filename_path)
	 	print( "Error: %s" % e )
	 	# pprint.pprint(product_to_upload)
	 	return None



def upload_all_to_media(src_track_directory, cropped_directory_name, cropped_file_prefix):
  client = Client('Removed for security','Removed for security', 'Removed for security')
 
# # # set to the path to your file
  response_list = []
  for filename in os.listdir(src_track_directory):
    #check if track is not a stem and upload the image for it
    if "-" not in filename:
      filename_jpg = filename[:-3]+"jpg"

      filename_path = cropped_directory_name + "/" + cropped_file_prefix + filename_jpg
      print("Uploading " + filename_path + " To media")
      data = {
          # 'name': filename[:-4],
          'name': filename_jpg,
          'type': 'image/jpg',
      }
      response_list.append(upload_to_media(filename_path, data, client))

    filename_path = src_track_directory + "/" + filename
    print("Uploading " + filename_path + " To media")
    data = {
	# prepare metadata
		'name': filename
	}
    
    data['type'] = "audio/mpeg"


    response = upload_to_media(filename_path, data, client)

    response_list.append(response)

  return response_list


def convert_attribute_value(attribute_value):
	if "section" in attribute_value.lower():
		return "Track+Sections"
	if "stems" in attribute_value.lower():
		return "Track+Stems"
	if "only" in attribute_value.lower():
		return "Track Only"

def join_try_except(string):
	try:
		if ", ".join(string)[-1] == ",": 
			return ", ".join(string)[:-1] 
		else:
			return ", ".join(string)
	except:
		return string

def upload_product(product, image_mp3_id_list, c):

	product_to_upload = { 
	'purchasable': True,
 	'stock_quantity': None,
 	'stock_status': 'instock',
  	'virtual': True,
	}

	product_to_upload["name"] = product["name"]
	product_to_upload["type"] = product["type"].lower()
	if product_to_upload["type"] == "simple":
		product_to_upload["downloadable"] = True 
		product_to_upload["downloads"] = [{'file': product['download_1_url'], 'name': product['download_1_name'][:-4]}]
	
	product_to_upload["regular_price"] = str(product["regular_price"])
	description_list = []

	description_list.append(join_try_except(product["tags"]))
	description_list.append(join_try_except(product["mood_value(s)"]))
	description_list.append(join_try_except(product["purpose_value(s)"]))
	description_list.append(join_try_except(product["instrument_value(s)"]))
	description_list.append(product["tempo_value(s)"])

	description_list.append(str(product["mins_value(s)"]))
	description_list.append(str(product["bpm_value(s)"]))

	product_to_upload["description"] = join_try_except(description_list)

	# tags = []
	# for tag in description_list:
	# 	print(tag)
	# 	tags.append({'name': tag})
		
	# product_to_upload["tags"] = [{'id': 29, 'name': 'calming', 'slug': 'calming'},
 #          {'id': 30, 'name': 'chilled', 'slug': 'chilled'},
 #          {'id': 31, 'name': 'cold', 'slug': 'cold'},
 #          {'id': 32, 'name': 'elegent', 'slug': 'elegent'},
 #          {'id': 33, 'name': 'love', 'slug': 'love'},
 #          {'id': 34, 'name': 'pretty', 'slug': 'pretty'},
 #          {'id': 35, 'name': 'romantic', 'slug': 'romantic'},
 #          {'id': 36, 'name': 'serene', 'slug': 'serene'},
 #          {'id': 37, 'name': 'tranquil', 'slug': 'tranquil'}]


	attribute_list = []
	if product["platform"] != None:
		attribute_list.append({'id': 11,
                 'name': 'Platform',
                 'options': product['platform'].split(", "),
                 'position': 8,
                 'variation': False,
                 'visible': True})


	if product["choose_value(s)"] != None:
		attribute_list.append({'id': 3,
                 'name': 'Choose',
                 'options': product["choose_value(s)"].split(", "),
                 'position': 0,
                 'variation': True,
                 'visible': True})

	if product["mins_value(s)"] != None:
		attribute_list.append({'id': 2,
                 'name': 'Mins',
                 'options': product["mins_value(s)"],
                 'position': 1,
                 'variation': False,
                 'visible': True})

	if product["bpm_value(s)"] != None:
		attribute_list.append({'id': 1,
                 'name': 'BPM',
                 'options': product["bpm_value(s)"],
                 'position': 2,
                 'variation': False,
                 'visible': True})

	if product["mood_value(s)"] != None:
		attribute_list.append({'id': 4,
                 'name': 'Mood',
                 'options': product["mood_value(s)"],
                 'position': 5,
                 'variation': False,
                 'visible': True})

	if product["tempo_value(s)"] != None:
		attribute_list.append({'id': 5,
                 'name': 'Tempo',
                 'options': product["tempo_value(s)"],
                 'position': 8,
                 'variation': False,
                 'visible': True})

	if product["genre_value(s)"] != None:
		attribute_list.append({'id': 6,
                 'name': 'Genre',
                 'options': product["genre_value(s)"],
                 'position': 3,
                 'variation': False,
                 'visible': True})

	# if product["price_value(s)"] != None:
	# 	attribute_list.append({'id': 7,
 #                 'name': 'Price',
 #                 'options': product["price_value(s)"],
 #                 'position': 6,
 #                 'variation': False,
 #                 'visible': True})

	if product["instrument_value(s)"] != None:
		attribute_list.append({'id': 8,
                 'name': 'Instrument',
                 'options': product["instrument_value(s)"],
                 'position': 4,
                 'variation': False,
                 'visible': True})

	if product["purpose_value(s)"] != None:
		attribute_list.append({'id': 9,
                 'name': 'Purpose',
                 'options': product["purpose_value(s)"],
                 'position': 7,
                 'variation': False,
                 'visible': True})



	product_to_upload["attributes"] = attribute_list	
	product_to_upload["catalog_visibility"] =  'visible'
	product_to_upload['sold_individually']: True


	product_to_upload["on_sale"] = True

	categorie_list = []
	if "sections" in product["categories"].lower():
		categorie_list.append({'id': 232})
	elif "stems" in product["categories"].lower():
		categorie_list.append({'id': 28})
	if "bundle" in product["categories"].lower():
		categorie_list.append({'id': 27})
	if "only" in product["categories"].lower():
		categorie_list.append({'id': 26})


	product_to_upload["categories"] =  categorie_list

	meta_data = []
	date_created = ""
	short_description_list = []
	for img_mp3 in image_mp3_id_list:
		try:
			if 'image_meta' in img_mp3['metadata']:
				if img_mp3['metadata']['file'][-3:] == "jpg":
					if "/" + product_to_upload["name"].replace(" ", "-").replace("'", "") + "-mp3-image" in img_mp3['metadata']['file']: 
						image_list =[]
						image_list.append({"id": img_mp3['id']})
						product_to_upload["images"] = image_list
		except:
			e = sys.exc_info()[0]
			print( "Error: %s" % e )

		try:
			if "dataformat" in img_mp3['metadata']:
				if img_mp3['metadata']['dataformat'][-3:] == "mp3":
					if product_to_upload["name"] == img_mp3['title'] or product_to_upload["name"] == img_mp3['title'].partition("-")[0].strip():
						if "-" not in img_mp3['title']:
							#base track 
							waveplayer = '[waveplayer ids='+str(img_mp3['id'])+']'
							# short_description_list.append([waveplayer, img_mp3['metadata']['title'], img_mp3['id']])
							meta_data.append({'key': 'player', 'value': waveplayer})
							meta_data.append({'key': '_player', 'value': 'field_5ee8e63ca6bcc'})
							date_created = img_mp3["date_created"]
							# product_to_upload['meta_data'] = [{'key': 'player', 'value': waveplayer}, {'key': '_player', 'value': 'field_5ee8e63ca6bcc'}]				
						else:
							#Stems
							waveplayer = '[waveplayer skin="play_n_wave" ids='+str(img_mp3['id'])+']'
							short_description_list.append([waveplayer, img_mp3['metadata']['title'], img_mp3['id']])
		except:
			e = sys.exc_info()[0]
			print( "Error: %s" % e )

	meta_data.append({'key': 'mins', 'value': product['mins_value(s)']})
	meta_data.append({'key': '_mins', 'value': 'field_5f047e0ec0454'})

	meta_data.append({'key': 'bpm', 'value': product['bpm_value(s)']})
	meta_data.append({'key': '_bpm', 'value': 'field_5f047e21af18b'})
	
	meta_data.append({'key': 'instrument', 'value': join_try_except(product['instrument_value(s)'])})
	meta_data.append({'key': '_instrument', 'value': 'field_5f047e3071ad9'})

	meta_data.append({'key': 'mood', 'value': join_try_except(product['mood_value(s)'])})
	meta_data.append({'key': '_mood', 'value': 'field_5f047e3f75cf6'})

	meta_data.append({'key': 'genre', 'value': join_try_except(product['genre_value(s)'])})
	meta_data.append({'key': '_genre', 'value': 'field_5f047e4dc9e74'})

	meta_data.append({'key': 'platform', 'value': product['platform']})
	meta_data.append({'key': '_platform', 'value': 'field_5f047e57697e5'})

	meta_data.append({'key': 'purpose', 'value': join_try_except(product['purpose_value(s)'])})
	meta_data.append({'key': '_purpose', 'value': 'field_5f047e64b7c9d'})

	meta_data.append({'key': 'tempo', 'value': product['tempo_value(s)']})
	meta_data.append({'key': '_tempo', 'value': 'field_5f047e7625b44'})
	
	meta_data.append({'key': 'product_type', 'value': product['categories']})
	meta_data.append({'key': '_product_type', 'value': 'field_5f047e82b2879'})
	
	meta_data.append({'key': 'watermarkmp3', 'value': product['watermark_url']})
	
	meta_data.append({
                'key': '_preview_files',
                'value': {"": {'file': '/wp-content/uploads/'+date_created+'/'+ product["name"].replace(" ", "-").replace("'", "") + '.mp3', 'name': product["name"]}}})


	product_to_upload['meta_data'] = meta_data 



	for track_or_stem in short_description_list:
		if "-" not in track_or_stem[1]:
			track_or_stem[0] = '[waveplayer skin="w2-legacy" ids='+str(track_or_stem[2])+']'
			main_track = track_or_stem
			short_description_list.remove(track_or_stem)
			short_description_list.insert(0,main_track) 
	
	short_description = ""
	for waveplayer in short_description_list:
		short_description = short_description +waveplayer[1]+ "\n"+ waveplayer[0] + "\n"
	
	product_to_upload["short_description"] = short_description

	
	print("Uploading " + product_to_upload["name"])
	return wcapi.post("products", product_to_upload).json()["id"]

def upload_variation(variation, parent_id):
	variation_to_upload = {
  	'purchasable': True,
	'status': 'publish',
  	'stock_quantity': None,
  	'stock_status': 'instock',
 	'tax_class': '',
  	'tax_status': 'taxable',
  	'virtual': True,
	'downloadable': True,
	}

	variation_to_upload["downloads"] = [{'file': variation['download_1_url'], 'name': variation['download_1_name'][:-4]}]

	attribute_list = []
	if variation["choose_value(s)"] != None:
		attribute_list.append({'id': 3,
                 'name': 'Choose',
                 'option': variation["choose_value(s)"],
                 'position': 0,
                 'variation': True,
                 'visible': True})

	if variation["mins_value(s)"] != None:
		attribute_list.append({'id': 2,
                 'name': 'Mins',
                 'options': variation["mins_value(s)"],
                 'position': 1,
                 'variation': False,
                 'visible': True})

	if variation["bpm_value(s)"] != None:
		attribute_list.append({'id': 1,
                 'name': 'BPM',
                 'options': variation["bpm_value(s)"],
                 'position': 2,
                 'variation': False,
                 'visible': True})

	if variation["mood_value(s)"] != None:
		attribute_list.append({'id': 4,
                 'name': 'Mood',
                 'options': variation["mood_value(s)"],
                 'position': 5,
                 'variation': False,
                 'visible': True})

	if variation["tempo_value(s)"] != None:
		attribute_list.append({'id': 5,
                 'name': 'Tempo',
                 'options': variation["tempo_value(s)"],
                 'position': 8,
                 'variation': False,
                 'visible': True})

	if variation["genre_value(s)"] != None:
		attribute_list.append({'id': 6,
                 'name': 'Genre',
                 'options': variation["genre_value(s)"],
                 'position': 3,
                 'variation': False,
                 'visible': True})

	# if variation["price_value(s)"] != None:
	# 	attribute_list.append({'id': 7,
 #                 'name': 'Price',
 #                 'options': variation["price_value(s)"],
 #                 'position': 6,
 #                 'variation': False,
 #                 'visible': True})

	if variation["instrument_value(s)"] != None:
		attribute_list.append({'id': 8,
                 'name': 'Instrument',
                 'options': variation["instrument_value(s)"],
                 'position': 4,
                 'variation': False,
                 'visible': True})

	if variation["purpose_value(s)"] != None:
		attribute_list.append({'id': 9,
                 'name': 'Purpose',
                 'options': variation["purpose_value(s)"],
                 'position': 7,
                 'variation': False,
                 'visible': True})

	variation_to_upload["attributes"] = attribute_list	
	variation_to_upload["name"] = variation["name"]
	variation_to_upload["regular_price"] = str(variation["regular_price"])


	# pprint.pprint(variation)
	# print("-----------------")
	wcapi.post("products/"+str(parent_id)+"/variations", variation_to_upload).json()
	# pprint.pprint(wcapi.post("products/"+str(parent_id)+"/variations", variation_to_upload).json())

# pprint.pprint(wcapi.post("products", product).json())


def upload(image_mp3_id_list, products):
	c = 0
	for product in products:
		for product_varation in product:
			if "product" in product_varation[0].lower():
				parent_id = upload_product(product_varation[1], image_mp3_id_list, c)
			elif "variation" in product_varation[0].lower():	
				upload_variation(product_varation[1], parent_id)
			c = c +1

# image_mp3_id_list = upload_all_to_media("mp3_128kbps","cropped_artwork", "cropped_")


# pprint.pprint(image_mp3_id_list)
# image_mp3_id_list = []
# upload(image_mp3_id_list, products)

# pprint.pprint(wcapi.post("products/"+str(1104)+"/variations", variation2).json())

