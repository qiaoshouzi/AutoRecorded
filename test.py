import json

json_path='config.json'
json_data=''

def get_json_data(json_path):
    with open(json_path,'rb') as f:
        params = json.load(f)
        json_data = params
    f.close()
    return json_data

json_data=get_json_data(json_path)

print(json_data)