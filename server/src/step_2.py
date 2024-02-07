import pandas as pd;

def read_input(file_name: str) -> dict:
    excel = pd.read_excel(file_name, usecols="D, E, M").dropna();
    return excel;

def extract_bacterial_sequences(file_contents: dict):
    count: int = 0;
    with open("bacteria_sequences_spaces_removed.fasta", "w") as f:
        for bacteria in file_contents.values:
            if bacteria[1] == "Bacteria":
                f.write(f">{bacteria[0].replace(' ', '_')}\n{bacteria[2]}\n");
                count += 1;
    print(count);
if __name__ == "__main__":
    file_contents = read_input("./bacterial_sequences.xlsx");
    extract_bacterial_sequences(file_contents);



# with open("iteration_5.tree.pda", "r") as f:
#     lines = f.readlines();
#     proteins = [];
#     for i, line in enumerate(lines):
#         if lines[i].startswith("The optimal"):
#             number_of_taxa = int(lines[i].split()[5]) + 1;
#             proteins = lines[i + 1:i + number_of_taxa];
#             break;
#     for protein in proteins:
#         file_name = protein.split("__")[1];
#         organism_protein = protein.split("__")[1].split("_");
#         organism_name = organism_protein[0];
#         protein_name = organism_protein[-1];
#         # print(organism_name);
#         print(file_name);
#         # print(protein_name);
            
#     # for line in lines:
#     #     print(line);
#     # print(lines);





