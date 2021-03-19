# First import wget python module.
import wget, datetime

# Set up the image URL
image_url = "http://192.168.2.203/capture"

# Use wget download method to download specified image url.

image_filename = 'test.jpg'
# time = datetime.datetime.now().time().strftime('%H:%M:%S.%f')
# image_filename = time[:-3] + image_filename
image_filename = wget.download(image_url)

print('Image Successfully Downloaded: ', image_filename)