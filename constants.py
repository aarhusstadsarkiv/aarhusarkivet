SESSION_KEY = 'profile'

ICONS = {
    "61": {"icon": "far fa-image", "label": "Billeder"},
    "95": {"icon": "fas fa-laptop", "label": "Elektronisk materiale"},
    "10": {"icon": "fas fa-gavel", "label": "Forskrifter og vedtægter"},
    "1": {"icon": "far fa-folder-open", "label": "Kommunale sager og planer"},
    "75": {"icon": "far fa-map", "label": "Kortmateriale"},
    "49": {"icon": "far fa-file-alt", "label": "Manuskripter"},
    "87": {"icon": "fas fa-film", "label": "Medieproduktioner"},
    "81": {"icon": "fas fa-music", "label": "Musik og lydoptagelser"},
    "36": {"icon": "fas fa-book", "label": "Publikationer"},
    "18": {"icon": "fab fa-leanpub", "label": "Registre og protokoller"},
    "29": {"icon": "far fa-chart-bar", "label": "Statistisk og økonomisk materiale"},
    "99": {"icon": "far fa-file", "label": "Andet materiale"},
}

STATIC_PAGES = [
    "robots.txt",
    "BingSiteAuth.xml",
    "google46a7bae009a5abed.html"
]

ABOUT_PAGES = [
    "collections",
    "availability",
    "usability",
    "cookies",
    "privacy",
    "archival_availability",
]

RESOURCE_PAGES = [
    "records",
    "people",
    "locations",
    "organisations",
    "events",
    "objects",
    "collections",
    "creators",
    "collectors",
]

GUIDE_PAGES = ["searchguide", "genealogy", "municipality_records"]

VOCAB_PAGES = ["availability", "usability", "content_types", "subjects"]

