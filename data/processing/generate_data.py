import os
import numpy as np
import Image
from scipy import sparse

def get_files(dir_name, filetype):
    """
    Return a list of files of a particular filetype in a directory

    Parameter
    =========
    dir_name = name of the directory
    filetype = type of file to be extracted

    Return
    ======
    List of paths to png
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
    List of directories
    """
    directories = []
    if not os.path.isfile(dir_name) and os.path.exists(dir_name):
        for dirpath, dirnames, filenames in os.walk(dir_name):
            if text in dirpath:
                directories.append(dirpath)
    return directories

def invert_colors(array):
    """
    loop through a given array and check the value the
    given value can either be 262.65 or 0.0
    the replcaes the value with 0.0 if 262.65 is given and vice versa.

    Parameter
    =========
    array = a vector with values 262.65 and 0.0

    Return
    ======
    an array wit values interchanged
    """
    for index in range(array.shape[0]):
        value = array[index]
        if value == 262.65:
            array[index] = 0.0
        else:
            array[index] = 262.65
    return array

def get_matrix(img_path):
    """
    Given an image path read the image and write the grayscale in
    matrix form in .npy files

    Parameter
    =========
    img_path = path of the image file to be processed

    Return
    ======
    List of filepaths
    """
    img = Image.open(img_path)
    arr = np.array(img)
    greyscale = np.dot(arr[...,:3], [0.299, 0.587, 0.144])
    greyscale = np.ravel(greyscale)
    greyscale = np.apply_along_axis(lambda x : invert_colors(x), 0, greyscale)
    return greyscale

def main():
    """
    This function is to be executed if script is executed
    """
    home = os.path.expanduser('~') + '/projects'
    project_path = home + '/digit-recoganizer'
    dir_name = project_path + '/data/English/'
    list_of_dir = get_directory_names(dir_name)
    print "Total list of directories"
    print "=========================================="
    print list_of_dir
    print "=========================================="
    #loop through each directory and generate a matrix file for each image
    for index in range(0, len(list_of_dir)):
        directory = list_of_dir[index]
        print "Processing directory ", directory
        pngs = get_files(directory, 'png')
        print "Found {0} png images".format(len(pngs))
        matrix_elements = [get_matrix(png) for png in pngs]
        print "successfully processed {0} pngs".format(len(matrix_elements))
        #combine the columns in ma=trix_elements to form the needed matrix
        matrix = np.vstack([col for col in matrix_elements])
        matrix = sparse.csr_matrix(matrix)
        np.save(directory, matrix)

if __name__ == "__main__":
    main()