import re


def converter_urls(arquivo_entrada, arquivo_saida):
    base_dataverse = "https://domusdados.unifesp.br/dataset.xhtml?persistentId="
    urls_convertidas = []

    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        linhas = f.read().splitlines()

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        
        
        if "hdl.handle.net/" in linha:
            
            id_persistent = linha.split("hdl.handle.net/")[-1]
            nova_url = f"{base_dataverse}hdl:{id_persistent}"
            urls_convertidas.append(nova_url)
            
        
        elif "doi.org/" in linha:
            
            id_persistent = linha.split("doi.org/")[-1]
            nova_url = f"{base_dataverse}doi:{id_persistent}"
            urls_convertidas.append(nova_url)
            
        else:
            
            print(f"Formato não reconhecido: {linha}")
            urls_convertidas.append(linha)

    
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        for url in urls_convertidas:
            f.write(url + '\n')

    print(f"Sucesso! {len(urls_convertidas)} URLs convertidas e salvas em '{arquivo_saida}'.")

if __name__ == "__main__":
    arquivo_in = "results/temp/unifesp.txt"
    arquivo_out = "results/temp/unifesp_ajustado.txt"
    
    
    converter_urls(arquivo_in, arquivo_out)