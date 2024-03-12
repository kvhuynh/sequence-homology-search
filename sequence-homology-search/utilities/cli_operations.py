import argparse;
from utilities.file_operations import *;
from models.HmmerOperator import *;
from controllers.find_controller import *;

def __cli_display():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description = "Sequence Homology Search")
 
    # defining arguments for parser object
    parser.add_argument("-p1", "--phase1", type = str, nargs = 3,
                        metavar = ("hmmer_file_path", "job_name", "iteration_count"), default = None,
                        help = "Begins phase 1, an iterative search on a given hmm file and database (currently only EukProt). Creates a separate folder for each iteration in the output folder.");

    parser.add_argument("-p2", "--phase2", type = str, nargs = 3,
                        metavar = ("path_to_p1_protein_file", "job_name", "bacterial_sequences"),
                        help = "Begins phase 2, combines eukaryotic and bacterial sequences into a hmm profile. Work flow: Align sequences with MAFFT -> build tress with FastTree -> downsample sequences with Phylogenetic Diversity Analyzer.");

    parser.add_argument("-f", "--find", type = str, nargs = 1, metavar = ("protein name"), help = "Searches the UniProt database for protein homologs of a given input string.");
     
    parser.add_argument("-d", "--database", type = str,
                        default = None,
                        help = "This version only supports the EukProt database. Due to it's large size, user download is required. Download link: https://figshare.com/articles/dataset/TCS_tar_gz/21586065. Extract database into the databases folder.")
    return parser;

def parse_args(parser: argparse.ArgumentParser):
    parsed_arguments: argparse.Namespace = parser.parse_args();

    if check_db() == False:
        create_combined_fasta();
    create_output();
    # job_name: str = create_job(job_name);

    if parsed_arguments.phase1 != None:
        hmm_file, job_name = parsed_arguments.phase1[0], parsed_arguments.phase1[1];
        # phase_1(hmm_file, job_name);
    elif parsed_arguments.phase2 != None:
        # run phase 2;
        pass;
    
    elif parsed_arguments.find != None:
        # ping_uniprot();
        print(parsed_arguments);
        get_uniprot_sequences(parsed_arguments.find);
        # hmm_search_main(args.number, args.phase1[0], args.phase1[1]);
        # if check_db() == False:
        #     create_combined_fasta();

        # print(parsed_arguments.phase1);
        # job_name = args.phase1[1];
        # create_job(job_name, "phase_1");
        # phase_1_main(args.number, args.phase1[0], args.phase1[1]);
        # elif args.phase2 != None:
        #     pass;

def run_cli():
    parser: argparse.ArgumentParser = __cli_display();
    parse_args(parser);
