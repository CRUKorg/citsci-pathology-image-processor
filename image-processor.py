__author__ = 'paters01'

import os
from os import listdir
from os.path import isfile, join
import csv
import shutil

# file locations
source_folder = '/data/Trailblazer/EGFR-all-images'
target_folder = '/data/Trailblazer/GitHub/lung-egfr-v2'  # note that this folder must already exist - script does not create it
# server_folder = '//citscitools.cancerresearchuk.org/static/mvp-images/lung-egfr-v2'
server_folder = '/static/trailblazer/images/lung_egfr'
source_file_extn = '.jpg'
target_file_extn = '.jpg'
metadata_filename = 'lung-egfr-metadata.csv'
start_index_after = 0 # images will be numbered sequentially from the number AFTER this value (normally zero)
delete_existing_files = True  # True when recreating whole folder structure, False to make additions

# common data for import
tumour_type = 'lung'
stain_type = 'egfr'
data_owner = 'Gareth Thomas'
dataset_id = 'gt01'
index_format = '02d'

processing_annotated_images = False  # no need to rename annotated files

# this needs to be changed according to data filename format
def get_core_id_from_filename(filename):
    start = filename.find('_',4) + 1
    end = filename.rfind('_')
    return filename[start:end]

# no need to change anything below here

csv_columns = ['original_name', 'url_b', 'slide_id', 'core_id', 'core_index', 'data_owner', 'stain_type', 'tumour_type']

def get_files_in_folder(path, extn):
    files = [f for f in listdir(path) if (isfile(join(path, f)) and f.endswith(extn))]
    return files


def create_metadata (files):
    metadata = []
    index = start_index_after
    for f in files:
        file_metadata = {}
        index += 1
        formatted_index = format(index, index_format)
        # data that varies by file
        file_metadata['original_name'] = f
        #  file_metadata['public_name'] = '-'.join((stain_type,format(index, '02d'))) + '.jpg'
        file_metadata['public_name'] = '-'.join((tumour_type, stain_type, dataset_id, formatted_index)) + target_file_extn
        file_metadata['url_b'] = join(server_folder, file_metadata['public_name'])
        file_metadata['slide_id'] = 'unknown'
        file_metadata['core_id'] = get_core_id_from_filename(f)
        file_metadata['core_index'] = formatted_index
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

    if delete_existing_files:
        #empty target folder
        purge(target_folder, target_file_extn)

    # create metadata for all files in source folder
    metadata = create_metadata(get_files_in_folder(source_folder, source_file_extn))

    with open(join(source_folder, metadata_filename), 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # write header row
        csvwriter.writerow(csv_columns)
        # write file data
        for file_metadata in metadata:
            # copy and rename files
            source_filename = join(source_folder, file_metadata['original_name'])
            if processing_annotated_images:
                # work out target name = source name but with target extn
                filename = file_metadata['original_name'].split('.')[0] + target_file_extn
                target_filename = join(target_folder, filename)
            else:
                target_filename = join(target_folder, file_metadata['public_name'])
            # shutil.copy(source_filename, target_filename)
            imagemagick_cmd = '/usr/local/bin/convert "' + source_filename + '" -resize 3000x3000 -quality 75 -strip ' + target_filename
            os.system(imagemagick_cmd)
            # write metadata to csv
            line = [ file_metadata[key] for key in csv_columns]
            csvwriter.writerow(line)
        csvfile.close()

main()




