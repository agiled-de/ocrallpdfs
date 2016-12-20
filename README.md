# ocrallpdfs

This is a small script that uses ocrmypdf on pdfs in the current folder and all its subfolders. It uses pdfinfo to check whether a pdf has already been processed, so you can run it multiple times on the same file and it will scan the image only once.

## Dependecies

You have to install ocrmypdf and the language packs of tesseract that you want to use. The script will check if the dependecies are met when you start it and give instructions on how to install unmet dependencies.

## Start the script

```
ocrallpdfs.py --help
```
