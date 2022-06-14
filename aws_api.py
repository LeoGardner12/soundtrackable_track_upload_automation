import boto3
import urllib
import moto
import os

from botocore.client import Config
ACCESS_KEY_ID = 'Removed for security'
ACCESS_SECRET_KEY = 'Removed for security'
bucket_name = "Removed for security"

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)

# for my_bucket_object in s3.Bucket(bucket_name).objects.all():
#     print(my_bucket_object)

def upload_to_aws(src_directory, bucket_name, url_txt):
	#uploads all zip files in a directory to aws bucket and returns a list of all uploaded product urls
	# f = open(url_txt, "w+")
	# f.close()
	url_list = []
	for filename in os.listdir(src_directory):
		filename_and_url=[]
		if filename[-3:] == "zip" or filename[-3:] == "mp3":
			already_uploaded = False
			for my_bucket_object in s3.Bucket(bucket_name).objects.all():
				if filename == my_bucket_object.key:
					print(filename+" Is already in aws bucket")
					already_uploaded = True
					break
			if already_uploaded == False:
				print("Uploading: "+filename+" to AWS")
				data = open(src_directory + "/" + filename, 'rb')
				s3.Bucket(bucket_name).put_object(Key=filename, Body=data)
	
				object_acl = s3.ObjectAcl(bucket_name, filename)
				response = object_acl.put(ACL='public-read')
	
				location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)['LocationConstraint']
				url = "https://%s.s3.%s.amazonaws.com/%s" % (bucket_name,location, filename.replace(" ", "+"))
				filename_and_url.append(filename)
				filename_and_url.append(url)
				url_list.append(filename_and_url)
				print(filename_and_url)
				f=open(url_txt, "a+")
				f.write(", ".join(filename_and_url))
				f.write("\n")
				f.close()
	return url_list

def read_url_txt(filename):
	f = open(filename, "r")
	url_list = []
	for title_url in f:
		url_list.append(title_url.split(", "))
	f.close()
	return url_list
		


# upload_to_aws("result/", bucket_name)

