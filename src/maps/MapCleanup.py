from PIL import Image

img = Image.open("dirtyMap.png")

pixels = img.load()  # create the pixel maps

print pixels[0, 0]

for i in range(img.size[0]):  # for every pixel:
    for j in range(img.size[1]):
        if pixels[i, j] != (0, 0, 0, 255):  # if not black:
            pixels[i, j] = (255, 255, 255, 255)  # change to white

img.save("maps.png")
