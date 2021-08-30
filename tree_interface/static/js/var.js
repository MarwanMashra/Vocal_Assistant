mtree = {
    "tag": "start",
    "keywords": [],
    "text": [
        [
            "Comment puis-je vous aider ?",
            "Je peux vous aider ?",
            "Avez-vous besoin de quelque chose ?",
            "Demandez-moi ce que vous voulez",
            "Dites-moi ce que vous voulez que je fasse",
            "Donnez-moi des ordres",
            "Qu'est-ce que je peux faire pour vous ?",
            "Dites-moi ce dont vous avez besoin"
        ]
    ],
    "action": "listen",
    "context": "",
    "next": [
        {
            "tag": "start>face",
            "keywords": [
                "facial"
            ],
            "text": [
                [
                    "on s'est déjà rencontré ?",
                    "Votre visage me dit quelque chose",
                    "vous me dites quelque chose",
                    "peut-être que je vous connais déjà"
                ],
                [
                    "Puis-je vous voir un peu ?",
                    "Je peux jeter un coup d'oeil de plus près?",
                    "Puis-je vous regarder via le webcam ?"
                ]
            ],
            "action": "listen",
            "context": "",
            "next": [
                {
                    "tag": "start>face>yes",
                    "keywords": [
                        "oui",
                        "yes",
                        "ouais"
                    ],
                    "text": [
                        [
                            "Regardez le webcam",
                            "Souriez pour le webcam",
                            "Je prend une photo maintenant",
                            "Montrez-moi votre sourire",
                            "Dites cheese"
                        ]
                    ],
                    "action": "face_recognizer",
                    "context": "",
                    "next": [
                        {
                            "tag": "start>face>yes>known",
                            "keywords": [
                                "known"
                            ],
                            "text": [
                                [
                                    "Ah oui, vous êtes {context}",
                                    "Je savais, vous êtes {context}",
                                    "Salut {context}",
                                    "Ah c'est vous {context}",
                                    "{context} je vous ai reconnu",
                                    "{context} je vous ai repéré",
                                    "Oui c'est {context}, mes yeux ne se trompent jamais"
                                ]
                            ],
                            "action": "None",
                            "context": "",
                            "next": [
                                "start"
                            ],
                            "config": []
                        },
                        {
                            "tag": "start>face>yes>unknown",
                            "keywords": [
                                "unknown"
                            ],
                            "text": [
                                [
                                    "Ah non, on s'est pas rencontré",
                                    "Ah non, je vous ai confondu avec la lune",
                                    "Désolé, je vous connais pas, je n'ai pas une si bonne mémoire apparemment"
                                ],
                                [
                                    "en tout cas, enchanté",
                                    "Je suis heureux de vous rencontrer"
                                ],
                                [
                                    "on m'appelle Chatbot",
                                    "Moi, je suis Chatbot",
                                    "on m'appelle Chatbot",
                                    "Moi, je suis votre assistant"
                                ]
                            ],
                            "action": "None",
                            "context": "",
                            "next": [
                                "start"
                            ],
                            "config": []
                        }
                    ],
                    "config": []
                },
                {
                    "tag": "start>face>no",
                    "keywords": [
                        "non",
                        "no"
                    ],
                    "text": [
                        [
                            "ok",
                            "pas de souci",
                            "ça marche"
                        ],
                        [
                            "Vous êtes timide",
                            "Vous semblez être timide",
                            "Je suis heureux de vous rencontrez en tout cas",
                            "je me suis peut-être trompé"
                        ]
                    ],
                    "action": "None",
                    "context": [],
                    "next": [
                        "start"
                    ],
                    "config": []
                }
            ],
            "config": []
        },
        {
            "tag": "start>emotion",
            "keywords": [
                "émotion",
                "sentiment",
                "enervé",
                "dégoûté",
                "apeuré",
                "heureux",
                "joyeux",
                "triste",
                "surpris",
                "neutre"
            ],
            "text": [
                [
                    "Je suis capable de détecter votre émotion",
                    "Je peux détecter votre émotion si vous voulez",
                    "La détection des émotions va commencer",
                    "La reconnaissance des émotions va commencer",
                    "Je peux reconnaître votre émotion",
                    "Je sais reconnaître les émotions",
                    "Je suis capable de reconnaître les émotions",
                    "Je sais faire de la reconnaissance des émotions"
                ],
                [
                    "Puis-je vous voir visage?",
                    "Je peux jeter un coup d'oeil de plus près?",
                    "Puis-je vous regarder via le webcam ?"
                ]
            ],
            "action": "listen",
            "context": "",
            "next": [
                {
                    "tag": "start>emotion>yes",
                    "keywords": [
                        "oui",
                        "yes",
                        "ouais"
                    ],
                    "text": [
                        [
                            "Regardez le webcam",
                            "Ouverture du webcam",
                            "J'ouvre le webcam"
                        ]
                    ],
                    "action": "emotion_recognition",
                    "context": "",
                    "next": [
                        {
                            "tag": "start>emotion>yes>known",
                            "keywords": [
                                "known"
                            ],
                            "text": [
                                [
                                    "vous avez l'aire {context} aujourd'hui",
                                    "hmmm, je pense que vous êtes {context} aujourd'hui",
                                    "ça me semble que vous êtes {context} aujourd'hui",
                                    "Vous me sembler {context} aujourd'hui",
                                    "je ne suis pas sûr mais je crois que vous êtes {context} aujourd'hui"
                                ]
                            ],
                            "action": "None",
                            "context": "",
                            "next": [
                                "start"
                            ],
                            "config": []
                        },
                        {
                            "tag": "start>emotion>yes>unknown",
                            "keywords": [
                                "unknown"
                            ],
                            "text": [
                                [
                                    "Délosée",
                                    "Je suis désolée",
                                    "Excusez-moi",
                                    "Oups",
                                    "Veuillez m'excuser"
                                ],
                                [
                                    "Je n'ai pas pu reconnaître votre émotion",
                                    "Votre émotion n'a pas pu être reconnue"
                                ],
                                [
                                    "Peut-être votre visage n'apparaît pas en entier ou il n'y a pas assez de lumière"
                                ],
                                [
                                    "Vous voulez que je réessaye ?",
                                    "Je peux réessayer ?",
                                    "Puis je réessayer ?",
                                    "Souhaitez-vous que je le refais ?",
                                    "Voulez-vous que je le refais ?"
                                ]
                            ],
                            "action": "listen",
                            "context": "",
                            "next": [
                                "start>emotion>yes",
                                "start>emotion>no"
                            ],
                            "config": []
                        }
                    ],
                    "config": []
                },
                {
                    "tag": "start>emotion>no",
                    "keywords": [
                        "non",
                        "no"
                    ],
                    "text": [
                        [
                            "Ok, pas de souci",
                            "ça marche",
                            "ok"
                        ]
                    ],
                    "action": "None",
                    "context": "",
                    "next": [
                        "start"
                    ],
                    "config": []
                }
            ],
            "config": []
        },
        {
            "tag": "start>face_register",
            "keywords": [
                "enregistrer"
            ],
            "text": [
                [
                    "Je peux",
                    "Puis-je",
                    "est-ce que je peux",
                    "M'autorisez-vous à",
                    "est-ce que vous me permettez de",
                    "est-ce que vous me autorisez à"
                ],
                [
                    "ouvrir le webcam",
                    "voir votre visage via le webcam",
                    "jeter un coup d'oeil via le webcam ?",
                    "vous regarder rapidement via le webcam"
                ]
            ],
            "action": "listen",
            "context": "",
            "next": [
                {
                    "tag": "start>face_register>yes",
                    "keywords": [
                        "oui",
                        "yes",
                        "ouais"
                    ],
                    "text": [
                        [
                            "Regardez le webcam",
                            "Ouverture du webcam",
                            "J'ouvre le webcam"
                        ]
                    ],
                    "action": "face_register",
                    "context": "",
                    "next": [
                        {
                            "tag": "start>face_register>succes",
                            "keywords": [
                                "succes"
                            ],
                            "text": [
                                [
                                    "Votre visage a été enregistré",
                                    "C'est fait, j'arrive à vous reconnaître maintenant"
                                ]
                            ],
                            "action": "None",
                            "context": "",
                            "next": [
                                "start"
                            ],
                            "config": []
                        },
                        {
                            "tag": "start>face_register>fail",
                            "keywords": [
                                "fail"
                            ],
                            "text": [
                                [
                                    "Délosée",
                                    "Je suis désolée",
                                    "Excusez-moi",
                                    "Oups",
                                    "Veuillez m'excuser"
                                ],
                                [
                                    "Je n'ai pas pu enregistrer votre visage",
                                    "L'opération a échoué",
                                    "Un problème s'est produit"
                                ],
                                [
                                    "Vous voulez que je réessaye ?",
                                    "Je peux réessayer ?",
                                    "Puis je réessayer ?",
                                    "Souhaitez-vous que je le refais ?",
                                    "Voulez-vous que je le refais ?"
                                ]
                            ],
                            "action": "listen",
                            "context": "",
                            "next": [
                                "start>face_register>yes",
                                "start>face_register>no"
                            ],
                            "config": []
                        }
                    ],
                    "config": []
                },
                {
                    "tag": "start>face_register>no",
                    "keywords": [
                        "non",
                        "no"
                    ],
                    "text": [
                        [
                            "Ok, pas de souci",
                            "ça marche",
                            "ok"
                        ]
                    ],
                    "action": "None",
                    "context": "",
                    "next": [
                        "start"
                    ],
                    "config": []
                }
            ],
            "config": []
        },
        {
            "tag": "start>google",
            "keywords": [
                "chercher",
                "google",
                "recherche",
                "rechercher"
            ],
            "text": [
                [
                    "Que voulez-vous chercher ?",
                    "Ok, qu'est-ce que je dois chercher ?",
                    "Dites moi ce que je dois chercher"
                ]
            ],
            "action": "google",
            "context": "",
            "next": [
                "start"
            ],
            "config": [
                "screen"
            ]
        },
        {
            "tag": "start>youtube",
            "keywords": [
                "youtube",
                "vidéo"
            ],
            "text": [
                [
                    "Quelle vidéo vous voulez voir ?",
                    "Quelle vidéo vous voulez chercher ?",
                    "Ok, qu'est-ce que vous voulez chercher sur YouTube ?"
                ]
            ],
            "action": "youtube",
            "context": "",
            "next": [
                "start"
            ],
            "config": [
                "screen"
            ]
        },
        {
            "tag": "start>stop",
            "keywords": [
                "fermer",
                "fermeture",
                "annuler",
                "annulation",
                "arrêter",
                "arrêt",
                "terminer",
                "quitter",
                "fin"
            ],
            "text": [],
            "action": "stop",
            "context": "",
            "next": [
                "start"
            ],
            "config": []
        }
    ],
    "config": [],
}

