Mode d'emploi 
===============
1. avant de tester, vous devez télécharger [ce fichier](https://files.pythonhosted.org/packages/70/dc/e8c5e7983866fa4ef3fd619faa35f660b95b01a2ab62b3884f038ccab542/tensorflow-2.4.1-cp37-cp37m-manylinux2010_x86_64.whl) et le mettre dans le dossier emotion_recognition sans changer son nom. Cela donnera :
         TER_S6/emotion_recognition/tensorflow-2.4.1-cp37-cp37m-manylinux2010_x86_64.whl
2. Créer les containers en utilisant la commande 
```console
$ docker-compose build
````
3. pour lancer, il suffie d'éxecuter le fichier main.py. l'émotion détectée sera écrite dans _data/emotion.txt 

```
project
│   README.md
│   file001.txt    
│
└───folder1
│   │   file011.txt
│   │   file012.txt
│   │
│   └───subfolder1
│       │   file111.txt
│       │   file112.txt
│       │   ...
│   
└───folder2
    │   file021.txt
    │   file022.txt
```

