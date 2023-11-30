from PIL import Image
from pathlib import Path
import os
import numpy as np  
import argparse
import itertools

# TODO: split when there are MORE than one vehicle in one row (e.g., width = 192 * 16)
# TODO: split when there is  LESS than one vehicle in one row (e.g., width = 192 * 4)
# TODO: skip empty tiles
# TODO: remove background color 

def crop(filename, dir_in, dir_out):
    d = 192 # tile dimension
    name, extension = os.path.splitext(filename)
    image = Image.open(os.path.join(dir_in, filename))
    w, h = image.size
    count_vehicle, count_view = 0, 0
    
    grid = itertools.product(range(0, h-h%d, d), range(0, w-w%(d*4), d))
    for i, j in grid:
        box = (j, i, j+d, i+d)
        # out = os.path.join(dir_out, f'{name}_{int(i/d)}_{int(j/d)}{extension}')
        image_cropped = image.crop(box)
        image_cropped_bg_removed = remove_background(image_cropped)
        
        if count_view == 8:
            count_view = 0
            count_vehicle = count_vehicle + 1

        out = os.path.join(dir_out, f'{name}_{count_vehicle}_{count_view}{extension}')
        image_cropped_bg_removed.save(out)
        count_view = count_view + 1

    print('finished processing {}{}'.format(dir_in, filename))
        
        
def remove_background(image):
    d = 192
    image = image.convert('RGBA')
    image_arr = np.array(image) 
    
    for x in range(d):
        for y in range (d):
            if np.array_equal(image_arr[x, y], [231, 255, 255, 255]):
                image_arr[x, y] = [0, 0, 0, 0]
                
    image_bg_removed = Image.fromarray(image_arr) 
    return image_bg_removed

def main(args):
    input_folder_path = args.input_folder_path
    output_folder_path = args.output_folder_path
    filenames = []
    for p in Path('.').glob(f'{input_folder_path}/*.png'):
        filenames += [p.name]        
    
    for filename in filenames:
        crop(filename, f'{input_folder_path}/', f'{output_folder_path}/')

def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_folder_path', type=str, default=".")
    parser.add_argument('--output_folder_path', type=str, default="output")

    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args)