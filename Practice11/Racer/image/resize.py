from PIL import Image

# open the image
image = Image.open('kedergi.png')

# set new size (width, height)
new_size = (50,100)

# change the image size 
resized_image = image.resize(new_size, Image.BICUBIC)

# saving the new image with the new name
resized_image.save('up_kedergi.png')

print("The image size changed successfully!")