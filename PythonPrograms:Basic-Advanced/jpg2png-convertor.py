from PIL import Image
import argparse
import os


def main():

	parse = argparse.ArgumentParser()
	parse.add_argument('-s','--source', help='source directory name')
	parse.add_argument('-d','--destination', help='destination directory name')
	parse_arguments = parse.parse_args()

	path = os.path.abspath(parse_arguments.source)
	dest_dir = os.path.abspath(parse_arguments.destination)

	if not os.path.exists(dest_dir):
	    os.mkdir(dest_dir)
	    
	if os.path.exists(path):
	    for filename in os.listdir(path):
	        if filename.endswith('.jpg'):
	            image = Image.open(os.path.join(path,filename))
	            data = os.path.splitext(filename)[0]
	            image.save(f'{dest_dir}/{data}.png')
	else:
	    print(f'Directoty {path} does not exists')


if __name__ == '__main__':
	main()
