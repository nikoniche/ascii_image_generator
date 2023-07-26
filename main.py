from image_to_ascii import convert_image_to_text
from ascii_to_image import generate_image

original = input("Path to original image: ")
new_pixel_width = input("Pixel width of the ASCII image: ")
font_size = int(input("Font size: "))

if new_pixel_width == "keep":
    convert_image_to_text(original, font_size)
else:
    convert_image_to_text(original, font_size, int(new_pixel_width))
generate_image(font_size)
