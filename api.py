import requests, sys, json

cities_list = ["NANTES", 'MASSY TGV', "PARIS"]
URL_TGVMAX = "https://data.sncf.com/api/records/1.0/search/?dataset=tgvmax&q=&facet=date&facet=origine&facet=destination&facet=od_happy_card"

def main():
    test_connect(URL_TGVMAX)

#Test de connexion à l'endpoint de l'api
def test_connect(url):
    response = requests.get(URL_TGVMAX)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)
    pull_datas(URL_TGVMAX)

#Récupération des données en json selon les villes choisies par l'utilisateur
def pull_datas(url):

    print("Villes disponibles : {0}".format(cities_list))

    while True :
        try:
            origine_city = input("Ville de départ : ").upper()
            if origine_city in cities_list :
                break
        except origine_city not in cities_list:
            continue

        
    while True :
        try:
            destination_city = input("Ville d'arrivé : ").upper()
            if destination_city in cities_list :
                break
        except destination_city not in cities_list:
            continue
    
    #On va faire correspondre l'entrée "paris" avec "paris (intramuros)" qui est utilisé dans l'API 
    cities_data = {'origine': origine_city, 'destination': destination_city}
    for k, v in cities_data.items():
        if v == "PARIS":
            cities_data[k] = "PARIS (intramuros)"

    datas = {'refine.origine' : cities_data['origine'], 'refine.destination' : cities_data['destination'], 'refine.date': '2021-11-05'}
    response = requests.get(url, params=datas)
    contenu = response.json()

    with open("data.json", "w") as f:
        json.dump(contenu, f, indent=4, ensure_ascii=False)
        f.close()

    read_datas()

def read_datas():
    with open("data.json", "r") as f :
        data_dict = json.load(f)
        f.close()
    print(data_dict['records'])

if __name__ == "__main__" :
    read_datas()