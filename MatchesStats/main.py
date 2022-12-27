import requests, json
# Variables globales
api_key ="RGAPI-e5852235-5284-4041-b3ca-278c7944a9f2"
nameCompte= "MentaIiyah Ill"
nbGamesINIT = "30"
selfInclus = False     #True ou false
typegame = ""        # 0=Flex+soloq, 1=soloq, 2=flex


#Fonctions

def kda(kills, deaths, assists):
    if deaths == 0:
        return kills + assists
    else:
        return (kills + assists) / deaths



def moyenne(values):
  return sum(values) / len(values)


def isInclus():
    if selfInclus == True:
        return "Oui"
    else:
        return "Non"



def exec(name,file):
    if file == "Soloq":
        typegame=1
    if file == "Flex":
        typegame=2
    if file == "Flex+Soloq":
        typegame=0
    if file == "Aram":
        typegame=3
    #Variables poubelles
    global nbSOLOQ, nbFLEX
    nbSOLOQ=0
    nbFLEX=0
    nbARAM=0
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
    urlLISTEMATCHS = debuturlLISTEMATCHS + puuid + "/ids?start=0&count="+ nbGamesINIT + "&api_key=" + api_key

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
    KdaMoi=[]
    #url d'un match,    queueId soloqueue : 420      queueId flex : 440     queueId Aram : 450
    for idmatch in listeMatchs:
        debuturlSTATSMATCH= "https://europe.api.riotgames.com/lol/match/v5/matches/"
        urlSTATSMATCH = debuturlSTATSMATCH + idmatch + "?api_key=" + api_key
        # request stats d'un match 

        response3 = requests.get(urlSTATSMATCH)
        response3 = response3.json()
        if typegame ==0 :
            #print(urlSTATSMATCH)                        #AFFICHAGEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE URL MATCH
            #PARSER STATS DE CHAQUE PARTICIPANT
            if response3['info']['queueId']==420 or response3['info']['queueId']==440 :    # SOLOQ + FLEX
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

                if selfInclus == False:
                    if teamAlliée['jungle']['summonerName'] != name:
                        KdaJglAlly.append(kda(teamAlliée['jungle']['kills'],teamAlliée['jungle']['deaths'],teamAlliée['jungle']['assists']))
                        KdaJglEnnemy.append(kda(teamEnnemie['jungle']['kills'],teamEnnemie['jungle']['deaths'],teamEnnemie['jungle']['assists']))               
                        
                else:
                    KdaJglAlly.append(kda(teamAlliée['jungle']['kills'],teamAlliée['jungle']['deaths'],teamAlliée['jungle']['assists']))
                    KdaJglEnnemy.append(kda(teamEnnemie['jungle']['kills'],teamEnnemie['jungle']['deaths'],teamEnnemie['jungle']['assists']))
                if response3['info']['queueId'] == 420:
                    nbSOLOQ = nbSOLOQ+1
                elif response3['info']['queueId'] == 440:
                    nbFLEX = nbFLEX+1     
                    
        if typegame==1:    
            if response3['info']['queueId']==420 :    # ONLY SOLOQ 
                #print(urlSTATSMATCH)                        #AFFICHAGEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE URL MATCH
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

                if selfInclus == False:
                    if teamAlliée['jungle']['summonerName'] != name:
                        KdaJglAlly.append(kda(teamAlliée['jungle']['kills'],teamAlliée['jungle']['deaths'],teamAlliée['jungle']['assists']))
                        KdaJglEnnemy.append(kda(teamEnnemie['jungle']['kills'],teamEnnemie['jungle']['deaths'],teamEnnemie['jungle']['assists']))
                    
                else:
                    KdaJglAlly.append(kda(teamAlliée['jungle']['kills'],teamAlliée['jungle']['deaths'],teamAlliée['jungle']['assists']))
                    KdaJglEnnemy.append(kda(teamEnnemie['jungle']['kills'],teamEnnemie['jungle']['deaths'],teamEnnemie['jungle']['assists']))
                nbSOLOQ+=1
                    
            
        if typegame==2:
            if response3['info']['queueId']==440 : # ONLY FLEX
                #print(urlSTATSMATCH)                        #AFFICHAGEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE URL MATCH
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

                if selfInclus == False:
                    if teamAlliée['jungle']['summonerName'] != name:
                        KdaJglAlly.append(kda(teamAlliée['jungle']['kills'],teamAlliée['jungle']['deaths'],teamAlliée['jungle']['assists']))
                        KdaJglEnnemy.append(kda(teamEnnemie['jungle']['kills'],teamEnnemie['jungle']['deaths'],teamEnnemie['jungle']['assists']))                  
                else:
                    KdaJglAlly.append(kda(teamAlliée['jungle']['kills'],teamAlliée['jungle']['deaths'],teamAlliée['jungle']['assists']))
                    KdaJglEnnemy.append(kda(teamEnnemie['jungle']['kills'],teamEnnemie['jungle']['deaths'],teamEnnemie['jungle']['assists']))
                nbFLEX+=1
        
        if typegame==3:
            if response3['info']['queueId']==450 : # ONLY ARAM
                #print(urlSTATSMATCH)                        #AFFICHAGEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE URL MATCH
                #PARSER STATS DE CHAQUE PARTICIPANT
                numMoi = 0
                nombreGames += 1
                while response3['info']['participants'][numMoi]['summonerName'].lower()!=name.lower() :
                    numMoi = numMoi + 1
                    KdaMoi.append(kda(response3['info']['participants'][numMoi]['kills'],response3['info']['participants'][numMoi]['deaths'],response3['info']['participants'][numMoi]['assists']))
                nbARAM+=1

    #complétion fichier txt 
    f = open('mon_fichier.txt', 'w')

    if typegame == 0:
        chaine = "Moyenne de KDA des junglers, analyse des : " + nbGamesINIT + " dernières games de " + name + " comprenant "+str(nbSOLOQ)+" Soloq et : "+str(nbFLEX)+" Flex" + "\nJungle allié : " + str(moyenne(KdaJglAlly))+ "\nJungle ennemi :" + str(moyenne(KdaJglEnnemy))
        f.write(chaine)
    if typegame == 1:
        chaine = "Moyenne de KDA des junglers, analyse des : " + nbGamesINIT + " dernières games de " + name + " comprenant "+str(nbSOLOQ)+" Soloq" + "\nJungle allié : " + str(moyenne(KdaJglAlly))+ "\nJungle ennemi :" + str(moyenne(KdaJglEnnemy))
        f.write(chaine)
    if typegame == 2:
        chaine = "Moyenne de KDA des junglers, analyse des : " + nbGamesINIT + " dernières games de " + name + " comprenant "+str(nbFLEX)+" Flex" "\nJungle allié : " + str(moyenne(KdaJglAlly))+ "\nJungle ennemi :" + str(moyenne(KdaJglEnnemy))
        f.write(chaine)
    if typegame == 3:
        chaine = "Analyse des :" + nbGamesINIT + " dernières games de " + name + " qui a joué "+str(nbARAM)+" ARAMs" "\nLa moyenne de son KDA est de: " + str(moyenne(KdaMoi))
        f.write(chaine)
    print(chaine)
    f.close()

