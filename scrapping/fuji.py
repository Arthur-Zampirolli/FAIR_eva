import requests
import json
import os
url = "http://localhost:1071/fuji/api/v1/evaluate"

fileList = os.listdir("results")
print(fileList)
def run():
    fileList.remove('fuji')
    for file in fileList:
        lines = open(f"results/{file}").read().splitlines()
        
        print(lines)
        result = []
        resultFile = None
        try:
            os.mkdir(f"results/fuji")
        except FileExistsError:
            pass
        
        resultFile = open(f"results/fuji/{file}_output.json", "w")
       
        for handle in lines:
            
            print(f"Processing {handle}")
            payload = json.dumps({
                "object_identifier": f"{handle}",
                "test_debug": True,
                "metadata_service_endpoint": "http://ws.pangaea.de/oai/provider",
                "metadata_service_type": "oai_pmh",
                "use_datacite": True,
                "use_github": False,
                "use_headless": False,
                "metric_version": "metrics_v0.8"
            })
            headers = {
                'accept': 'application/json',
                'Authorization': 'Basic bWFydmVsOndvbmRlcndvbWFu',
                'Content-Type': 'application/json'
            }
            try:
                response = requests.request("POST", url, headers=headers, data=payload)
                temp = json.loads(response.text)
                print(response.text)
                result.append(temp)
            except Exception as e:
                print(f"Error processing {handle}: {e}")
                continue
            #response = requests.request("POST", url, headers=headers, data=payload)
            #temp = json.loads(response.text)
            #print(response.text)
            #result.append(temp)
        json.dump(result, resultFile, indent=4)
        resultFile.close()
        
if __name__ == "__main__":
    run()
    print("Starting...")