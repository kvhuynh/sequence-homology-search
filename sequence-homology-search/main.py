

# importing the required modules
import os;
from classes.ThirdPartyTools import *;
import argparse;
from hmmer_operations import hmm_search_main;

def create_output() -> None:
    if not os.path.exists("./output"):
        os.mkdir("output");

def check_db() -> bool:
    if not os.path.exists("./databases/TCS"):
        print("DATABASE NOT FOUND. PLEASE DOWNLOAD DATABASE FROM: https://figshare.com/articles/dataset/TCS_tar_gz/21586065 AND EXTRACT INTO THE DATABASES FOLDER.");
        exit();
    else:
        if not os.path.isfile("./databases/combined_eukprot.fasta"):
            print("Combined eukprot file not found. Creating one...");
            return False;
        else:
            print("Database file found. ");
            return True;

def create_job(job_name: str, phase: str) -> None:
    while True:
        common_prefix: str = f"./{phase}/output/{job_name}"
        if os.path.exists(common_prefix):
            override_job: str = input(f"A job named {job_name} already exists. Would you like to override? (y/n/q): ").lower().strip();
            if override_job == "y" or override_job == "yes":
                shutil.rmtree(common_prefix);
                os.mkdir(common_prefix);
                break;
            elif override_job== "n" or override_job == "no":
                new_job_name: str = input(f"Please choose a new name: ");
                job_name = new_job_name;
                continue;
            elif override_job == "q" or override_job == "quit":
                quit();
            else:
                print("Invalid response");
        else:
            os.mkdir(common_prefix);
            break;
    return job_name;

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
                        help = "Begins phase 1, an iterative search on a given hmm file and database (currently only EukProt). Creates a separate folder for each iteration in the output folder.");

    parser.add_argument("-p2", "--phase2", type = str, nargs = 3,
                        metavar = ("path_to_p1_protein_file", "job_name", "bacterial_sequences"),
                        help = "Begins phase 2, combines eukaryotic and bacterial sequences into a hmm profile. Work flow: Align sequences with MAFFT -> build tress with FastTree -> downsample sequences with Phylogenetic Diversity Analyzer.")
     
    parser.add_argument("-d", "--database", type = str,
                        default = None,
                        help = "This version only supports the EukProt database. Due to it's large size, user download is required. Download link: https://figshare.com/articles/dataset/TCS_tar_gz/21586065. Extract database into the databases folder.")

 
    # parse the arguments from standard input
    args = parser.parse_args()
    # calling functions depending on type of argument
    if args.phase1 != None:
        hmm_search_main(args.number, args.phase1[0], args.phase1[1]);
    elif args.phase2 != None:
        pass;



 
if __name__ == "__main__":
    # calling the main function
    # main();
    test = ThirdPartyTools("f");
    print(test);