import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#BASE_URL = "https://repositorio.ufcspa.edu.br/server/api"
#BASE_URLS = ["https://repositorio.unipampa.edu.br", "https://repositorio.ufcspa.edu.br"]
BASE_URLS = open("input-dspace7+.txt").read().splitlines()
API_URL = "/server/api"
def obter_handles_recentes(base_url:str):
    file = open(f"results/{base_url.removeprefix("https://").removeprefix("http://").replace('/', '-')}.txt", "w")
    params = {
        "query": "*",
        "dsoType": "ITEM",
        "sort": "dc.date.accessioned,DESC",
        "size": 100,
        "page": 0
    }

    r = requests.get(
        f"{base_url + API_URL}/discover/search/objects",
        params=params,
        headers={"Accept": "application/json"},
        verify=False
    )

    r.raise_for_status()

    objetos = (
        r.json()
        .get("_embedded", {})
        .get("searchResult", {})
        .get("_embedded", {})
        .get("objects", [])
    )
    result = []
    for obj in objetos:
        item = obj["_embedded"]["indexableObject"]

        titulo = item.get("name", "")
        uuid = item["uuid"]

        item_resp = requests.get(
            f"{base_url+API_URL}/core/items/{uuid}",
            headers={"Accept": "application/json"}, verify=False
        )
        item_resp.raise_for_status()

        item_json = item_resp.json()

        handle = item_json.get("handle")
        result.append(f"{base_url+ '/handle/' +handle}")
        print(f"{handle} - {titulo}")
    file.writelines([f"{item}\n" for item in result])
    file.close()
if __name__ == "__main__":
    for url in BASE_URLS:
        obter_handles_recentes(url)