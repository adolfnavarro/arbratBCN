from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://adolfnavarro:holamundo1984@cluster0.xfpk27l.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Conectem a la db   
db=client.get_database('arbres_barcelona')
coleccioArbres=db.arbres



# Funcions varies
def afegirArbre(nom_cientific,nom_catala,nom_espanyol,adreça):
    nou_arbre={
        "Nom_científic":nom_cientific,
        "Nom_català":nom_catala,
        "Nom_espanyol":nom_espanyol,
        "Adreça":adreça
    }
    coleccioArbres.insert_one(nou_arbre)
    print("Arbre insertat")   

def printArbre(arbre):
    print(f"Adreça : ",arbre["Adreça"])
    print(f"Nom cientific : ",arbre["Nom_científic"])
    print(f"Nom català : ",arbre["Nom_català"])
    print(f"Nom espanyol : ",arbre["Nom_espanyol"])
      
def escollirCamp():
    print("1 - Nom cientific : ")
    print("2 - Nom català : ")
    print("3 - Nom espanyol : ")
    print("4 - Adreça : ")
    opcio=666
    while opcio>4 or opcio<0:
        opcio=int(input("\nEscull la opció  (1-4) : "))
    if opcio==1:
        camp="Nom_científic"
    elif opcio==2:
        camp="Nom_català"
    elif opcio==3:
        camp="Nom_espanyol"
    elif opcio==4:
        camp="Adreça"
    return camp


    
menu=666
nom_cientific=""
nom_catala=""
nom_espanyol=""
adreça=""

# Programa menu
while menu!="0":
    print("\n------Arbrat de Barcelona-------")
    print("1-Afegir arbre")
    print("2-Esborrar arbre")
    print("3-Modificar arbre/s")
    print("4-LListar arbres per adreça")
    print("5-Cerca del número d’arbres d’un mateix tipus (nom català) ")
    print("6-Cerca dels arbres de la col·lecció que inclouen un cert text")
    print("7-Reinicia la base de dades amb els arbres per defecte")  
    print("0-Sortir")
    menu=input("Escull opció (0-6) : ")
    
    if menu=="1":
        nom_cientific=input("Nom cientific : ")
        nom_catala=input("Nom catala : ")
        nom_espanyol=input("Nom espanyol : ")
        adreça=input("Adreça : ")
        afegirArbre(nom_cientific,nom_catala,nom_espanyol,adreça)
    elif menu=="2":
        nom_cientific=input("Digues el nom cientific de l' arbre que vols borrar ? ")
        coleccioArbres.delete_one({"Nom_científic": nom_cientific})
    elif menu=="3":
        print("\nPer quin camp vols filtrar els arbres a modificar ? ")
        campCercar=escollirCamp()
        textCercar=input("\nQue hi posa en aquest camp ?")
        print("\nQuin camp vols modificar ? ")
        campModificar=escollirCamp()
        textNou=input("\nQue hi vols posar ?")
        coleccioArbres.update_many({campCercar: textCercar},{"$set": {campModificar: textNou}})
              
    elif menu=="4":
        llistaArbres=list(coleccioArbres.find())
        contadorArbres=1
        for arbre in llistaArbres:
            print(f"\n -------- Arbre num : {contadorArbres}---------")
            printArbre(arbre)
            contadorArbres=contadorArbres+1
    elif menu=="5":
        nom_catala=input("\n Digues el nom en català de l' arbre que vols cercar ? ")
        numArbres = coleccioArbres.count_documents({"Nom_català": nom_catala})
        print(f"Número d' arbres {nom_catala} trobats : {numArbres}")
    elif menu=="6":
        textAbuscar=input("Escriu el text que vols buscar :")
        coleccioArbres.create_index([("$**", "text")])  # Creem un index que s' aplica a tots els camps 
        llistaArbres = coleccioArbres.find({"$text": {"$search": textAbuscar}})
        contadorArbres=1
        for arbre in llistaArbres:
            print(f"\n -------- Arbre num : {contadorArbres}---------")
            printArbre(arbre)
            contadorArbres=contadorArbres+1
    elif menu=="7":
        # Per a reiniciar la base de dades:
        #Borrem tots els registres 
        coleccioArbres.delete_many({})
        # Afegim varios registres d' arbres de la web  https://jjvidalmac.carto.com/viz/c3c54164-7fcf-11e4-b04f-0e853d047bba/public_map
        afegirArbre("Populus nigra","Àlamo negro","Alamo negro","C\ Marina, 111")
        afegirArbre("Celtis australis","Lledoner","Almez","C\ Almogàvers, 56")
        afegirArbre("Brachychiton populneum","Arbre ampolla","Árbol botella","C\ Pere IV, 29")
        afegirArbre("Populus alba","Àlber","ólamo blanco","C\ Bisbe Josep Climent")
                
    

