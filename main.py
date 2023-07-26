from image_to_ascii import convert_image_to_text
from ascii_to_image import generate_image

original = input("Path to the original image: ")
new_pixel_width = input("Pixel width of the ASCII image: ")
font_size = int(input("Font size: "))
invert = input("Invert the background, default - black (y/n): ")

invert = True if invert == "y" else False
if new_pixel_width == "keep":
    convert_image_to_text(original, font_size, inverted=invert)
else:
    convert_image_to_text(original, font_size, int(new_pixel_width), inverted=invert)
generate_image(font_size)
