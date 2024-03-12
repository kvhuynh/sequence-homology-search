import os;


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
    print(os.getcwd());
    # create phase folder inside of job name
    while True:
        common_prefix: str = f"./output/{job_name}"
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

def create_combined_fasta() -> None:
    # create combined file in database folder
    command: str = f"cat ./databases/TCS/*.fasta > ./databases/combined_eukprot.fasta";
    subprocess.run(command, shell=True);