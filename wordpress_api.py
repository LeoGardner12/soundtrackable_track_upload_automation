import os
import requests

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import mimetypes 
from woocommerce import API
import pprint
import eyed3

wcapi = API(
url = "Removed for security",
consumer_key="Removed for security",
consumer_secret="Removed for security",
version="wc/v3"
)

def upload_to_media(filename_path, data, client):
	# with open(filename_path, 'rb') as img:
	#     data['bits'] = xmlrpc_client.Binary(img.read())

	f = open(filename_path, 'rb')
	data['bits'] = xmlrpc_client.Binary(f.read())
	print(data)
	response = client.call(media.UploadFile(data))
	f.close() 

	attachment_id = response
	
	return attachment_id

def upload_all_to_media(src_track_directory, cropped_directory_name, cropped_file_prefix):

	client = Client('Removed for security','Removed for security', 'Removed for security')

# # # set to the path to your file
	response_list = []
	for filename in os.listdir(src_track_directory):

		filename_path = src_track_directory + "/" + filename
		print("Uploading " + filename_path + " To media")

		# prepare metadata
		data = {
			'name': filename
		}
		data['type'] = mimetypes.read_mime_types(filename) or mimetypes.guess_type(filename)[0]


		response = upload_to_media(filename_path, data, client)

		response_list.append([response["title"],response["attachment_id"], response["url"]])
	return response_list

response_list = upload_all_to_media("mp3_128kbps","cropped_artwork", "cropped_")
print(response_list)

def upload_product(product):
	product_to_upload = {}
	product_to_upload["name"] = product["name"]
	product_to_upload["type"] = product["type"].lower()
	product_to_upload["categories"] = [{'id': 26, 'name': 'Track Only', 'slug': 'trackonly'}]
	product_to_upload["catalog_visibility"] =  'visible'
	attribute_list = []
	product_to_upload["virtual"] = True
	product_to_upload["downloadable"] = True
	product_to_upload["downloads"] = [{'file':  product["download_1_url"], 'name': product["name"]}]
	# product_to_upload["mood"] = product[0][1]["mood"]
	product_to_upload["genre"] = product["genre"]
	product_to_upload["variations"] = [1087, 1090, 1091]
	# for media in media_response_list:
	# 	if media[0] == product_to_upload["name"].strip().replace(" ", "-")+".mp3":
	# 		print()
	product_to_upload['meta_data'] = [
              {'id': 8163,
               'key': 'player',
               'value': '[waveplayer ids="285"]'},
              {'id': 8164, 'key': '_player', 'value': 'field_5ee8e63ca6bcc'},
              {'id': 8165, 'key': 'price', 'value': ''},
              {'id': 8167, 'key': '_et_pb_post_hide_nav', 'value': 'default'},
              {'id': 8168,
               'key': '_et_pb_page_layout',
               'value': 'et_right_sidebar'},
              {'id': 8169, 'key': '_et_pb_side_nav', 'value': 'off'},
              {'id': 8170, 'key': '_et_pb_use_builder', 'value': 'on'},
              {'id': 8171, 'key': '_et_pb_first_image', 'value': ''},
              {'id': 8172, 'key': '_et_pb_truncate_post', 'value': ''},
              {'id': 8173, 'key': '_et_pb_truncate_post_date', 'value': ''},
              {'id': 8174,
               'key': '_et_pb_product_page_layout',
               'value': 'et_build_from_scratch'},
              {'id': 8175, 'key': '_et_pb_old_content', 'value': ''}]
	if product["attribute_1_name"] != None:
		attribute_list.append({'id': 3,
	                 'name': product['attribute_1_name'],
	                 'options':  product['attribute_1_value(s)'],
	                 'position': 0,
	                 'variation': False,
	                 'visible': True})
	if product["attribute_2_name"] != None:
		attribute_list.append({'id': 2,
	                 'name': product['attribute_2_name'],
	                 'options':  product['attribute_2_value(s)'],
	                 'position': 0,
	                 'variation': False,
	                 'visible': True})
	if product["attribute_3_name"] != None:
		attribute_list.append({'id': 1,
	                 'name': product['attribute_3_name'],
	                 'options':  product['attribute_3_value(s)'],
	                 'position': 0,
	                 'variation': False,
	                 'visible': True})
	product_to_upload["attributes"] = attribute_list	

	return wcapi.post("products", product_to_upload).json()

def upload_variaiton(product_variation, parent_id):
	attribute_list = []

	print(product_variation)
	if product_variation["attribute_1_name"] != None:
		attribute_list.append({'id': 3,
	                 'name': product_variation['attribute_1_name'],
	                 'option':  product_variation['attribute_1_value(s)']})
	if product_variation["attribute_2_name"] != None:
		attribute_list.append({'id': 2,
	                 'name': product_variation['attribute_2_name'],
	                 'option':  product_variation['attribute_2_value(s)']})
	if product_variation["attribute_3_name"] != None:
		attribute_list.append({'id': 1,
	                 'name': product_variation['attribute_3_name'],
	                 'option':  product_variation['attribute_3_value(s)']})

