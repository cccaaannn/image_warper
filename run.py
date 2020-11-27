import os
import argparse
from image_warper import image_warper

def dims(d):
    try:
        w, h = map(int, d.split(','))
        return w, h
    except:
        raise argparse.ArgumentTypeError("window dimensions has to be in this format int,int")

def path(p):
    if(os.path.exists(p)):
        return p
    else:
        raise argparse.ArgumentTypeError("path does not exists")

parser = argparse.ArgumentParser(description='List the content of a folder')

# Add the arguments
parser.add_argument('--image_path', dest="image_path", type=path, help='path of the image', required=True)
parser.add_argument('--save_folder', dest="save_folder", metavar='save_folder', type=path, help='path of the output folder', default="out")
parser.add_argument('-d', dest="d", action='store', type=dims, help='window dimensions w,h', default=(1200, 700))

args = parser.parse_args()

image_path = args.image_path
save_folder = args.save_folder
w = args.d[0]
h = args.d[1]


warper = image_warper(image_path, save_folder=save_folder, windows_size=(w,h))
warper.start_warper()
