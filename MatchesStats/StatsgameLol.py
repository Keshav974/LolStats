import requests, json
# Variables globales
api_key ="RGAPI-0a5eb06f-3773-4999-ae0b-2995a59b150a"
name= "GrinchDx"
nbGames = "20"
# URL compte
debuturlACCOUNT = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
urlACCOUNT = debuturlACCOUNT + name + "?api_key=" + api_key

# request url des infos
response1 = requests.get(urlACCOUNT)


#id
summonerId = response1.json()['id']
accountId = response1.json()['accountId']
puuid = response1.json()['puuid']

#lurl de matchs depuis URL puuid
debuturlLISTEMATCHS = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"
urlLISTEMATCHS = debuturlLISTEMATCHS + puuid + "/ids?start=0&count="+ nbGames + "&api_key=" + api_key

"""
print(urlLISTEMATCHS)    
"""

# request liste des matchs 
response2 = requests.get(urlLISTEMATCHS)

"""
print(response2.json())
"""
#REMPLISSAGE MATCHS
listeMatchs = response2.json()
#print(listeMatchs) 

KdaJglAllyO = []
KdaJglEnnemyO= []
KdaJglAlly = []
KdaJglEnnemy= []
nombreGames = 0
 #url d'un match,    queueId soloqueue : 420      queueId flex : 440     queueId Aram : 450
for idmatch in listeMatchs:
    debuturlSTATSMATCH= "https://europe.api.riotgames.com/lol/match/v5/matches/"
    urlSTATSMATCH = debuturlSTATSMATCH + idmatch + "?api_key=" + api_key
    # request stats d'un match 

    response3 = requests.get(urlSTATSMATCH)
    response3 = response3.json()
    if response3['info']['queueId']==420 or response3['info']['queueId']==440 :    # SOLOQ + FLEX
    #if response3['info']['queueId']==420 :    # ONLY SOLOQ 
    #if response3['info']['queueId']==440 : # ONLY FLEX    
        print(urlSTATSMATCH)                        #AFFICHAGEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE URL MATCH
        #PARSER STATS DE CHAQUE PARTICIPANT
        numMoi = 0
        nombreGames += 1
        while response3['info']['participants'][numMoi]['summonerName'].lower()!=name.lower() :
            numMoi = numMoi + 1
            if numMoi<5:
                teamAlliée= {'top' : response3['info']['participants'][0],'jungle': response3['info']['participants'][1],"mid": response3['info']['participants'][2],"adc":response3['info']['participants'][3],"support":response3['info']['participants'][4]}
                teamEnnemie= {'top' : response3['info']['participants'][5],'jungle': response3['info']['participants'][6],"mid": response3['info']['participants'][7],"adc":response3['info']['participants'][8],"support":response3['info']['participants'][9]}
            else :
                teamAlliée={'top' : response3['info']['participants'][5],'jungle': response3['info']['participants'][6],"mid": response3['info']['participants'][7],"adc":response3['info']['participants'][8],"support":response3['info']['participants'][9]}
                teamEnnemie={'top' : response3['info']['participants'][0],'jungle': response3['info']['participants'][1],"mid": response3['info']['participants'][2],"adc":response3['info']['participants'][3],"support":response3['info']['participants'][4]}

        def kda(kills, deaths, assists):
            if deaths == 0:
                return kills + assists
            else:
                return (kills + assists) / deaths

        KdaJglAlly.append(kda(teamAlliée['jungle']['kills'],teamAlliée['jungle']['deaths'],teamAlliée['jungle']['assists']))
        KdaJglEnnemy.append(kda(teamEnnemie['jungle']['kills'],teamEnnemie['jungle']['deaths'],teamEnnemie['jungle']['assists']))


def moyenne(values):
  return sum(values) / len(values)


print(moyenne(KdaJglAlly))
print(moyenne(KdaJglEnnemy))









#complétion fichier txt 
f = open('mon_fichier.txt', 'w')


chaine = "Kda des fils de putes de junglers dans les " + str((nombreGames)) + " dernières soloqueue de " + name + "\nJungle allié : " + str(moyenne(KdaJglAlly))+ "\nJungle ennemi :" + str(moyenne(KdaJglEnnemy))
f.write(chaine)

f.close()