mmodel = { "class": "go.TreeModel",
                        "nodeDataArray": [
                        {"key":1, "name":"Stella Payne Diaz", "title":"CEO", "parent":0},
                        {"key":2, "name":"Luke Warm", "title":"VP Marketing/Sales", "parent":1},
                        {"key":3, "name":"Meg Meehan Hoffa", "title":"Sales", "parent":2},
                        {"key":4, "name":"Peggy Flaming", "title":"VP Engineering", "parent":1},
                        {"key":5, "name":"Saul Wellingood", "title":"Manufacturing", "parent":4},
                        {"key":6, "name":"Al Ligori", "title":"Marketing", "parent":2},
                        {"key":7, "name":"Dot Stubadd", "title":"Sales Rep", "parent":3},
                        {"key":8, "name":"Les Ismore", "title":"Project Mgr", "parent":5},
                        {"key":9, "name":"April Lynn Parris", "title":"Events Mgr", "parent":6},
                        {"key":10, "name":"Xavier Breath", "title":"Engineering", "parent":4},
                        {"key":11, "name":"Anita Hammer", "title":"Process", "parent":5},
                        {"key":12, "name":"Billy Aiken", "title":"Software", "parent":10},
                        {"key":13, "name":"Stan Wellback", "title":"Testing", "parent":10},
                        {"key":14, "name":"Marge Innovera", "title":"Hardware", "parent":10},
                        {"key":15, "name":"Evan Elpus", "title":"Quality", "parent":5},
                        {"key":16, "name":"Lotta B. Essen", "title":"Sales Rep", "parent":3}
                        ]
                        }


info={
    name:"Le nom doit être court, sans '<' ni '>' et de préférence sans espace. Deux noueds du même père ne peuvent pas avoir le même nom. ",
    keywords:"L'algorithme cherchera ces mots clés dans la requête de l'utilisateur pour déterminer si ce noeud doit être le prochain (en cas de l'action 'listen'). ",
    action:"L'action principale à exécuter, par exemple l'action 'listen' pour écouter la demande de l'utilisateur. À Laisser vide si aucune action n'est nécessaire. Par exemple: L'action 'listen' permet de recevoir une demande de l'utilisateur et de chercher les mots clés dedans.",
    text:"Ce que l'application va dire à l'utilisateur au début de chaque noeud. Il est composé d'une ou plusieurs parties (appuyer sur '+' pour ajouter une partie). Chaque partie consiste à plusieurs phrases parmis lesquelles, l'application choisirait une aléatoirement. ",
    screen:"À cocher si cette scénario nécissite que l'application soit en mode écran.",
    next:"La possibilité d'ajouter des noeuds existants comme enfants. "
}