from PIL import Image

im1 = Image.open("v1.png")
im2 = Image.open("v2.png")

im_result = Image.new("RGB", (im1.width, im1.height))

for row in range(im1.width):
	for col in range(im1.height):
		pixel1 = im1.getpixel((row,col))
		pixel2 = im2.getpixel((row,col))

		#print(im_result.getpixel((row,col)))

		if pixel1 != pixel2:
			im_result.putpixel((row,col),pixel1)
		else:
			im_result.putpixel((row,col),(255,0,0,1))
pixel1 = im_result
			
for row in range(im1.width):
	for col in range(im1.height):
		pixel1 = im1.getpixel((row,col))
		pixel2 = im2.getpixel((row,col))

		#print(im_result.getpixel((row,col)))

		if pixel1 != pixel2:
			im_result.putpixel((row,col),pixel1)
		else:
			im_result.putpixel((row,col),(0,0,0,1))


im_result.save("this.png")