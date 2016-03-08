# CRUK Trailblazer image processor project

## Basic idea

This Python script is used to process to transform tissue micro-array (TMA) images for use in
Cancer Research UK's Trailblazer project.  It does teh following:
 
- reads images from a source folder, 
- transforms them,
- writes out anonymised versions to a target folder and 
- creates a file of image metadata to describe the transformed images

## Prerequisites

imagemagick (6.9.3-0 or later) must be installed.  Can be downloaded from [http://www.imagemagick.org/script/binary-releases.php]

## Image transformation

The script does the following to each source image
- resizes it to 3000 x 3000 (source images are often larger than this)
- compresses image by saving at 75% quality
- strips out embedded colour profile (these can cause inconsistent colour display in different browsers)

All of the above is done by calling the imagemagick convert command.
See online imagemagick documentation for details of parameters [http://www.imagemagick.org]

## File processing

Given a source folder the script  converts all images in that folder.
Note that subfolders are not processed in any way.

Images are anonymised by renaming them based on tumour and stain type and adding an index number

## How to use

1. There are a set of constants defined at the top of the script - update these to match image locations and formats
2. A second set of constants refer to common metadata for this image set - update as required
3. Set 'processing_annotated_images' to be true or false according to image type being processed (see below)
4. Update 'get_core_id_from_filename' method according to how core_id is embedded in the source filename

The CSV metadata file produced as an output serves as a google spreadsheet import for PyBossa

Note that annotated images are not renamed but they are compressed and converted to jpg format.  
Annotated images are normally used in the tutorial and so do not need to be uploaded as tasks.
The CSV file is created for annotated images but is not needed or used.

## Image metadata

Image names are changed to ensure anonymity.  As a consequence any information encoded in the name is lost.
To preserve this, and add extra metadata, a metadata file is created as part of the transformation process.  
It is placed in the **source** folder
Some metadata is image specific, other is common to the whole batch of images being transformed.
Common metadata values are set as constants within the script:
 - collection - the name of the collection from which these images was taken
 - stain_type - the type of stain used in the images

## Changing transformation behaviour

The script has been written so that it is easy to change its behaviour in certain areas:

- source folder
- target folder
- source image type (jpeg, tiff)
- transformation details

These are all set up as constants at the top of the script and can be changed as needed

## Copyright / Licence

Copyright 2016 Cancer Research UK

Source Code License: The GNU Affero General Public License, either version 3 of the License or (at your option) any later version. (See agpl.txt file)

The GNU Affero General Public License is a free, copyleft license for software and other kinds of works, specifically designed to ensure 
cooperation with the community in the case of network server software.

Documentation is under a Creative Commons Attribution License version 3.

