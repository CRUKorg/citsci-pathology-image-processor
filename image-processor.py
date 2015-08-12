__author__ = 'paters01'

import os
from os import listdir
from os.path import isfile, join
import csv
import shutil

# file locations
source_folder = '/data/Trailblazer/lung-all-min/'
target_folder = '/data/Trailblazer/GitHub/lung_mvp01/'
server_folder = '//citscitools.cancerresearchuk.org/static/mvp-images/lung_mvp01/'
file_extn = '.jpg'
metadata_filename = 'lung_mvp01_metadata.csv'

# common data for import
data_owner = ''
stain_type = 'lung'
tumour_type = 'lung'

# this needs to be changed according to data filename format
def get_core_id_from_filename(filename):
    return filename.split()[0]

# no need to change anything below here

csv_columns = ['original_name', 'url_b', 'slide_id', 'core_id', 'data_owner', 'stain_type', 'tumour_type']

def get_files_in_folder(path, extn):
    files = [f for f in listdir(path) if (isfile(join(path, f)) and f.endswith(extn))]
    return files


def create_metadata (files):
    metadata = []
    index = 0
    for f in files:
        file_metadata = {}
        index += 1
        # data that varies by file
        file_metadata['original_name'] = f
        file_metadata['public_name'] = '-'.join((stain_type,format(index, '02d'))) + '.jpg'
        file_metadata['url_b'] = join(server_folder, file_metadata['public_name'])
        file_metadata['slide_id'] = 'unknown'
        file_metadata['core_id'] = get_core_id_from_filename(f)
        # data common to all files
        file_metadata['data_owner'] = data_owner
        file_metadata['stain_type'] = stain_type
        file_metadata['tumour_type'] = tumour_type
        metadata.append(file_metadata)
    return metadata

def purge(dir, pattern):
    for f in os.listdir(dir):
        if f.endswith(pattern):
            os.remove(os.path.join(dir, f))

def main():

    #empty target folder
    purge(target_folder, file_extn)

    # create metadata for all files in source folder
    metadata = create_metadata(get_files_in_folder(source_folder, file_extn))

    with open(join(source_folder, metadata_filename), 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # write header row
        csvwriter.writerow(csv_columns)
        # write file data
        for file_metadata in metadata:
            # copy and rename files
            source_filename = join(source_folder, file_metadata['original_name'])
            target_filename = join(target_folder, file_metadata['public_name'])
            # shutil.copy(source_filename, target_filename)
            imagemagick_cmd = 'convert "' + source_filename + '" -resize 3000x3000 -quality 75 -strip ' + target_filename
            os.system(imagemagick_cmd)
            # write metadata to csv
            line = [ file_metadata[key] for key in csv_columns]
            csvwriter.writerow(line)
        csvfile.close()

main()




