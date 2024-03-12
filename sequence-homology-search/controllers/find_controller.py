import requests;

UNIPROT_URL: str = f"https://rest.uniprot.org/uniprotkb/search?&query=protein_name:";
ENSEMBL_PROTISTS_URL_FRONT: str = "https://rest.ensembl.org/sequence/id/";
ENSEMBL_PROTISTS_URL_BACK: str = "?content-type=application/json;expand=1";

def get_uniprot_sequences(initial_input: str):
    initial_input = initial_input[0];
    response: tuple = __ping_uniprot(UNIPROT_URL + initial_input);
    pagination_link: str = response[0];
    protein_sequence = response[1];
    count: int = 0;
    while pagination_link != None:
        response = __ping_uniprot(pagination_link);
        pagination_link = response[0];
        print(pagination_link);
        count += 1;
    print(count);
    
        


    #  slice string to extract what is between <>


def __ping_uniprot(url: str):
    response: requests.models.Response = requests.get(url);
    try:
        return (response.headers["link"].split(";")[0][1:-1], response.json()["results"][0]["sequence"]["value"]);
    except KeyError:
        return (None, response.json()["results"][0]["sequence"]["value"])


