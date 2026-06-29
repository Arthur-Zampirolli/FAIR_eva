import requests


BASE_URL = "https://domusdados.unifesp.br"
API_ENDPOINT = f"{BASE_URL}/api/search"


params = {
    "q": "*",                       
    "type": "dataset",              
    "sort": "date",                
    "order": "desc",                
    "per_page": 100,                
    "start": 0
}

headers = {
    "X-Dataverse-key": ""
}

print(f"Buscando os últimos 100 datasets em: {BASE_URL}...\n")

try:
    response = requests.get(API_ENDPOINT, params=params, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    items = data.get("data", {}).get("items", [])
    
    links_identificadores = []
    
    for item in items:
        global_id = item.get("global_id", "")
        
        if not global_id:
            
            url_direta = item.get("url")
            if url_direta:
                links_identificadores.append(url_direta)
            continue

        
        if "doi:" in global_id.lower():
            
            clean_doi = global_id.lower().replace("doi:", "").strip()

            original_id = global_id[-len(clean_doi):] if clean_doi else ""
            links_identificadores.append(f"https://doi.org/{original_id}")
            

        elif "hdl:" in global_id.lower():
            clean_hdl = global_id.lower().replace("hdl:", "").strip()
            original_id = global_id[-len(clean_hdl):] if clean_hdl else ""
            links_identificadores.append(f"https://hdl.handle.net/{original_id}")
            

        elif global_id.startswith("http"):
            links_identificadores.append(global_id)


    print(f"Sucesso! Encontrados {len(links_identificadores)} identificadores:\n")
    for url in links_identificadores:
        print(url)

except requests.exceptions.RequestException as e:
    print(f"Erro ao conectar com a API: {e}")