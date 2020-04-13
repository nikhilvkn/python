import argparse
import PyPDF2
import sys
import os


def merge_from_directory(directory, name):
	# Function to merge pdf files in a directory
	# To run this program, given directory and program.py,
	# must be in the same location
	merger = PyPDF2.PdfFileMerger()
	pdf_files = [pdf for pdf in os.listdir(directory) if pdf.endswith(".pdf")]
	for pdf in pdf_files:
		merger.append(pdf)
	merger.write(os.path.join(directory, name))
	print(f'Created PDF: {os.path.join(directory, name)}')


def merge_given_pdf(data, name):
	# Function to merge pdf given as a list
	# Inorder to run this function, it is mandatory that,
	# program.py and pdf files be in the same location
	merger = PyPDF2.PdfFileMerger()
	for pdf in data:
		merger.append(pdf)
	merger.write(name)
	print(f'Created PDF: {name}')


def watermark(source_pdf, watermark_pdf, name='watermarked.pdf'):
	# Function does watermarking a pdf with watermark pdf
	# Both the pdf and program.py be in the same location	
	pdf_name = PyPDF2.PdfFileReader(open(source_pdf, 'rb'))
	template_pdf = PyPDF2.PdfFileReader(open(watermark_pdf, 'rb'))

	watermark_result = PyPDF2.PdfFileWriter()

	for pages in range(pdf_name.getNumPages()):
		page = pdf_name.getPage(pages)
		page.mergePage(template_pdf.getPage(0))
		watermark_result.addPage(page)

	with open(name, 'wb') as pdf_file:
		watermark_result.write(pdf_file)
	print(f'Created PDF: {name}')
				 

def main():
	'''Program to merge PDF'''

	try:
		parse = argparse.ArgumentParser()
		parse.add_argument('-f','--files', nargs='+', help='list of pdf files comma seperated', metavar='')
		parse.add_argument('-d','--directory', help='source directory name')
		parse.add_argument('-n','--name', help='name of the merged pdf file')
		parse.add_argument('-w','--watermark', help='watermarking pdf file')
		parse.add_argument('-p','--pdfname', help='pdf file to be watermarked',)
		parse_arguments = parse.parse_args()

		if parse_arguments.files and parse_arguments.name:
			merge_given_pdf(parse_arguments.files, parse_arguments.name)

		elif parse_arguments.directory and parse_arguments.name:
			merge_from_directory(parse_arguments.directory, parse_arguments.name)

		elif parse_arguments.pdfname and parse_arguments.watermark:
			if parse_arguments.name:
				watermark(parse_arguments.pdfname, parse_arguments.watermark, parse_arguments.name)
				return
			watermark(parse_arguments.pdfname, parse_arguments.watermark)
		else:
			print('RuntimeError: -n should be included with -f & -d. Please check help option')

	except FileNotFoundError as e:
		print(e)
	except Exception as exception:
		print(f'Exception: {exception}')

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass