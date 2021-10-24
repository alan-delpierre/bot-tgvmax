import requests, sys, json

cities_list = ["NANTES", 'MASSY TGV', "PARIS"]


#Test de connexion à l'endpoint de l'api
def test_connect(url):
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)
    

#Récupération des données en json selon les villes choisies par l'utilisateur
def pull_datas(origine, destination, date):
    URL_TGVMAX = "https://data.sncf.com/api/records/1.0/search/?dataset=tgvmax&q=&facet=date&facet=origine&facet=destination&facet=od_happy_card"
    test_connect(URL_TGVMAX)

    origine = origine.upper()
    destination = destination.upper()
    
    #On va faire correspondre l'entrée "paris" avec "paris (intramuros)" qui est utilisé dans l'API 
    cities_data = {'origine': origine, 'destination': destination}
    for k, v in cities_data.items():
        if v == "PARIS":
            cities_data[k] = "PARIS (intramuros)"

    datas = {'refine.origine' : cities_data['origine'], 'refine.destination' : cities_data['destination'], 'refine.date': date}
    response = requests.get(URL_TGVMAX, params=datas)
    data_dict = response.json()

    with open("data.json", "w") as f:
        json.dump(data_dict, f, indent=4, ensure_ascii=False)
        f.close()

    responses_list = []
    trains_list = []

    for x in data_dict['records'] :
        responses_list.append(x)
    
    for i in range(len(responses_list) - 1):
        fields = data_dict['records'][i]
        datas_dict = fields['fields']
        trains_details = {"depart" : datas_dict["heure_depart"], "arrive":datas_dict["heure_arrivee"], "train":datas_dict["train_no"]}
        trains_list.append(trains_details)
    print(trains_list)
    return trains_list


