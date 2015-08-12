# CRUK Trailblazer image processor project

## Basic idea

The Python scripts here for the basis of the pre-upload image processing necessary to get pathology images into PyBossa.

The main functions carried out are

- rename the files to ensure they are anonymised
- copies output file to a different target directory
- compress them
- convert to jpg if necessary
- create a Pybossa image upload csv that contains image metadata

## How to use

1. There are a set of constants defined at the top of the script - update these to match image locations and formats
2. A second set of constants refer to common metadata for this image set - update as required
3. Set 'processing_annotated_images' to be true or false according to image type being processed
4. Update 'get_core_id_from_filename' according to how core_id is embedded in filename

The CSV metadata file produced as an output serves as a google spreadsheet impot for PyBossa

Note that for annotated images are not renamed but they are compressed and converted to jpg format.  The CSV file is
created for annotated images but is not needed or used.

