#! /usr/bin/env python

__author__ = 'Josef Ludvicek <josef.ludvicek.cz@gmail.com>'

from datetime import datetime
from os import listdir
from os import rename
from os.path import isfile, join
import sys

# requires library exifread
# see https://github.com/ianare/exif-py
import exifread

# path where to rename files
BASE_DIR = ''

# list supported extensions, where exif data can be obtained
# other file types will be ignored
EXTENSIONS = ('jpg',)

EXIF_TIMESTAMP_FORMAT = '%Y:%m:%d %H:%M:%S'
FILESYSTEM_TIMESTAMP_FORMAT = '%Y-%m-%d_%H-%M-%S'


def get_exif_timestamp(file_path):
    """
    Fetch EXIF created timestamp from photo.

    :param file_path: path to file with EXIF data
    :return: timestamp string formated with FILESYSTEM_TIMESTAMP_FORMAT or None if sth fails
    """
    try:
        # fetch timestamp and close file
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
            # Return Exif tags
            timestamp = tags.get('EXIF DateTimeOriginal', None)

        timestamp = datetime.strptime(str(timestamp), EXIF_TIMESTAMP_FORMAT)
        return timestamp.strftime(FILESYSTEM_TIMESTAMP_FORMAT)

    except Exception, e:
        print "failed to fetch EXIF DateTime from %s" % file_path
        print e
        return None


if len(sys.argv) < 2:
    print "Usage: exif_timestamp.py <path to base dir>"
    sys.exit(1)

BASE_DIR = sys.argv[1]
print "Renaming files with extensions %s in dir %s " % (EXTENSIONS, BASE_DIR)

# non-recursive list files in dir
file_names = [f for f in listdir(BASE_DIR) if isfile(join(BASE_DIR, f))]
if len(file_names) == 0:
    print "No files found in %s" % BASE_DIR

for file_name in file_names:
    path = "%s/%s" % (BASE_DIR, file_name)
    new_name = None

    # skip unsupported file types
    extension = file_name.split('.')[1]
    extension = extension.lower()
    if extension not in EXTENSIONS:
        print "skipping file %s" % file_name
        continue

    # fetch created timestamp from EXIF data
    new_name = get_exif_timestamp(path)

    if new_name:
        # prefix original file name with timestamp from EXIF data
        new_path = "%s/%s_%s" % (BASE_DIR, new_name, file_name)
        print "%s == > %s" % (path, new_path)
        rename(path, new_path)

    else:
        print "** timestamp not found for %s" % file_name
