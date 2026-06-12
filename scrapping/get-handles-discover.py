import requests

#BASE_URL = "https://repositorio.ufcspa.edu.br/server/api"
BASE_URL = "https://repositorio.unipampa.edu.br/server/api"
def obter_handles_recentes():
    params = {
        "query": "*",
        "dsoType": "ITEM",
        "sort": "dc.date.accessioned,DESC",
        "size": 100,
        "page": 0
    }

    r = requests.get(
        f"{BASE_URL}/discover/search/objects",
        params=params,
        headers={"Accept": "application/json"}
    )

    r.raise_for_status()

    objetos = (
        r.json()
        .get("_embedded", {})
        .get("searchResult", {})
        .get("_embedded", {})
        .get("objects", [])
    )

    for obj in objetos:
        item = obj["_embedded"]["indexableObject"]

        titulo = item.get("name", "")
        uuid = item["uuid"]

        item_resp = requests.get(
            f"{BASE_URL}/core/items/{uuid}",
            headers={"Accept": "application/json"}
        )
        item_resp.raise_for_status()

        item_json = item_resp.json()

        handle = item_json.get("handle")

        print(f"{handle} - {titulo}")

if __name__ == "__main__":
    obter_handles_recentes()