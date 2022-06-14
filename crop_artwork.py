from PIL import Image
import os


#the name of the directory the original images are in 
# artwork_directory = "artwork"

#the directory the cropped images will be stored in
# dst_filename = "cropped_artwork"
 
#cropped image size
# size = 320, 320

#cropped image quality
# quality = 80

#what will be added to the begining of the filename for the cropped images
# cropped_file_prefix = "cropped_"


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def crop_artwork(artwork_directory, dst_filename, size, quality, cropped_file_prefix):
	#takes a destination filename where cropped images will be stored and a size for the cropped images to be
	if os.path.isdir(dst_filename) == False:
		os.mkdir(dst_filename + '/')

	for artwork in os.listdir(artwork_directory):
		if artwork not in os.listdir(dst_filename):
			if cropped_file_prefix not in artwork: 
				if artwork[-3:] == "png" or artwork[-3:] == "jpg": 
					img = Image.open(artwork_directory+"/"+artwork)
			
					img = crop_max_square(img)
					img.thumbnail(size, Image.ANTIALIAS)
			
					if artwork[-3:] == "png":
						rgb_img = img.convert('RGB')
						rgb_img.save(dst_filename + "/" + cropped_file_prefix + artwork.replace("png","jpg"), quality = quality)
					else:
						img.save(dst_filename+"/"+ cropped_file_prefix + artwork, quality = quality)