FACETS = {
    'content_types': {
        'label': 'Materialetype',
        'multiple': True,
        'hierarchical': True,
        'content': [
            {
                "id": u"99",
                "label": u"Andet materiale"
            },
            {
                "children": [
                  {
                    "id": u"66",
                    "icon": "far fa-image",
                    "label": u"Afbildning af arkitektur og bygning"
                  },
                  {
                    "id": u"65",
                    "icon": "far fa-image",
                    "label": u"Afbildning af kunst"
                  },
                  {
                    "id": u"73",
                    "icon": "far fa-image",
                    "label": u"Arkitekturtegning"
                  },
                  {
                    "id": u"64",
                    "icon": "far fa-image",
                    "label": u"By- og gadebilleder"
                  },
                  {
                    "id": u"70",
                    "icon": "far fa-image",
                    "label": u"Collage"
                  },
                  {
                    "id": u"71",
                    "icon": "far fa-image",
                    "label": u"Illustrationer"
                  },
                  {
                    "id": u"100",
                    "icon": "far fa-image",
                    "label": u"Landskabs- og naturbilleder"
                  },
                  {
                    "id": u"62",
                    "icon": "far fa-image",
                    "label": u"Luftfoto"
                  },
                  {
                    "id": u"68",
                    "icon": "far fa-image",
                    "label": u"Maleri"
                  },
                  {
                    "id": u"67",
                    "icon": "far fa-image",
                    "label": u"Plakat"
                  },
                  {
                    "id": u"69",
                    "icon": "far fa-image",
                    "label": u"Planche"
                  },
                  {
                    "id": u"63",
                    "icon": "far fa-image",
                    "label": u"Portræt"
                  },
                  {
                    "id": u"74",
                    "icon": "far fa-image",
                    "label": u"Postkort"
                  },
                  {
                    "id": u"72",
                    "icon": "far fa-image",
                    "label": u"Tekniske tegninger"
                  }
                ],
                "id": u"61",
                "icon": u"far fa-image",
                "label": u"Billeder"
              },
              {
                "children": [
                  {
                    "id": u"98",
                    "icon": u"fas fa-laptop",
                    "label": u"Hjemmesider"
                  },
                  {
                    "id": u"96",
                    "icon": u"fas fa-laptop",
                    "label": u"Software"
                  },
                  {
                    "id": u"97",
                    "icon": u"fas fa-laptop",
                    "label": u"Spil"
                  }
                ],
                "id": u"95",
                "icon": u"fas fa-laptop",
                "label": u"Elektronisk materiale"
              },
              {
                "children": [
                  {
                    "description": u"Skøder, pantebreve, forpagtningskontrakter, m.m.",
                    "id": u"13",
                    "icon": u"fas fa-gavel",
                    "label": u"Ejendomspapirer"
                  },
                  {
                    "id": u"12",
                    "icon": u"fas fa-gavel",
                    "label": u"Kontrakter"
                  },
                  {
                    "id": u"16",
                    "icon": u"fas fa-gavel",
                    "label": u"Love og cirkulærer"
                  },
                  {
                    "id": u"15",
                    "icon": u"fas fa-gavel",
                    "label": u"Regulativer"
                  },
                  {
                    "id": u"11",
                    "icon": u"fas fa-gavel",
                    "label": u"Retningslinier"
                  },
                  {
                    "id": u"17",
                    "icon": u"fas fa-gavel",
                    "label": u"Standarder og specifikationer"
                  },
                  {
                    "id": u"14",
                    "icon": u"fas fa-gavel",
                    "label": u"Vedtægter"
                  }
                ],
                "id": u"10",
                "icon": u"fas fa-gavel",
                "label": u"Forskrifter og vedtægter"
              },
              {
                "children": [
                  {
                    "id": u"5",
                    "icon": u"far folder-open",
                    "label": u"Borgersager"
                  },
                  {
                    "id": u"2",
                    "icon": u"far folder-open",
                    "label": u"Bygge- og ejendomssager"
                  },
                  {
                    "id": u"8",
                    "icon": u"far folder-open",
                    "label": u"By- og lokalplaner"
                  },
                  {
                    "id": u"7",
                    "icon": u"far folder-open",
                    "label": u"Byråds- og udvalgssager"
                  },
                  {
                    "id": u"4",
                    "icon": u"far folder-open",
                    "label": u"Emnesager"
                  },
                  {
                    "id": u"9",
                    "icon": u"far folder-open",
                    "label": u"Kommunalplaner"
                  },
                  {
                    "id": u"6",
                    "icon": u"far folder-open",
                    "label": u"Personalesager"
                  },
                  {
                    "id": u"3",
                    "icon": u"far folder-open",
                    "label": u"Vej og område, kulturmiljøsager"
                  }
                ],
                "id": u"1",
                "icon": u"far folder-open",
                "label": u"Kommunale sager og planer"
              },
              {
                "children": [
                  {
                    "id": u"80",
                    "icon": u"far fa-map",
                    "label": u"Diagram"
                  },
                  {
                    "id": u"76",
                    "icon": u"far fa-map",
                    "label": u"Matrikelkort"
                  },
                  {
                    "id": u"79",
                    "icon": u"far fa-map",
                    "label": u"Tekniske kort"
                  },
                  {
                    "id": u"77",
                    "icon": u"far fa-map",
                    "label": u"Topografiske kort"
                  },
                  {
                    "id": u"78",
                    "icon": u"far fa-map",
                    "label": u"Økonomiske kort"
                  }
                ],
                "id": u"75",
                "icon": u"far fa-map",
                "label": u"Kortmateriale"
              },
              {
                "description": u"upubliceret",
                "children": [
                  {
                    "description": u"upubliceret",
                    "id": u"51",
                    "icon": u"far file-alt",
                    "label": u"Afhandlinger og disputatser"
                  },
                  {
                    "description": u"upubliceret",
                    "id": u"53",
                    "icon": u"far file-alt",
                    "label": u"Eksamensopgaver"
                  },
                  {
                    "description": u"upubliceret",
                    "id": u"50",
                    "icon": u"far file-alt",
                    "label": u"Erindringer og dagbøger"
                  },
                  {
                    "description": u"upubliceret",
                    "id": u"52",
                    "icon": u"far file-alt",
                    "label": u"Forelæsningspapirer og -noter"
                  },
                  {
                    "description": u"upubliceret",
                    "id": u"56",
                    "icon": u"far file-alt",
                    "label": u"Håndbøger og manualer"
                  },
                  {
                    "description": u"upubliceret, email, chat, breve, interviews",
                    "id": u"60",
                    "icon": u"far file-alt",
                    "label": u"Korrespondance"
                  },
                  {
                    "description": u"upubliceret, skudsmålsbøger, eksamenspapirer, anbefalinger, attester, m.m.",
                    "id": u"58",
                    "icon": u"far file-alt",
                    "label": u"Personlige papirer"
                  },
                  {
                    "description": u"upubliceret, arkivalske registranter",
                    "id": u"59",
                    "icon": u"far file-alt",
                    "label": u"Registranter"
                  },
                  {
                    "description": u"upubliceret, festtaler, oratoriske taler, politiske taler m.m.",
                    "id": u"54",
                    "icon": u"far file-alt",
                    "label": u"Taler"
                  },
                  {
                    "description": u"upubliceret",
                    "id": u"57",
                    "icon": u"far file-alt",
                    "label": u"Tweets, online posts, blogs"
                  },
                  {
                    "description": u"upubliceret",
                    "id": u"55",
                    "icon": u"far file-alt",
                    "label": u"Udklip og småtryk"
                  }
                ],
                "id": u"49",
                "icon": u"far file-alt",
                "label": u"Manuskripter"
              },
              {
                "description": u"tv, radio og internet",
                "children": [
                  {
                    "description": u"tv, radio og internet",
                    "id": u"93",
                    "icon": u"fas fa-film",
                    "label": u"Animation"
                  },
                  {
                    "description": u"tv, radio og internet",
                    "id": u"89",
                    "icon": u"fas fa-film",
                    "label": u"Dokumentarer"
                  },
                  {
                    "description": u"tv, radio og internet",
                    "id": u"90",
                    "icon": u"fas fa-film",
                    "label": u"Eksperimental videokunst"
                  },
                  {
                    "description": u"tv, radio og internet",
                    "id": u"92",
                    "icon": u"fas fa-film",
                    "label": u"Fiktion og kortfilm"
                  },
                  {
                    "description": u"tv, radio og internet",
                    "id": u"91",
                    "icon": u"fas fa-film",
                    "label": u"Magasin- og nyhedsprogrammer"
                  },
                  {
                    "description": u"tv, radio og internet",
                    "id": u"94",
                    "icon": u"fas fa-film",
                    "label": u"Oplæsninger"
                  },
                  {
                    "description": u"tv, radio og internet",
                    "id": u"88",
                    "icon": u"fas fa-film",
                    "label": u"Reportager"
                  }
                ],
                "id": u"87",
                "icon": u"fas fa-film",
                "label": u"Medieproduktioner"
              },
              {
                "children": [
                  {
                    "id": u"86",
                    "label": u"Ikke-musikalsk lyd"
                  },
                  {
                    "id": u"85",
                    "label": u"Live-opførelser"
                  },
                  {
                    "id": u"82",
                    "label": u"Musikudgivelser"
                  },
                  {
                    "id": u"83",
                    "label": u"Noder"
                  },
                  {
                    "id": u"84",
                    "label": u"Sange og salmer"
                  }
                ],
                "id": u"81",
                "label": u"Musik og lydoptagelser"
              },
              {
                "children": [
                  {
                    "description": u"inkl. anmeldelser, nekrologer, opiniods, m.m.",
                    "id": u"41",
                    "icon": u"fas fa-book",
                    "label": u"Artikler og essays"
                  },
                  {
                    "description": u"inkl. diskografi, filmografi og andre værkfortegnelse",
                    "id": u"40",
                    "icon": u"fas fa-book",
                    "label": u"Bibliografier"
                  },
                  {
                    "id": u"44",
                    "icon": u"fas fa-book",
                    "label": u"Detailkataloger, reklamer, propaganda"
                  },
                  {
                    "id": u"37",
                    "icon": u"fas fa-book",
                    "label": u"Faglitteratur"
                  },
                  {
                    "description": u"Vejvisere, telefonbøger, m.m.",
                    "id": u"46",
                    "icon": u"fas fa-book",
                    "label": u"Fortegnelser"
                  },
                  {
                    "id": u"45",
                    "icon": u"fas fa-book",
                    "label": u"Kataloger og programmer for diverse"
                  },
                  {
                    "id": u"47",
                    "icon": u"fas fa-book",
                    "label": u"Nyhedsbreve og medlemsblade"
                  },
                  {
                    "id": u"43",
                    "icon": u"fas fa-book",
                    "label": u"Pjecer, pamfletter"
                  },
                  {
                    "id": u"48",
                    "icon": u"fas fa-book",
                    "label": u"Rapporter"
                  },
                  {
                    "description": u"encyklopædier, ordbøger, m.m.",
                    "id": u"39",
                    "icon": u"fas fa-book",
                    "label": u"Reference- og opslagsværker"
                  },
                  {
                    "description": u"inkl. autobiografier",
                    "id": u"38",
                    "icon": u"fas fa-book",
                    "label": u"Skønlitteratur, dramatik og poesi"
                  },
                  {
                    "description": u"magasiner, årspublikationer, periodica, m.m.",
                    "id": u"42",
                    "icon": u"fas fa-book",
                    "label": u"Tidsskrifter og aviser"
                  }
                ],
                "id": u"36",
                "icon": u"fas fa-book",
                "label": u"Publikationer"
              },
              {
                "children": [
                  {
                    "id": u"27",
                    "icon": u"fab fa-leanpub",
                    "label": u"Andre registre og protokoller"
                  },
                  {
                    "id": u"22",
                    "icon": u"fab fa-leanpub",
                    "label": u"Brandtaksationsprotokoller"
                  },
                  {
                    "description": u"Lister, medlemsfortegnelser, adressefortegnelser, navnelister, m.m.",
                    "id": u"28",
                    "icon": u"fab fa-leanpub",
                    "label": u"Diverse fortegnelser"
                  },
                  {
                    "id": u"20",
                    "icon": u"fab fa-leanpub",
                    "label": u"Dødsattester og -journaler"
                  },
                  {
                    "id": u"24",
                    "icon": u"fab fa-leanpub",
                    "label": u"Folketællinger"
                  },
                  {
                    "id": u"25",
                    "icon": u"fab fa-leanpub",
                    "label": u"Kirkebøger"
                  },
                  {
                    "id": u"19",
                    "icon": u"fab fa-leanpub",
                    "label": u"Mødereferater og forhandlingsprotokoller"
                  },
                  {
                    "id": u"23",
                    "icon": u"fab fa-leanpub",
                    "label": u"Realregistre"
                  },
                  {
                    "id": u"21",
                    "icon": u"fab fa-leanpub",
                    "label": u"Skattemandtalslister"
                  },
                  {
                    "id": u"26",
                    "icon": u"fab fa-leanpub",
                    "label": u"Skifteprotokoller"
                  }
                ],
                "id": u"18",
                "icon": u"fab fa-leanpub",
                "label": u"Registre og protokoller"
              },
              {
                "children": [
                  {
                    "id": u"34",
                    "icon": u"far chart-bar",
                    "label": u"Database"
                  },
                  {
                    "id": u"31",
                    "icon": u"far chart-bar",
                    "label": u"Regnskaber og budgetmateriale"
                  },
                  {
                    "id": u"30",
                    "icon": u"far chart-bar",
                    "label": u"Spørgeskemaundersøgelser"
                  },
                  {
                    "id": u"32",
                    "icon": u"far chart-bar",
                    "label": u"Statistisk materiale"
                  },
                  {
                    "id": u"33",
                    "icon": u"far chart-bar",
                    "label": u"Statistisk undersøgelse"
                  },
                  {
                    "id": u"35",
                    "icon": u"far chart-bar",
                    "label": u"Tabelværk"
                  }
                ],
                "id": u"29",
                "icon": u"far chart-bar",
                "label": u"Statistisk og økonomisk materiale"
              }
        ]
    },
    'subjects': {
        'label': 'Emnekategori',
        'multiple': True,
        'hierarchical': True,
        'content': [
            {
                'id': '17',
                'label': 'Erhverv',
                'children': [
                    {
                        'id': '53',
                        'label': 'Banker og Sparekasser',
                    },
                    {
                        'id': '14',
                        'label': 'Detailhandel og service',
                    },
                    {
                        'id': '13',
                        'label': 'Fagforeninger',
                    },
                    {
                        'id': '66',
                        'label': 'Fiskeri og jagt',
                    },
                    {
                        'id': '15',
                        'label': 'Håndværk og industri',
                    },
                    {
                        'id': '57',
                        'label': 'Kooperation',
                    },
                    {
                        'id': '54',
                        'label': 'Kost og logi',
                    },
                    {
                        'id': '16',
                        'label': 'Land- og skovbrug',
                    },
                    {
                        'id': '55',
                        'label': 'Turistvæsen',
                    }
                ]
            },
            {
                'id': '29',
                'label': 'Historiske perioder og temaer',
                'children': [
                    {
                        'id': '4',
                        'label': 'Myter og sagn',
                    },
                    {
                        'id': '28',
                        'label': 'Oldtid',
                    },
                    {
                        'id': '51',
                        'label': 'Vikingetiden',
                    },
                    {
                        'id': '30',
                        'label': 'Indtil 1536',
                    },
                    {
                        'id': '72',
                        'label': '1536-1660',
                    },
                    {
                        'id': '69',
                        'label': '1660-1814',
                    },
                    {
                        'id': '68',
                        'label': 'Det 19. århundrede',
                    },
                    {
                        'id': '31',
                        'label': 'Det 20. århundrede',
                    },
                    {
                        'id': '70',
                        'label': 'Besættelsen',
                    },
                    {
                        'id': '7',
                        'label': 'Det 21. århundrede',
                    }
                ]
            },
            {
                'id': '37',
                'label': 'Kultur og fritid',
                'children': [
                    {
                        'id': '34',
                        'label': 'Arkitektur',
                    },
                    {
                        'id': '33',
                        'label': 'Arrangementer og festtraditioner',
                    },
                    {
                        'id': '56',
                        'label': 'Folkekultur og dagligdagsliv',
                    },
                    {
                        'id': '35',
                        'label': 'Forlystelser, spil og idræt',
                    },
                    {
                        'id': '76',
                        'label': 'Kulturinstitutioner',
                    },
                    {
                        'id': '74',
                        'label': 'Kunst og litteratur',
                    },
                    {
                        'id': '73',
                        'label': 'Mad og drikke',
                    },
                    {
                        'id': '36',
                        'label': 'Musik',
                    },
                    {
                        'id': '75',
                        'label': 'Skulpturer og offentlig kunst',
                    },
                    {
                        'id': '1',
                        'label': 'Teater, film, radio og tv',
                    }
                ]
            },
            {
                'id': '62',
                'label': 'Natur',
                'children': [
                    {
                        'id': '59',
                        'label': 'Kilder',
                    },
                    {
                        'id': '58',
                        'label': 'Skove',
                    },
                    {
                        'id': '61',
                        'label': 'Strand og bugt',
                    },
                    {
                        'id': '60',
                        'label': 'Søer',
                    },
                    {
                        'id': '12',
                        'label': 'Åer og bække',
                    }
                ]
            },
            {
                'id': '42',
                'label': 'Personer',
                'children': [
                    {
                        'id': '39',
                        'label': 'Arkitekter og bygmestre',
                    },
                    {
                        'id': '38',
                        'label': 'Embedsmænd',
                    },
                    {
                        'id': '41',
                        'label': 'Erhvervsfolk',
                    },
                    {
                        'id': '21',
                        'label': 'Gejstlige',
                    },
                    {
                        'id': '40',
                        'label': 'Historiske personer',
                    },
                    {
                        'id': '22',
                        'label': 'Journalister og pressefotografer',
                    },
                    {
                        'id': '19',
                        'label': 'Kulturpersoner',
                    },
                    {
                        'id': '18',
                        'label': 'Politikere',
                    },
                    {
                        'id': '20',
                        'label': 'Undervisere og forskere',
                    }
                ]
            },
            {
                'id': '3',
                'label': 'Samfund',
                'children': [
                    {
                        'id': '71',
                        'label': 'Beskæftigelse og arbejdsløshed',
                    },
                    {
                        'id': '5',
                        'label': 'Bolig, byggeri og byplanlægning',
                    },
                    {
                        'id': '47',
                        'label': 'Foreninger',
                    },
                    {
                        'id': '44',
                        'label': 'Kommunal forvaltning',
                    },
                    {
                        'id': '43',
                        'label': 'Kommunikation og medier',
                    },
                    {
                        'id': '6',
                        'label': 'Lovgivning og jura',
                    },
                    {
                        'id': '45',
                        'label': 'Militær',
                    },
                    {
                        'id': '27',
                        'label': 'Penge og økonomi',
                    },
                    {
                        'id': '24',
                        'label': 'Politi, brand og redning',
                    },
                    {
                        'id': '23',
                        'label': 'Politik',
                    },
                    {
                        'id': '46',
                        'label': 'Religion og kirke',
                    },
                    {
                        'id': '25',
                        'label': 'Socialpolitik og velfærd',
                    },
                    {
                        'id': '67',
                        'label': 'Sundhedsvæsen',
                    },
                    {
                        'id': '64',
                        'label': 'Trafik og transport',
                    },
                    {
                        'id': '53',
                        'label': 'Ud- og indvandring',
                    },
                    {
                        'id': '26',
                        'label': 'Undervisning og uddannelse',
                    },
                    {
                        'id': '65',
                        'label': 'Videnskab og forskning',
                    }
                ]
            },
            {
                'id': '9',
                'label': 'Steder',
                'children': [
                    {
                        'id': '8',
                        'label': 'Byer og bydele',
                    },
                    {
                        'id': '10',
                        'label': 'Ejendomme og bygningsværker',
                    },
                    {
                        'id': '52',
                        'label': 'Gader og veje',
                    },
                    {
                        'id': '49',
                        'label': 'Kirker',
                    },
                    {
                        'id': '48',
                        'label': 'Parker og anlæg',
                    },
                    {
                        'id': '11',
                        'label': 'Slotte og herregårde',
                    },
                    {
                        'id': '50',
                        'label': 'Sogne',
                    },
                    {
                        'id': '32',
                        'label': 'Torve og pladser',
                    }
                ]
            },
            {
                'id': '2',
                'label': 'Andet',
            }
        ]
    },
    'availability': {
        'label': 'Tilgængelighed',
        'multiple': False,
        'hierarchical': False,
        'content': [
            {
                'id': '2',
                'label': 'På magasin',
            },
            {
                'id': '3',
                'label': 'Kan ses på læsesalen',
            },
            {
                'id': '4',
                'label': 'Kan ses online',
            }
        ]
    },
    'usability': {
        'label': 'Brug af materialer',
        'multiple': False,
        'hierarchical': False,
        'content': [
            {
                'id': '1',
                'label': 'I offentlig eje',
            },
            {
                'id': '2',
                'label': 'CC Navngivelse',
            },
            {
                'id': '3',
                'label': 'CC Navngivelse-IkkeKommerciel',
            },
            {
                'id': '4',
                'label': 'Alle rettigheder forbeholdes',
            }
        ]
    }
}

