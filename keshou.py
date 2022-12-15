import requests, json

# URL compte
debuturlACCOUNT = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
urlACCOUNT = debuturlACCOUNT + name + "?api_key=" + api_key

# request url des infos
response1 = requests.get(urlACCOUNT)


#id
summonerId = response1.json()['id']
accountId = response1.json()['accountId']
puuid = response1.json()['puuid']

#liste de matchs depuis URL puuid
debuturlLISTEMATCHS = "https://europe.api.riotgames.com/lol/match/v5/match/by-puuid/"
urlLISTEMATCHS = debuturlLISTEMATCHS + puuid + "/ids?start=0&count="+ nbGames + "&api_key=" + api_key

# resquest liste des matchs 
response2 = requests.get(urlLISTEMATCHS)

response2.json()
