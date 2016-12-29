#!/usr/bin/python3
"""
This module runs ocrmypdf for all pdfs in the currend folder.
"""

import logging
import argparse
import os
import subprocess

# Set default language
LANGUAGE = "deu"

def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    logging.basicConfig(level=logging.DEBUG)
    args = get_commandline_arguments()
    initialize_logging(args)
    language = args.language
    if not language:
        language = LANGUAGE
    check_dependencies(language)
    logging.info("The language " + language + " will be used for ocr processing")
    # Find all files that end with .pdf
    pdf_files = []
    for root, _, files in os.walk(os.path.dirname(__file__)):
        for f in files:
            if not f.endswith(".pdf"):
                continue
            file_path = os.path.join(root, f)
            logging.debug("PDF File was found: " + file_path)
            pdf_files.append(file_path)

    unprocessed_files = []
    processed_files = []
    for pdf_file in pdf_files:
        pdf_info = subprocess.check_output(["pdfinfo", pdf_file])
        if "ocrmypdf" in str(pdf_info):
            processed_files.append(pdf_file)
        else:
            unprocessed_files.append(pdf_file)

    if processed_files:
        processed_files_str = ""
        for f in processed_files:
            processed_files_str += f + "\n"
        logging.info("The following PDF files where found but where already " +
                     "processed:\n" + processed_files_str)

    for f in unprocessed_files:
        logging.info("Starting ocr for file: " + f)
        try:
            subprocess.run(["ocrmypdf", "-l", language, f, f])
        except OSError:
            logging.error("ocrmypdf could not be executed with the given language " +
                          "please install the language with:\n" +
                          "sudo apt-get install tesseract-ocr-" + language)
            exit(1)
        logging.info("Finished ocr for file: " + f)


def check_dependencies(language):
    """Check whether the used programms are installed
    :returns: None

    """
    try:
	# pipe output to /dev/null for silence
        null = open("/dev/null", "w")
        subprocess.Popen("ocrmypdf", stdout=null, stderr=null)
        null.close()

    except OSError:
        logging.error("ocrmypdf could not be executed, please install it with:\n" +
                      "sudo apt-get install pip3\n" +
                      "sudo apt-get install libffi-dev\n" +
                      "sudo pip3 install ocrmypdf")
        exit(1)


    try:
	# pipe output to /dev/null for silence
        null = open("/dev/null", "w")
        subprocess.Popen("pdfinfo", stdout=null, stderr=null)
        null.close()

    except OSError:
        logging.error("pdfinfo could not be executed, please install the language with:\n" +
                      "sudo apt-get install poppler-utils")
        exit(1)

def get_commandline_arguments():
    """ Commandline argument parser for this module
    :returns: namespace with parsed arguments

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--language", help="language of the document, is" +
                        "used to enhance ocr results, it should be a Teseract " +
                        "language that is installed on the system defaults to: "
                        + LANGUAGE)
    parser.add_argument("--logfile", help="path to a file the output is passed to")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
    group.add_argument("-q", "--quiet", help="no output except errors", action="store_true")
    args = parser.parse_args()
    return args

def initialize_logging(commandline_args):
    """Initialize logging as given in the commandline arguments
    :returns: None

    """
    loglevel = "INFO"
    if commandline_args.verbosity:
        loglevel = "DEBUG"
    if commandline_args.quiet:
        loglevel = "ERROR"


    logfile = commandline_args.logfile

    # If logfile is given, generate a new logger with file handling
    if logfile:
        filehandler = logging.FileHandler(logfile, 'a')
        formatter = logging.Formatter()
        filehandler.setFormatter(formatter)
        logger = logging.getLogger()
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.addHandler(filehandler)

    loglevel = getattr(logging, loglevel.upper())
    logging.getLogger().setLevel(loglevel)

if __name__ == "__main__":
    main()
