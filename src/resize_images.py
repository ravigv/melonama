import os
import glob
from tqdm import tqdm
from PIL import Image
from joblib import Parallel, delayed
import argparse
# to run simply run the command `python resize_images.py`

def resize_and_save(path, output_path, sz: tuple):
    fn = os.path.basename(path)  
    im = Image.open(path)
    im = im.resize(sz, resample=Image.BILINEAR)
    im.save(os.path.join(output_path, fn))


def resize_and_mantain(path, output_path, sz: tuple):
    # from research paper `https://isic-challenge-stade.s3.amazonaws.com/9e2e7c9c-480c-48dc-a452-c1dd577cc2b2/ISIC2019-paper-0816.pdf?AWSAccessKeyId=AKIA2FPBP3II4S6KTWEU&Signature=nQCPd%2F88z0rftMkXdxYG97Nau4Y%3D&Expires=1592222403`
    fn = os.path.basename(path)  
    img = Image.open(path)
    size = min(600, sz[0])  
    old_size = img.size
    ratio = float(size)/max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])
    img = img.resize(new_size, resample=Image.BILINEAR)
    img.save(os.path.join(output_path, fn))


if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_folder", 
        default=None, 
        type=str, 
        required=True, 
        help="Input folder where images exist."
    )
    parser.add_argument(
        "--output_folder", 
        default=None, 
        type=str, 
        required=True, 
        help="Output folder for images."
    )
    parser.add_argument(
        "--mantain_aspect_ratio", 
        default=True, 
        type=bool, 
        required=True, 
        help="Whether to mantain aspect ratio of images."
    )
    args = parser.parse_args()
    images = glob.glob(os.path.join(args.input_folder, '*.jpg'))
    if not args.mantain_aspect_ratio:
        Parallel(n_jobs=16)(
            delayed(resize_and_save)(i, args.output_folder, (224, 224)) for i in tqdm(images))
    else:
        Parallel(n_jobs=16)(
            delayed(resize_and_mantain)(i, args.output_folder, (600, 600)) for i in tqdm(images))