import os;
import csv;
import subprocess;
import shutil;
from Bio import SearchIO;
from Bio import SeqIO;

"""
Creates folder for the current iteration

Args:
    i (int): Current iteration
Returns:
  None
"""
def make_folder(job_name: str, i: int) -> None:
    print(f"in make_folder {os.getcwd()}");
    # os.chdir(f"./output/{job_name}");
    folder_name: str = f"{job_name}_iteration_{i}"
    os.mkdir(f"./output/{job_name}/{folder_name}");
    # os.chdir(f"./{folder_name}");
    # print(os.getcwd());

"""
Runs hmmsearch

Args:
  i (int): Current iteration
  hmm_file (str): hmmer profile used to be searched against the EukProt database

Returns:
  None
"""
def hmm_search(hmm_file: str, job_name: str, i: int) -> None:
    command: str = f"hmmsearch -E 0.001 --tblout ./output/{job_name}/{job_name}_iteration_{i}/{job_name}_iteration_{i}.txt ./{hmm_file} ./databases/combined_eukprot.fasta";
    print(f"Searching {hmm_file} against EukProt...")
    subprocess.run(command, shell=True);
    print(f"Results have been saved to ./output/{job_name}/{job_name}_iteration_{i}/{job_name}_iteration_{i}.txt");
    


"""
Parses results of hmm_search (hmmsearch)

Args:
  i (int): Current iteration
  hmm_file (str): hmmer profile used to be searched against the EukProt database

Returns:
  None
"""
def parse_hmm_search(job_name: str, i: int) -> dict:
    species_information: dict = {};
    print(f"Parsing results of hmmsearch...")
    with open(f"./output/{job_name}/{job_name}_iteration_{i}/{job_name}_iteration_{i}.txt", "r") as input:
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

    # ------ testing purposes only ------ #
    with open("test_dict.txt", "w") as f:
        f.write(str(species_information));
    # ----------------------------------- #   
    return species_information;

def extract_protein_from_fasta(job_name: str, parsed_hmm: dict, i: int) -> None:
    print(f"Retrieving protein sequences of hits in EukProt database...");
    with open(f"./output/{job_name}/{job_name}_iteration_{i}/{job_name}_iteration_{i}_protein_matches.fasta", "w") as fasta_file:
        for key in parsed_hmm:
            proteins = parsed_hmm[key]["proteins"];
            for file in os.listdir("./databases/TCS"):
                file_name: str = file.split("_")[0];
                if key == file_name:
                    with open(f"./databases/TCS/{file}", "r") as f:
                        for record in SeqIO.parse(f, "fasta"):
                            for protein in proteins:
                                if protein == record.id.split("_")[-1]:
                                    # print(f"MATCH: {protein} {record.id.split('_')[-1]}");
                                    fasta_file.write(f"> {record.id}\n{record.seq}\n");

def hmmalign(job_name: str, path_to_original_hmm: str, i: int) -> None:
    # align with original input hmm
    print(f"Aligning sequences with {path_to_original_hmm} against iteration_{i}.fasta...");
    output_location: str = f"./output/{job_name}/{job_name}_iteration_{i}/{job_name}_iteration_{i}_aligned.txt";
    protein_matches: str = f"./output/{job_name}/{job_name}_iteration_{i}/{job_name}_iteration_{i}_protein_matches.fasta";
    command: str = f"hmmalign -o {output_location} {path_to_original_hmm} {protein_matches}";
    subprocess.run(command, shell=True);

def hmmbuild(i: int) -> str:
    print(f"Creating a new hmm file...");
    command: str = f"hmmbuild ../hmm_folder/iteration_{i}.hmm aligned_iter_{i}.txt"
    subprocess.run(command, shell=True);
    return f"iteration_{i}.hmm";

def check_database() -> bool:
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

def create_output() -> None:
    if not os.path.exists("./output"):
        os.mkdir("output");

def create_combined_fasta() -> None:
    # create combined file in database folder
    command: str = f"cat ./databases/TCS/*.fasta > ./databases/combined_eukprot.fasta";
    subprocess.run(command, shell=True);

def create_job(job_name: str) -> None:
    while True:
        if os.path.exists(f"./output/{job_name}"):
            override_job: str = input(f"A job named {job_name} already exists. Would you like to override? (y/n/q): ").lower().strip();
            if override_job == "y" or override_job == "yes":
                shutil.rmtree(f"./output/{job_name}");
                os.mkdir(f"./output/{job_name}");
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
            os.mkdir(f"./output/{job_name}");
            break;
    return job_name;
        

def hmm_search_main(number_of_iterations: int, hmm_file: str, job_name: str) -> None:
    if check_database() == False:
        create_combined_fasta();
    create_output();
    job_name = create_job(job_name);
    path_to_original_hmm = hmm_file;
    current_hmm_file = hmm_file;
    iteration: int = 1;
    while iteration <= 2:
        common_file_prefix: str = f"./output/{job_name}/{job_name}_iteration_{i}/{job_name}_iteration_{i}";
        make_folder(job_name, iteration);
        hmm_search(current_hmm_file, job_name, iteration);
        parsed_hmm: dict = parse_hmm_search(job_name, iteration);
        extract_protein_from_fasta(job_name, parsed_hmm, iteration);
        hmmalign(job_name, path_to_original_hmm, iteration);
        # current_hmm_file: str = hmmbuild(i);
        iteration += 1;

    
