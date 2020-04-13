# Smart PDF

Smart PDF helps in merging pdf files together and also helps in adding watermark to pdf files

```
$ python smart-pdf.py --help
usage: smart-pdf.py [-h] [-f  [...]] [-d DIRECTORY] [-n NAME] [-w WATERMARK]
                    [-p PDFNAME]

optional arguments:
  -h, --help            show this help message and exit
  -f  [ ...], --files  [ ...]
                        list of pdf files comma seperated
  -d DIRECTORY, --directory DIRECTORY
                        source directory name
  -n NAME, --name NAME  name of the merged pdf file
  -w WATERMARK, --watermark WATERMARK
                        watermarking pdf file
  -p PDFNAME, --pdfname PDFNAME
                        pdf file to be watermarked
```

## Merge PDF
There are two options provided when it comes to merging pdf files together:
1) We can add files one by one 
2) Point out a directory where all pdf files are located

```
$ python smart-pdf.py -f one_page.pdf two_page.pdf -n files_merged.pdf
Created PDF: files_merged.pdf
```
```
$ python smart-pdf.py -d pdf_directory -n directory_merged.pdf
Created PDF: pdf_directory/directory_merged.pdf
```

## Watermark PDF
To watermark a pdf, we need a watermark in form of pdf. Following option shows how we can achieve this
```
$ python smart-pdf.py -p files_merged.pdf -w watermark.pdf -n marked.pdf
Created PDF: marked.pdf
```
```
$ python smart-pdf.py -p files_merged.pdf -w watermark.pdf
Created PDF: watermarked.pdf
```
I have added two options here, either we can add a name for the final watermarked file using `-n <name>` or just not add
`-n` option and let the program choose the name


```
Maintainer: Nikhil Narayanan [nikhilvkn@yahoo.com]
```
