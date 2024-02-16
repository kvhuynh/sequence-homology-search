class HmmerOperations:

    def __init__(self, common_file_prefix: str):
        self.common_file_prefix = common_file_prefix;
        pass;
    
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