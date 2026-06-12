import requests
from bs4 import BeautifulSoup
import time
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL_BASE_LIST = ["https://ri.unir.br"]  
FRONTENDS = ["jspui", "xmlui", ""]  

URL_BROWSE_BASE = f"{URL_BASE_LIST}/{FRONTENDS[0]}/browse?type=dateissued&sort_by=2&order=DESC&rpp=100"

def extrair_handles_recentes(url_busca, max_paginas=5):
    handles_coletados = []
    handles_unicos_controle = set()
    
    pagina_atual = 1
    offset = 0  
    padrao_handle = re.compile(r'handle/\d+/\d+')

    print(f"Iniciando raspagem cronológica decrescente para: {URL_BASE_LIST[0]}")
    print("-" * 50)

    while True:
        print(f"Coletando página {pagina_atual} (Offset: {offset})...")
        
        url_pagina = f"{url_busca}&offset={offset}"

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            resposta = requests.get(url_pagina, headers=headers, verify=False, timeout=30)
            
            if resposta.status_code != 200:
                print(f"Erro HTTP {resposta.status_code} ao acessar a página.")
                break
                
            soup = BeautifulSoup(resposta.content, 'html.parser')
            
            links = soup.find_all('a', href=True)
            
            novos_handles_na_pagina = 0
            
            for link in links:
                href = link['href']
                if 'handle/' in href:
                    resultado = padrao_handle.search(href)
                    if resultado:
                        url_handle_completa = f"{URL_BASE}/{FRONTEND}/{resultado.group(0)}"
                        
                        if url_handle_completa not in handles_unicos_controle:
                            handles_unicos_controle.add(url_handle_completa)
                            handles_coletados.append(url_handle_completa)
                            novos_handles_na_pagina += 1

            print(f"Handles encontrados nesta página: {novos_handles_na_pagina}")
            print(f"Total acumulado: {len(handles_coletados)} handles únicos em ordem decrescente.")

            if novos_handles_na_pagina == 0:
                print("\nFim dos registros encontrados ou nenhuma novidade nesta página.")
                break

            pagina_atual += 1
            offset += 100  
            
            if pagina_atual > max_paginas:
                print(f"\n[Aviso] Limite de segurança de {max_paginas} páginas atingido.")
                break
                
            time.sleep(1.5)

        except Exception as e:
            print(f"Ocorreu uma falha durante a raspagem: {e}")
            break

    return handles_coletados

if __name__ == "__main__":
    lista_de_handles = extrair_handles_recentes(URL_BROWSE_BASE, max_paginas=1)
    
    print("\n" + "=" * 50)
    print(f"Extração Concluída! {len(lista_de_handles)} Handles encontrados (do mais recente ao mais antigo):")
    print("=" * 50)
    
    for h in lista_de_handles[:20]:
        print(f" - {h}")
    
    if len(lista_de_handles) > 20:
        print(f" ... e mais {len(lista_de_handles) - 20} handles.")
        
    with open("handles_recentes_unir.txt", "w") as f:
         for h in lista_de_handles:
            f.write(f"{h}\n")
    print("\nArquivo 'handles_recentes_unir.txt' gerado com sucesso!")