# This file serves as a template for adding repositories to grabseqs.

import requests, argparse, sys, os, time, json, glob
from subprocess import call

from grabseqslib.utils import check_existing, fetch_file

def add_XYZ_subparser(subparser):
	"""
	Function to add a subparser for XYZ repository.
	"""

	### Base args: should be in every
	parser_XYZ = subparser.add_parser('XYZ', help="download from XYZ")
	parser_XYZ.add_argument('XYZid', type=str, nargs='+', 
				help="One or more XYZ project or sample identifiers (EXAMPLE####)")

	parser_XYZ.add_argument('-o', dest="outdir", type=str, default="",
				help="directory in which to save output. created if it doesn't exist")
	parser_XYZ.add_argument('-r',dest="retries", type=int, default=0,
				help="number of times to retry download")
	parser_XYZ.add_argument('-t',dest="threads", type=int, default=1,
				help="threads to use (for pigz)")

	parser_XYZ.add_argument('-f', dest="force", action="store_true",
				help = "force re-download of files")
	parser_XYZ.add_argument('-l', dest="list", action="store_true",
				help="list (but do not download) samples to be grabbed")

	### OPTIONAL: Use if metadata are available
	parser_XYZ.add_argument('-m', dest="metadata", action="store_true",
				help="save metadata")

	### Add any repository-specific arguments here

def get_XYZ_acc_metadata(pacc, save = False, loc = ''):
	"""
	Function to get list of XYZ sample accession numbers from a particular 
	project. Takes project accession number `pacc` and returns a list of XYZ
	accession numbers. Optional arguments to `save` metadata .csv in a specified
	`loc`ation.
	"""

	sample_list = []
	# Search for project or sample information and metadata (if available)

	if save:
		# Save metadata in `loc`

	# LISTING OPTION 1: If user would like to list the available samples (-l) and
	# this information is available, i.e. from a metadata table, this can
	# be tested for here (and then return an empty list to prevent downstream
	# processing). For an example of this, see the sra.py module

	return sample_list

def download_XYZ_sample(acc, retries = 0, threads = 1, loc='', force=False, list_only=False):
	"""
	Helper function to download sequences given an XYZ `acc`ession,
	with support for a particular number of `retries`. Can use multiple
	`threads` with pigz (if data are not already compressed on arrival).
	"""

	# LISTING OPTION 2: If the information about whether samples are paired or
	# unpaired is only available from a sample-specific page, it usually makes more
	# sense to look that up here, and then just skip the downloading part. For an
	# example of this, see the mg-rast.py module

	# Make sure to check that the sample isn't already downloaded
	if not force:
		found = check_existing(loc, acc)
		if found != False:
			print("found existing file matching acc:" + acc + ", skipping download. Pass -f to force download")
			return False

	# Need to know this
	paired = True

	# Generally, unless there's a tool like fasterq-dump that downloads both reads,
	# it's just easier to iterate through file paths (i.e. either one unpaired, or
	# two paired).
	seq_urls = []
	file_paths = build_paths(acc, loc, paired) #see utils.py for details

	for i in range(len(seq_urls)):
		print("Downloading accession "+acc+" from XYZ repository")
		# fetch_file should work for most things where a URL is available
		retcode = fetch_file(seq_urls[i],file_paths[i],retries)

		# There are a number of things you may want to do here: check and handle
		# downloaded file integrity, convert to .fastq (see mgrast.py for an example
		# of a scenario dealing with .fastx in general), retries, etc.

		print("Compressing .fastq")
		rzip = call(["pigz -f -p "+ str(threads) + ' ' + file_paths[i]], shell=True)

	return True