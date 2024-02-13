import os;
import csv;
import subprocess;
from Bio import SearchIO;
from Bio import SeqIO;

"""
Creates folder for the current iteration

Args:
    i (int): Current iteration
Returns:
  None
"""
def make_folder(i: int) -> None:
    folder_name: str = f"iteration_{i}"
    os.mkdir(folder_name);
    os.chdir(f"./{folder_name}");

"""
Runs hmmsearch

Args:
  i (int): Current iteration
  hmm_file (str): hmmer profile used to be searched against the EukProt database

Returns:
  None
"""
def hmm_search(i: int, hmm_file: str, path_to_database: str) -> None:
    # command: str = f"hmmsearch -E 0.001 --tblout ./run_{i}.txt ../hmm_folder/{hmm_file} ../eukprot_combined.fasta";
    # print(f"Searching {hmm_file} against EukProt...")
    # subprocess.run(command, shell=True);
    pass;
    


"""
Parses results of hmm_search (hmmsearch)

Args:
  i (int): Current iteration
  hmm_file (str): hmmer profile used to be searched against the EukProt database

Returns:
  None
"""
def parse_hmm_search(i: int) -> dict:
    species_information: dict = {};
    print(f"Parsing results of hmmsearch...")
    with open(f"run_{i}.txt", "r") as input:
        for result in SearchIO.parse(input, "hmmer3-tab"):
            for hit in result:
                split_file_name: list = hit.id.split("_");
                species: str = split_file_name[0]
                protein_name: str = split_file_name[-1];
                if species not in species_information:
                    species_information[species] = {"count": 1, "proteins": [protein_name]};
                else:
                    if species_information[species]["count"] < 10:
                        species_information[species]["count"] += 1;
                        species_information[species]["proteins"].append(protein_name);
    with open("test_dict.txt", "w") as f:
        f.write(str(species_information));
    return species_information;

def extract_protein_from_fasta(parsed_hmm: dict, i: int) -> None:
    os.chdir("../TCS");
    print(f"Retrieving protein sequences of hits in EukProt database...");
    with open(f"../iteration_{i}/iteration_{i}.fasta", "w") as fasta_file:
        for key in parsed_hmm:
            proteins = parsed_hmm[key]["proteins"];
            for file in os.listdir():
                file_name: str = file.split("_")[0];
                if key == file_name:
                    with open(file, "r") as f:
                        for record in SeqIO.parse(f, "fasta"):
                            for protein in proteins:
                                # print(record.id.split("_")[-1]);
                                if protein == record.id.split("_")[-1]:
                                    print(f"MATCH: {protein} {record.id.split('_')[-1]}");
                                    fasta_file.write(f"> {record.id}\n{record.seq}\n");
    os.chdir("../")

def hmmalign(i: int, previous_hmm_iteration: str) -> None:
    # hmm file from previous iteration
    os.chdir(f"./iteration_{i}");
    print(f"Aligning sequences with {previous_hmm_iteration} against iteration_{i}.fasta...");
    # command: str = f"hmmalign -o aligned_iter_{i}.txt ../hmm_folder/{previous_hmm_iteration} iteration_{i}.fasta";
    command: str = f"hmmalign -o aligned_iter_{i}.txt ../hmm_folder/PF04055.hmm iteration_{i}.fasta";

    subprocess.run(command, shell=True);

def hmmbuild(i: int) -> str:
    print(f"Creating a new hmm file...");
    command: str = f"hmmbuild ../hmm_folder/iteration_{i}.hmm aligned_iter_{i}.txt"
    subprocess.run(command, shell=True);
    return f"iteration_{i}.hmm";

def create_combined_fasta() -> None:
    
    pass;

def hmm_search_main(number_of_iterations: int, hmm_file: str, job_name: str) -> None:
    os.chdir("./utilities");
    if not os.path.exists("./TCS"):
        print("DATABASE NOT FOUND. PLEASE DOWNLOAD DATABASE FROM: https://figshare.com/articles/dataset/TCS_tar_gz/21586065 AND EXTRACT INTO THE UTILITIES FOLDER.");
        exit();
    else:
        if not os.path.isfile("./combined_eukprot.fasta"):
            print("Combined eukprot file not found. Creating one...");
            create_combined_fasta();
        os.chdir("../");


    if not os.path.exists("./output"):
        os.mkdir("output")
    os.chdir("./output");
    os.mkdir(job_name);
    os.chdir(f"./{job_name}");
    current_hmm_file = hmm_file;
    iteration: int = 1;
    while iteration <= 2:
        make_folder(iteration);
        # hmm_search(iteration, current_hmm_file, path_to_database);
        # parsed_hmm: dict = parse_hmm_search(i);
        # extract_protein_from_fasta(parsed_hmm, i);
        # hmmalign(i, current_hmm_file);
        # current_hmm_file: str = hmmbuild(i);
        print(os.getcwd());
        os.chdir("../");
        print(os.getcwd());
        iteration += 1;

    
