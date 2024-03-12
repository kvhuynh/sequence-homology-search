class HmmerOperator:

    def __init__(self, hmm_file: str,  common_file_prefix: str):
        self.hmm_file = hmm_file;
        self.common_file_prefix = common_file_prefix;

    def get_iteration(self):
        # implement feature later to stop when searches are saturated
        iteration_amount: int = int(input("How many iterations would you like to run."));
        return iteration_amount;
    
    def hmm_search(self, common_file_prefix: str, hmm_file: str):
        command: str = f"hmmsearch -E 0.001 --tblout {common_file_prefix}.txt ./{hmm_file} ./databases/combined_eukprot.fasta";
        print(f"Searching {hmm_file} against EukProt...")
        subprocess.run(command, shell=True);
        print(f"Results have been saved to {common_file_prefix}.txt");

    def hmm_align(self, common_file_prefix: str, path_to_original_hmm, i: int):
        print(f"Aligning sequences with {path_to_original_hmm} against iteration_{i}.fasta...");
        output_location: str = f"{common_file_prefix}_aligned.txt";
        protein_matches: str = f"{common_file_prefix}_protein_matches.fasta";
        command: str = f"hmmalign -o {output_location} {path_to_original_hmm} {protein_matches}";
        subprocess.run(command, shell=True);

    def hmm_build(self, common_file_prefix: str):
        print(f"Creating a new hmm file...");
        new_hmm: str = f"{common_file_prefix}.hmm"
        command: str = f"hmmbuild {common_file_prefix}.hmm {common_file_prefix}_aligned.txt";
        subprocess.run(command, shell=True);
        return new_hmm;

    def __extract_protein_from_fasta(common_file_prefix: str, parsed_hmm: dict, i: int) -> None:
        print(f"Retrieving protein sequences of hits in EukProt database...");
        with open(f"{common_file_prefix}_protein_matches.fasta", "w") as fasta_file:
            for key in parsed_hmm:
                proteins = parsed_hmm[key]["proteins"];
                for file in os.listdir("./databases/TCS"):
                    file_name: str = file.split("_")[0];
                    if key == file_name:
                        with open(f"./databases/TCS/{file}", "r") as f:
                            for record in SeqIO.parse(f, "fasta"):
                                for protein in proteins:
                                    if protein == record.id.split("_")[-1]:
                                        fasta_file.write(f"> {record.id}\n{record.seq}\n");