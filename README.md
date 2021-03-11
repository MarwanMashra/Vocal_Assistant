Mode d'emploi 
===============
1. Télécharger [ce fichier](https://files.pythonhosted.org/packages/70/dc/e8c5e7983866fa4ef3fd619faa35f660b95b01a2ab62b3884f038ccab542/tensorflow-2.4.1-cp37-cp37m-manylinux2010_x86_64.whl) et le mettre dans le dossier emotion_recognition sans changer son nom. Cela donnera :
```
TER_S6
│
|─── emotion_recognition
│   │---tensorflow-2.4.1-cp37-cp37m-manylinux2010_x86_64.whl
```
2. Créer les containers en utilisant la commande 
```
$ docker-compose build
````
3. Tester avec 
```
$ python ./main.py
```




