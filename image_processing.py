from PIL import Image

im = Image.open("C:\Users\Matt\Documents\GitHub\ledmatrix\icons\moma_emoji.jpg")
pix = im.load()

w, h = im.size

y = 564
x_step = 5
y_step = 5

color = (0, 0, 0)

for x in range(w):
  for y in range(h):

    if x / x_step % 4 == 0 and y / y_step % 4 == 0:
      color = (255, 0, 0)
    else:
      color = (0, 0, 0)

    if x % x_step == 0 and y % y_step == 0:
      pix[x, y] = color


im.save("test.bmp")
