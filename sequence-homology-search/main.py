

# importing the required modules
import os
import argparse
from hmmer_operations import hmm_search_main;

 
# error messages
# INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be a .txt file."
# INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."
 
 
def validate_file(file_name):
    '''
    validate file name and path.
    '''
    if not valid_path(file_name):
        print(INVALID_PATH_MSG%(file_name))
        quit()
    elif not valid_filetype(file_name):
        print(INVALID_FILETYPE_MSG%(file_name))
        quit()
    return
     
def valid_filetype(file_name):
    # validate file type
    return file_name.endswith('.txt')
 
def valid_path(path):
    # validate file path
    return os.path.exists(path)
         
     
 
def read(args):
    # get the file name/path
    file_name = args.read[0]
 
    # validate the file name/path
    validate_file(file_name)
 
    # read and print the file content
    with open(file_name, 'r') as f:
        print(f.read())
 
 
def show(args):
    # get path to directory
    dir_path = args.show[0]
     
    # validate path
    if not valid_path(dir_path):
        print("Error: No such directory found.")
        exit()
 
    # get text files in directory
    files = [f for f in os.listdir(dir_path) if valid_filetype(f)]
    print("{} text files found.".format(len(files)))
    print('\n'.join(f for f in files))
     
 
def delete(args):
    # get the file name/path
    file_name = args.delete[0]
 
    # validate the file name/path
    validate_file(file_name)
     
    # delete the file
    os.remove(file_name)
    print("Successfully deleted {}.".format(file_name))
     
 
def copy(args):
    # file to be copied
    file1 = args.copy[0]
    # file to copy upon
    file2 = args.copy[1]
 
    # validate the file to be copied
    validate_file(file1)
 
    # validate the type of file 2
    if not valid_filetype(file2):
        print(INVALID_FILETYPE_MSG%(file2))
        exit()
 
    # copy file1 to file2
    with open(file1, 'r') as f1:
        with open(file2, 'w') as f2:
            f2.write(f1.read())
    print("Successfully copied {} to {}.".format(file1, file2))
 
 
def rename(args):
    # old file name
    old_filename = args.rename[0]
    # new file name
    new_filename = args.rename[1]
 
    # validate the file to be renamed
    validate_file(old_filename)
 
    # validate the type of new file name
    if not valid_filetype(new_filename):
        print(INVALID_FILETYPE_MSG%(new_filename))
        exit()
 
    # renaming
    os.rename(old_filename, new_filename)
    print("Successfully renamed {} to {}.".format(old_filename, new_filename))
def main():
    # create parser object
    parser = argparse.ArgumentParser(description = "Sequence Homology Search")
 
    # defining arguments for parser object
    parser.add_argument("-r", "--read", type = str, nargs = 1,
                        metavar = "file_name", default = None,
                        help = "Opens and reads the specified text file.")

    parser.add_argument("-n", "--number", type = str, nargs = 1,
                        metavar=("number_of_iterations"), default = 5, help = "Specify the amount of iterations a search should perform.")
     
    parser.add_argument("-s", "--search", type = str, nargs = 2,
                        metavar = ("hmmer_file_path", "job_name"), default = None,
                        help = "Begins an iterative search on a given hmm file and database (currently only EukProt). Creates a separate folder for each iteration in the output folder.")
     
    parser.add_argument("-d", "--database", type = str,
                        default = None,
                        help = "This version only supports the EukProt database. Due to it's large size, user download is required. Download link: https://figshare.com/articles/dataset/TCS_tar_gz/21586065. Extract database into the utilities folder.")

 
    # parse the arguments from standard input
    args = parser.parse_args()
    # calling functions depending on type of argument
    if args.read != None:
        read(args);
    elif args.search != None:
        hmm_search_main(args.number, args.search[0], args.search[1]);
    elif args.delete !=None:
        delete(args);
    elif args.copy != None:
        copy(args);
    elif args.rename != None:
        rename(args);

 
if __name__ == "__main__":
    # calling the main function
    main();