import requests

url = 'http://127.0.0.1:8000/ask'

json_data = {
    'start': 'Entrée principal du Solbosch',
    'arrival': 'H.101'
}
response = requests.get(url, json=json_data)
print('Code de statut :', response.status_code)
print('Contenu de la réponse :', response.text)
