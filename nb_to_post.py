#!/usr/bin/env python3.6

import argparse
import os

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('post_dir', type=str,
		help='source directory containing post notebook and images')

	args = parser.parse_args()
	return args
	
if __name__ == '__main__':

	args = parse_args()
	
	for filename in os.listdir(args.post_dir):
		if filename=='images':
			img_folder = os.listdir(os.path.join(args.post_dir, 'images'))[0]
			remove_old = f"rm -r {os.path.join('images', img_folder)}"
			print(remove_old)
			os.system(remove_old)

			copy_imgs = (f"cp -r {os.path.join(args.post_dir, 'images', img_folder)} {os.path.join('images', img_folder)}")
			print(copy_imgs)
			os.system(copy_imgs)

		name, ext = os.path.splitext(filename)

		if ext == '.ipynb':
			convert = f"jupyter nbconvert {os.path.join(args.post_dir, filename)} --to markdown --output-dir {'_posts'}"
			print(convert)
			os.system(convert)

			md_file = f"{os.path.join('_posts', name)}.md"	
			with open(md_file) as f:
				content = f.read()

			content = content.strip()

			with open(md_file, 'w') as f:
				f.write(content)




