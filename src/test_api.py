import requests

url = 'http://127.0.0.1:8000/ask'

json_data = {
    'start': 'H101_01',
    'arrival': 'E214_03'
}
response = requests.get(url, json=json_data)
print('Code de statut :', response.status_code)
print('Contenu de la réponse :', response.text)
