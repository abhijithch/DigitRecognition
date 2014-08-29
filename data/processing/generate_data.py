import os
import glob
import numpy as np
import Image

def get_files(dir_name, filetype):
    """
    Return a list of files of a particular filetype in a directory

    Parameter
    =========
    dir_name = name of the directory
    filetype = type of file to be extracted

    Return
    ======
    list of paths to png
    """
    pngfiles = []
    if not os.path.isfile(dir_name) and os.path.exists(dir_name):
        for dirpath, dirnames, filenames in os.walk(dir_name):
            for f in filenames:
                if f.split('.')[1] == filetype:
                    pngfiles.append(dirpath + '/' + f)
    else:
        raise  Exception('path given does not exists or is not a folder')
    return pngfiles

def get_directory_names(dir_name, text='Img/Sample'):
    """
    Get directory paths containing specific directory names

    Parameter
    =========
    dir_name = directory name in which to search for.
    text = text to be matched on the path.

    Return
    ======
    list of directories
    """
    directories = []
    if not os.path.isfile(dir_name) and os.path.exists(dir_name):
        for dirpath, dirnames, filenames in os.walk(dir_name):
            if text in dirpath:
                directories.append(dirpath)
    return directories

def get_matrix(img_path):
    """
    Given an image path read the image and return the grayscale in
    matrix form.
    """
    img = Image.open(img_path)
    filepath = '/'.join(img_path.split('/')[:-1])
    if not os.path.exists(filepath+'/data'):
        os.makedirs(filepath+'/data')
    filename = filepath + '/data/' + img_path.split('/')[-1].split('.')[0]
    arr = np.array(img)
    greyscale = np.dot(arr[...,:3], [0.299, 0.587, 0.144])
    np.save(filename, greyscale)
    return filename

def main():
    """
    This function is to be executed if script is executed
    """
    home = os.path.expanduser('~') + '/projects'
    project_path = home + '/digit-recoganizer'
    dir_name = project_path + '/data/English/'
    list_of_dir = get_directory_names(dir_name)

    #loop through each directory and generate a matrix file for each image
    for index in range(0, 1):
        directory = list_of_dir[0]
        print "Processing directory ", directory
        pngs = get_files(directory, 'png')
        matrix_files = [get_matrix(png) for png in pngs]


if __name__ == "__main__":
    main()