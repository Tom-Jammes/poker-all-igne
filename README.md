# POKER ALL-IGNE
Jeu de poker en ligne entre amis 

## Installation du projet
Executer cette commande : 
```
docker-compose up -d --build
```

Puis pour initialiser la base de données : 
```
docker exec -it poker-all-igne-web-1 flask init-db
```

## Modificiation de la base de données
Afin de pouvoir effectuer une modification vous devez au préalable initialiser
le système de migration une première fois avec cette commande : 
```
docker exec -it poker-all-igne-web-1 flask db init
```

Lors d'une modificiation de la base de données il faut créer une 
migration grâce à cette commande
```
docker exec -it poker-all-igne-web-1 flask db migrate -m "nom_de_la_modification_apporté"
```
Puis appliquez votre migration
```
docker exec -it poker-all-igne-web-1 flask db upgrade
```
Vous devez ensuite redémarer le container web 
```
docker-compose restart web
```