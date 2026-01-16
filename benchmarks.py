import timeit
from typing import Callable
from common.typing import Color, Image
from core.visuals import IMG_SUN

def draw_box_v0(x1, y1, x2, y2, color: Color) -> None:
    v = 0
    for y in range(y1, y2):
        for x in range(x1, x2):
            v += (x + y + color.r + color.g + color.b)

def draw_box_v1(x1, y1, x2, y2, color: Color) -> None:
    v = 0
    r, g, b = color.r, color.g, color.b
    for y in range(y1, y2):
        for x in range(x1, x2):
            v += (x + y + r + g + b)

def draw_image_v0(image: Image, start_x, start_y) -> None:
    v = 0
    for line_iteration, line in enumerate(image):
        for pixel_iteration, pixel in enumerate(line):
            if pixel.on:
                if pixel.color:
                    v += (start_x + pixel_iteration + start_y + line_iteration + pixel.color.r + pixel.color.g + pixel.color.b)
                else:
                    v += (start_x + pixel_iteration + start_y + line_iteration + 255 + 255 + 255)
            else:
                continue

def draw_image_v1(image: Image, start_x, start_y) -> None:
    v = 0
    for y in range(len(image)): # y = line_iteration
        line = image[y]
        pixel_y = start_y + y
        
        for x in range(len(line)): # x = pixel_iteration
            pixel = line[x]
            if not pixel.on:
                continue
            
            pixel_x = start_x + x
            c = pixel.color
            if c:
                v += (start_x + pixel_x + start_y + pixel_y + c.r + c.g + c.b)
            else:
                continue

if __name__ == "__main__":
    test1: Callable = draw_image_v0
    test2: Callable = draw_image_v1
    
    test1_res = timeit.timeit(lambda: test1(IMG_SUN, 1, 1), number=100000)
    test2_res = timeit.timeit(lambda: test2(IMG_SUN, 1, 1), number=100000)
    
    print(f"Test 1 Result:\t{round(test1_res, 5)}s\nTest 2 Result:\t{round(test2_res, 5)}s\nChange from Test 1 to 2: {round((test1_res / test2_res) * 100, 3)}%")