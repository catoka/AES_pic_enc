import math
from PIL import Image

def calculate_entropy(image, size):
    color_counts = {}
    entropy_value = 0
    for i in range(size):
        color = image.getpixel((i % image.width, i // image.width))
        if color not in color_counts:
            color_counts[color] = 1
        else:
            color_counts[color] += 1
    for color in color_counts:
        count = color_counts[color]
        probability = count / size
        entropy_value += probability * math.log(size / count, 2)
    return entropy_value



def get_uaci(image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    result = 0.0
    image1 = image1.convert("L")
    image2 = image2.convert("L")
    bright_sum = 0.0
    for x in range(image1.width):
        for y in range(image1.height):
            bright_sum += abs(image1.getpixel((x, y)) - image2.getpixel((x, y))) / 256
    result = bright_sum / (image1.height * image1.width)
    return result * 100

def get_npcr(image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    result = 0.0
    changed_pixels_count = 0
    for x in range(image1.width):
        for y in range(image1.height):
            if image1.mode == "P":
                if image1.getpixel((x, y)) != image2.getpixel((x, y)):
                    changed_pixels_count += 1
            else:
                if sum(image1.getpixel((x, y))[:2]) / 3 != sum(image2.getpixel((x, y))[:2]) / 3:
                    changed_pixels_count += 1
    result = changed_pixels_count / (image1.height * image1.width)
    return result * 100


def get_avg_brightness(picture_path):
        image = Image.open(picture_path).convert("RGB")
        width = image.size[0]
        height = image.size[1]
        all_pixels_count = width * height
        sum_brightness = 0
        for x in range(0, width):
            for y in range(0, height):
                pixels = image.getpixel((x, y))
                sum_brightness += bright(pixels)
        return sum_brightness / all_pixels_count


def bright(pixels):
    return 0.299 * pixels[0] + 0.587 * pixels[1] + 0.114 * pixels[2]


def get_coff_corelation(picture_path, mode=0):
    image = Image.open(picture_path).convert("RGB")
    width = image.size[0]
    height = image.size[1]
    sum_xy = 0
    D = 0
    avg_brightness = get_avg_brightness(picture_path)
    if mode == 0: 
        end_width = width - 1
        end_height = height
        shamt_x = 1
        shamt_y = 0
    elif mode == 1:
        end_width = width
        end_height = height - 1
        shamt_x = 0
        shamt_y = 1
    else:
        end_width = width - 1
        end_height = height - 1
        shamt_x = 1
        shamt_y = 1
    for x in range(0, end_width):
        for y in range(0, end_height):
            pixels_x = image.getpixel((x, y))
            pixels_y = image.getpixel((x + shamt_x, y + shamt_y))
            pixels_x_brightness = bright(pixels_x)
            pixels_y_brightness = bright(pixels_y)
            sum_xy += (pixels_x_brightness - avg_brightness) * (pixels_y_brightness - avg_brightness)
    for x in range(0, width):
        for y in range(0, height):
            pixels_x = image.getpixel((x, y))
            pixels_x_brightness = bright(pixels_x)
            D += (pixels_x_brightness - avg_brightness) ** 2
    return sum_xy / D
