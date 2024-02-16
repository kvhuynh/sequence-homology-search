

# importing the required modules
import os
import argparse
from hmmer_operations import hmm_search_main;
 
def main():
    # create parser object
    parser = argparse.ArgumentParser(description = "Sequence Homology Search")
 
    # defining arguments for parser object
    parser.add_argument("-r", "--read", type = str, nargs = 1,
                        metavar = "file_name", default = None,
                        help = "Opens and reads the specified text file.")

    parser.add_argument("-n", "--number", type = str, nargs = 1,
                        metavar=("number_of_iterations"), default = 5, help = "Specify the amount of iterations a search should perform.")
     
    parser.add_argument("-p1", "--phase1", type = str, nargs = 2,
                        metavar = ("hmmer_file_path", "job_name"), default = None,
                        help = "Begins an iterative search on a given hmm file and database (currently only EukProt). Creates a separate folder for each iteration in the output folder.");

    parser.add_argument("-p2", "--phase2", type = str, nargs = 2,
                        metavar = ("path_to_p1_hmmer", "job_name", "bacterial_sequences"),
                        help = "")
     
    parser.add_argument("-d", "--database", type = str,
                        default = None,
                        help = "This version only supports the EukProt database. Due to it's large size, user download is required. Download link: https://figshare.com/articles/dataset/TCS_tar_gz/21586065. Extract database into the databases folder.")

 
    # parse the arguments from standard input
    args = parser.parse_args()
    # calling functions depending on type of argument
    if args.read != None:
        read(args);
    elif args.phase1 != None:
        hmm_search_main(args.number, args.phase1[0], args.phase1[1]);
    elif args.delete !=None:
        delete(args);
    elif args.copy != None:
        copy(args);
    elif args.rename != None:
        rename(args);

 
if __name__ == "__main__":
    # calling the main function
    main();