FILTERS = {
            "creators": {
                "label": u"Ophavsretsholder",
                "repeatable": True,
                "type": "object",
                "negatable": True,
            },
            "locations": {
                "label": u"Stedsangivelse",
                "repeatable": True,
                "type": "object",
                "negatable": True,
            },
            "events": {
                "label": u"Begivenhed",
                "repeatable": True,
                "type": "object",
                "negatable": True,
            },
            "people": {
                "label": u"Person",
                "repeatable": True,
                "type": "object",
                "negatable": True,
            },
            "organisations": {
                "label": u"Organisation",
                "repeatable": True,
                "type": "object",
                "negatable": True,
            },
            "collection": {
                "label": u"Samling",
                "repeatable": False,
                "type": "object",
                "negatable": True,
            },
            "date_from": {
                "label": u"Tidligste dato",
                "repeatable": False,
                "type": "date",
                "negatable": False,
            },
            "date_to": {
                "label": u"Seneste dato",
                "repeatable": False,
                "type": "date",
                "negatable": False,
            },
            "subjects": {
                "label": u"Emnekategori",
                "repeatable": True,
                "type": "object",
                "negatable": True,
            },
            "series": {
                "label": u"Arkivserie",
                "repeatable": False,
                "type": "string",
                "negatable": False,
            },
            "admin_tags": {
                "label": u"Administrativt tag",
                "repeatable": True,
                "type": "string",
                "negatable": True,
            },
            "collection_tags": {
                "label": u"Samlingstags",
                "repeatable": True,
                "type": "string",
                "negatable": True,
            },
            "content_types": {
                "label": u"Materialetype",
                "repeatable": True,
                "type": "object",
                "negatable": True,
            },
            "collectors": {
                "label": u"Arkivskaber",
                "repeatable": True,
                "type": "object",
                "negatable": True,
            },
            "curators": {
                "label": u"Kurator",
                "repeatable": True,
                "type": "object",
                "negatable": True,
            },
            "availability": {
                "label": u"Tilgængelighed",
                "repeatable": False,
                "type": "object",
                "negatable": True,
            },
            'sort': {
                'label': u'Sortering',
                'repeatable': False,
                'type': 'string',
                'negatable': False,
            },
            'size': {
                'label': u'Antal visninger',
                'repeatable': False,
                'type': 'integer',
                'negatable': False,
            },
            "usability": {
                "label": u"Hvad må jeg bruge?",
                "repeatable": False,
                "type": "object",
                "negatable": True,
            },
            "registration_id": {
                "label": u"RegistreringsID",
                "repeatable": False,
                "type": "integer",
                "negatable": False,
            },
        }