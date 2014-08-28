#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    This file is a part of DARFI project (dna Damage And Repair Foci Imager)
#    Copyright (C) 2014  Ivan V. Ozerov
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 2 as·
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License v2 for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import os
import pic_an_2

def calc_multiple_dirs(dir_path, nuclei_name='3DAPI.TIF', foci_name='3FITС.TIF'):
    '''Separately calculates foci for all subdirs'''

    subdirs = [os.path.join(dir_path, directory) for directory in os.listdir(dir_path) \
            if os.path.isdir(os.path.join(dir_path, directory))]

    for subdir in subdirs:

        print 'Calculation has STARTED in', os.path.split(subdir)[0]

        calc_foci_in_dir(subdir, nuclei_name, foci_name)

        print 'Calculation has FINISHED in', os.path.split(subdir)[0]


def calc_foci_in_dir(dir_path, nuclei_name='3DAPI.TIF', foci_name='3FITС.TIF', outfile = 'result.txt'):
    '''Calculates foci from dir'''

    dirs_with_images = [os.path.join(dir_path, directory) for directory in os.listdir(dir_path)]

    pre_image_dirs = [image_dir for image_dir in dirs_with_images if \
            (os.path.isfile(os.path.join(image_dir,nuclei_name)) and os.path.isfile(os.path.join(image_dir, foci_name)))]

    image_dirs = [pic_an_2.image_dir(image_dir) for image_dir in pre_image_dirs]

    path1,name2 = os.path.split(dir_path)
    name1       = os.path.split(path1)[1]

    name = name1 + '_' + name2
    absoutfile = os.path.join(dir_path,outfile)

    cell_set = pic_an_2.cell_set(name=name, cells=[])

    remained = len(image_dirs)

    print "We have", remained, 'images to load for', name

    print "Image loading have started for", name

    for image_dir in image_dirs:
        image_dir.load_separate_images( nuclei_name, foci_name, 1500)

        remained -= 1

        if remained == 0:
            print "Image loading have finished for", name
        else:
            print remained, 'images remained to load for', name

        cell_set.extend(image_dir)

    if len(cell_set.cells) == 0:
        print "There are no cells in the images from ", dir_path
        return

    print "We have", len(cell_set.cells), "cells to analyze for", name

    cell_set.rescale_nuclei()
    cell_set.rescale_foci()

    cell_set.calculate_foci()
    cell_set.calculate_foci_parameters()
    cell_set.write_parameters(absoutfile)

    for image_dir in image_dirs:
        image_dir.write_all_pic_files()



