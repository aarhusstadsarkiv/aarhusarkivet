import os
# import urllib
import json
from copy import deepcopy
import requests
from six.moves.urllib.parse import urlencode

import serviceInterface

OAWS_API_KEY = os.environ.get('OAWS_API_KEY')

FACETS = {
    'content_types': {
        'label': u'Materialetype',
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
        'label': u'Emnekategori',
        'multiple': True,
        'hierarchical': True,
        'content': [
            {
                'id': u'17',
                'label': u'Erhverv',
                'children': [
                    {
                        'id': u'53',
                        'label': u'Banker og Sparekasser',
                    },
                    {
                        'id': u'14',
                        'label': u'Detailhandel og service',
                    },
                    {
                        'id': u'13',
                        'label': u'Fagforeninger',
                    },
                    {
                        'id': u'66',
                        'label': u'Fiskeri og jagt',
                    },
                    {
                        'id': u'15',
                        'label': u'Håndværk og industri',
                    },
                    {
                        'id': u'57',
                        'label': u'Kooperation',
                    },
                    {
                        'id': u'54',
                        'label': u'Kost og logi',
                    },
                    {
                        'id': u'16',
                        'label': u'Land- og skovbrug',
                    },
                    {
                        'id': u'55',
                        'label': u'Turistvæsen',
                    }
                ]
            },
            {
                'id': u'29',
                'label': u'Historiske perioder og temaer',
                'children': [
                    {
                        'id': u'4',
                        'label': u'Myter og sagn',
                    },
                    {
                        'id': u'28',
                        'label': u'Oldtid',
                    },
                    {
                        'id': u'51',
                        'label': u'Vikingetiden',
                    },
                    {
                        'id': u'30',
                        'label': u'Indtil 1536',
                    },
                    {
                        'id': u'72',
                        'label': u'1536-1660',
                    },
                    {
                        'id': u'69',
                        'label': u'1660-1814',
                    },
                    {
                        'id': u'68',
                        'label': u'Det 19. århundrede',
                    },
                    {
                        'id': u'31',
                        'label': u'Det 20. århundrede',
                    },
                    {
                        'id': u'70',
                        'label': u'Besættelsen',
                    },
                    {
                        'id': u'7',
                        'label': u'Det 21. århundrede',
                    }
                ]
            },
            {
                'id': u'37',
                'label': u'Kultur og fritid',
                'children': [
                    {
                        'id': u'34',
                        'label': u'Arkitektur',
                    },
                    {
                        'id': u'33',
                        'label': u'Arrangementer og festtraditioner',
                    },
                    {
                        'id': u'56',
                        'label': u'Folkekultur og dagligdagsliv',
                    },
                    {
                        'id': u'35',
                        'label': u'Forlystelser, spil og idræt',
                    },
                    {
                        'id': u'76',
                        'label': u'Kulturinstitutioner',
                    },
                    {
                        'id': u'74',
                        'label': u'Kunst og litteratur',
                    },
                    {
                        'id': u'73',
                        'label': u'Mad og drikke',
                    },
                    {
                        'id': u'36',
                        'label': u'Musik',
                    },
                    {
                        'id': u'75',
                        'label': u'Skulpturer og offentlig kunst',
                    },
                    {
                        'id': u'1',
                        'label': u'Teater, film, radio og tv',
                    }
                ]
            },
            {
                'id': u'62',
                'label': u'Natur',
                'children': [
                    {
                        'id': u'59',
                        'label': u'Kilder',
                    },
                    {
                        'id': u'58',
                        'label': u'Skove',
                    },
                    {
                        'id': u'61',
                        'label': u'Strand og bugt',
                    },
                    {
                        'id': u'60',
                        'label': u'Søer',
                    },
                    {
                        'id': u'12',
                        'label': u'Åer og bække',
                    }
                ]
            },
            {
                'id': u'42',
                'label': u'Personer',
                'children': [
                    {
                        'id': u'39',
                        'label': u'Arkitekter og bygmestre',
                    },
                    {
                        'id': u'38',
                        'label': u'Embedsmænd',
                    },
                    {
                        'id': u'41',
                        'label': u'Erhvervsfolk',
                    },
                    {
                        'id': u'21',
                        'label': u'Gejstlige',
                    },
                    {
                        'id': u'40',
                        'label': u'Historiske personer',
                    },
                    {
                        'id': u'22',
                        'label': u'Journalister og pressefotografer',
                    },
                    {
                        'id': u'19',
                        'label': u'Kulturpersoner',
                    },
                    {
                        'id': u'18',
                        'label': u'Politikere',
                    },
                    {
                        'id': u'20',
                        'label': u'Undervisere og forskere',
                    }
                ]
            },
            {
                'id': u'3',
                'label': u'Samfund',
                'children': [
                    {
                        'id': u'71',
                        'label': u'Beskæftigelse og arbejdsløshed',
                    },
                    {
                        'id': u'5',
                        'label': u'Bolig, byggeri og byplanlægning',
                    },
                    {
                        'id': u'47',
                        'label': u'Foreninger',
                    },
                    {
                        'id': u'44',
                        'label': u'Kommunal forvaltning',
                    },
                    {
                        'id': u'43',
                        'label': u'Kommunikation og medier',
                    },
                    {
                        'id': u'6',
                        'label': u'Lovgivning og jura',
                    },
                    {
                        'id': u'45',
                        'label': u'Militær',
                    },
                    {
                        'id': u'27',
                        'label': u'Penge og økonomi',
                    },
                    {
                        'id': u'24',
                        'label': u'Politi, brand og redning',
                    },
                    {
                        'id': u'23',
                        'label': u'Politik',
                    },
                    {
                        'id': u'46',
                        'label': u'Religion og kirke',
                    },
                    {
                        'id': u'25',
                        'label': u'Socialpolitik og velfærd',
                    },
                    {
                        'id': u'67',
                        'label': u'Sundhedsvæsen',
                    },
                    {
                        'id': u'64',
                        'label': u'Trafik og transport',
                    },
                    {
                        'id': u'53',
                        'label': u'Ud- og indvandring',
                    },
                    {
                        'id': u'26',
                        'label': u'Undervisning og uddannelse',
                    },
                    {
                        'id': u'65',
                        'label': u'Videnskab og forskning',
                    }
                ]
            },
            {
                'id': u'9',
                'label': u'Steder',
                'children': [
                    {
                        'id': u'8',
                        'label': u'Byer og bydele',
                    },
                    {
                        'id': u'10',
                        'label': u'Ejendomme og bygningsværker',
                    },
                    {
                        'id': u'52',
                        'label': u'Gader og veje',
                    },
                    {
                        'id': u'49',
                        'label': u'Kirker',
                    },
                    {
                        'id': u'48',
                        'label': u'Parker og anlæg',
                    },
                    {
                        'id': u'11',
                        'label': u'Slotte og herregårde',
                    },
                    {
                        'id': u'50',
                        'label': u'Sogne',
                    },
                    {
                        'id': u'32',
                        'label': u'Torve og pladser',
                    }
                ]
            },
            {
                'id': u'2',
                'label': u'Andet',
            }
        ]
    },
    'availability': {
        'label': u'Tilgængelighed',
        'multiple': False,
        'hierarchical': False,
        'content': [
            {
                'id': u'2',
                'label': u'På magasin',
            },
            {
                'id': u'3',
                'label': u'Kan ses på læsesalen',
            },
            {
                'id': u'4',
                'label': u'Kan ses online',
            }
        ]
    },
    'usability': {
        'label': u'Brug af materialer',
        'multiple': False,
        'hierarchical': False,
        'content': [
            {
                'id': u'1',
                'label': u'I offentlig eje',
            },
            {
                'id': u'2',
                'label': u'CC Navngivelse',
            },
            {
                'id': u'3',
                'label': u'CC Navngivelse-IkkeKommerciel',
            },
            {
                'id': u'4',
                'label': u'Alle rettigheder forbeholdes',
            }
        ]
    }
}

FILTERS = {
    'creators': {
        'label': u'Ophavsretsholder',
        'repeatable': True,
        'type': 'object',
    },
    'locations': {
        'label': u'Stedsangivelse',
        'repeatable': True,
        'type': 'object',
    },
    'events': {
        'label': u'Forestilling',
        'repeatable': True,
        'type': 'object',
    },
    'people': {
        'label': u'Person',
        'repeatable': True,
        'type': 'object',
    },
    'organisations': {
        'label': u'Organisation',
        'repeatable': True,
        'type': 'object',
    },
    'collection': {
        'label': u'Samling',
        'repeatable': False,
        'type': 'object',
    },
    'date_from': {
        'label': u'Startdato',
        'repeatable': False,
        'type': 'string',
    },
    'date_to': {
        'label': u'Slutdato',
        'repeatable': False,
        'type': 'string',
    },
    'subjects': {
        'label': u'Emnekategori',
        'repeatable': True,
        'type': 'object',
    },
    'series': {
        'label': u'Serie',
        'repeatable': False,
        'type': 'string',
    },
    'admin_tags': {
        'label': u'Tag',
        'repeatable': True,
        'type': 'string',
    },
    'collection_tags': {
        'label': u'Samlingstags',
        'repeatable': True,
        'type': 'string',
    },
    'content_types': {
        'label': u'Materialetype',
        'repeatable': True,
        'type': 'object',
    },
    'collectors': {
        'label': u'Arkivskaber',
        'repeatable': True,
        'type': 'object',
    },
    'curators': {
        'label': u'Kurator',
        'repeatable': True,
        'type': 'object',
    },
    'availability': {
        'label': u'Tilgængelighed',
        'repeatable': False,
        'type': 'object',
    },
    'sort': {
        'label': u'Sortering',
        'repeatable': False,
        'type': 'string',
    },
    'size': {
        'label': u'Antal visninger',
        'repeatable': False,
        'type': 'integer',
    },
    'start': {
        'label': u'Start',
        'repeatable': False,
        'type': 'integer',
    },
    'usability': {
        'label': u'Hvad må jeg bruge?',
        'repeatable': False,
        'type': 'object'
    },
    'registration_id': {
        'label': u'RegistreringsID',
        'repeatable': False,
        'type': 'integer'
    }
}


class Client():

    def __init__(self):
        self.facets = FACETS
        self.filters = FILTERS
        self.service = serviceInterface.Service(OAWS_API_KEY)
        self.service_url = 'https://openaws.appspot.com'
        self.resources = {
            'records': 'records_v3',
            'people': 'entities',
            'locations': 'entities',
            'organisations': 'entities',
            'events': 'entities',
            'creators': 'entities',
            'collectors': 'entities',
            'objects': 'objects',
            'collections': 'collections'
        }

    def list_facets_v2(self):
        def encode(key, val):
            utf8_param = [(key, val)]
            return urlencode(utf8_param)

        facets = self.service.list_facets()
        result = {}

        for facet in facets:
            out = {}
            for b in facets[facet].get('buckets'):
                b['add_link'] = encode(facet, b.get('value'))
                out[b.get('value')] = b
            result[facet] = out
        return {'total_facets': self.facets, 'active_facets': result}

    def list_resources(self, query_params=None):

        def _generate_views(params, view):
            output = []
            views = [
                {
                    'label': u'Listevisning',
                    'value': 'list',
                    'icon': 'fas fa-list'  # 'view_list'
                },
                {
                    'label': u'Galleri-visning',
                    'value': 'gallery',
                    'icon': 'fas fa-th'  # 'view_module'
                }
            ]

            if params:
                stripped_params = [(t[0], t[1]) for t in params if t[0] != 'view']
            else:
                stripped_params = []

            for option in views:
                current = {}
                current['label'] = option.get('label')
                current['icon'] = option.get('icon')
                if option.get('value') == view:
                    current['selected'] = True
                else:
                    current['link'] = _urlencode(stripped_params + [('view', option.get('value'))])
                output.append(current)
            return output

        def _generate_sorts(params, sort, direction):
            sorts = [
                {
                    'label': u'Ældste dato først',
                    'sort': 'date_from',
                    'icon': 'fas fa-long-arrow-alt-up',  # 'arrow_upward'
                    'direction': 'asc'
                },
                {
                    'label': u'Nyeste dato først',
                    'sort': 'date_to',
                    'icon': 'fas fa-long-arrow-alt-down',  # 'arrow_downward'
                    'direction': 'desc'
                },
                {
                    'label': u'Relevans',
                    'sort': '_score',
                    'direction': 'desc'
                }
            ]
            output = []

            if params:
                stripped_params = [(t[0], t[1]) for t in params if t[0] not in ['sort', 'direction', 'start']]
            else:
                stripped_params = []

            for option in sorts:
                current = {}
                current['icon'] = option.get('icon')
                current['label'] = option.get('label')
                if option.get('sort') == sort and option.get('direction') == direction:
                    current['selected'] = True
                else:
                    current['link'] = _urlencode(stripped_params + [('sort', option.get('sort')), ('direction', option.get('direction'))])
                output.append(current)
            return output

        def _generate_sizes(params, size):
            sizes = [20, 50, 100]
            output = []

            if params:
                stripped_params = [(t[0], t[1]) for t in params if t[0] != 'size']
            else:
                stripped_params = []

            for option in sizes:
                current = {}
                current['label'] = option
                if option == size:
                    current['selected'] = True
                else:
                    current['link'] = _urlencode(stripped_params + [('size', option)])
                output.append(current)
            return output

        def _generate_filters_v2(filters, params):
            # Takes filters-array of filters and adds view- and remove-links
            for f in filters:
                # If resolve_params has a display_label equal to "ID Missing"
                if f.get('error'):
                    continue

                key = f.get('key')
                value = f.get('value')
                negated = f.get('negated')

                # View_link
                # 'label' indicates an id-based filter, which has
                # an id and has been resolved
                if f.get('label'):
                    if key == 'collection':
                        f['view_link'] = "/".join(['collections', value])
                    else:
                        f['view_link'] = "/".join([key, value])

                # Remove_link
                # If positive collection, also remove series
                # negative collection-params works like normal param
                if key == 'collection' and not negated:
                    new_params = [(k, v) for k, v in params if k not in ['collection', 'series', 'start']]
                    f['remove_link'] = _urlencode(new_params)
                else:
                    new_params = [(k, v) for k, v in params if k not in ['start']]
                    original_key = '-' + key if negated else key
                    f['remove_link'] = _urlencode(new_params,
                                                  remove=(original_key, value))

                # Inverse_link
                # If negated, replace with positive, vice versa
                # exception: if positive collection, remove series-param, as
                # it follows the positive collection
                if negated:
                    new_params = [(k, v) for k, v in params if k not in ['start']]
                    f['invert_link'] = _urlencode(new_params,
                                                  insert=(key, value),
                                                  remove=('-' + key, value))
                else:
                    if key == 'collection':
                        new_params = [(k, v) for k, v in params if k not in ['collection', 'series']]
                        f['invert_link'] = _urlencode(new_params,
                                                      insert=('-' + key, value))
                    else:
                        new_params = [(k, v) for k, v in params if k not in ['start']]
                        f['invert_link'] = _urlencode(new_params,
                                                      insert=('-' + key, value),
                                                      remove=(key, value))

                if key in ['people', 'organisations']:
                    response = self._get_request("https://openaws.appspot.com/entities/" + value)
                    if response.get('status_code') == 0:
                        entity = response.get('result')

                        if entity.get('is_creative_creator'):
                            f['creator_link'] = "creators=" + value
                        if entity.get('is_creator'):
                            f['creator_link'] = "collectors=" + value

            return filters

        def _generate_facets_v2(facets, params=None):

            def _generate_facet(name, active_facets, params):

                def _recursive(name, total_facets, active_facets, params):

                    for d in total_facets:
                        _id = d.get('id')

                        if _id in active_facets.keys():
                            d['count'] = active_facets.get(_id)

                            current = (name, _id)
                            if params and (current in params):
                                rm_params = [x for x in params if x != current]
                                d['remove_link'] = _urlencode_v2(rm_params)
                                # i['remove_link'] = _urlencode(params,
                                #                               remove=current)
                            elif params:
                                add_params = params + [current]
                                d['add_link'] = _urlencode_v2(add_params)
                                # i['add_link'] = _urlencode(params,
                                #                            insert=current)
                            else:
                                d['add_link'] = _urlencode_v2([current])

                            if d.get('children'):
                                _recursive(name, d.get('children'),
                                           active_facets, params)

                    return total_facets

                facet_label = self.facets[name].get('label')
                total_facets = deepcopy(self.facets[name].get('content'))
                linked_tree = _recursive(name, total_facets, active_facets, params)

                return {"label": facet_label, 'content': linked_tree}

            output = {}
            for facet_name in facets:
                # extract id and count from aws-output
                buckets = facets[facet_name].get('buckets')
                active_facets = {b.get('value'): b.get('count') for b in buckets}
                # generate links recursively
                output[facet_name] = _generate_facet(facet_name,
                                                     active_facets,
                                                     params)

            return output

        def _generate_facets_v3(facets, params=None):
            result = {}
            for facet in facets:
                out = {}
                for b in facets[facet].get('buckets'):
                    active = (facet, b.get('value'))
                    if params and (active in params):
                        rm_params = [x for x in params if x != active]
                        b['remove_link'] = _urlencode_v2(rm_params)
                    elif params:
                        b['add_link'] = _urlencode_v2(params + [active])
                    else:
                        b['add_link'] = _urlencode_v2([active])
                    out[b.get('value')] = b
                result[facet] = out
            return result

        def _urlencode_v2(params):
            # params must be a list of tuple(s)
            if not params:
                return "root"
            else:
                # utf8_params = [(t[0], unicode(t[1]).encode('utf-8')) for t in params]
                utf8_params = [(t[0], t[1]) for t in params]
                return urlencode(utf8_params)

        def _urlencode(params=None, remove=None, insert=None):
            # Like original _urlencode, but added utf8-encoding before
            # returning urlencoded params
            temp_params = deepcopy(params) if params else []
            if remove and not insert:
                if remove in temp_params:
                    temp_params.remove(remove)
            elif remove and insert:
                if remove in temp_params:
                    loc = temp_params.index(remove)
                    temp_params[loc] = insert
                else:
                    temp_params.append(insert)
            elif insert:
                    temp_params.append(insert)

            # utf8_params = [(t[0], unicode(t[1]).encode('utf-8')) for t in temp_params]
            utf8_params = [(t[0], t[1]) for t in temp_params]
            return urlencode(utf8_params)

        # If requesting af list of collections
        if query_params.get('resource', '') == 'collections':
            response = self._get_request("https://openaws.appspot.com/collections")
            if response.get('status_code') == 0:
                return response.result
            else:
                return {"error": response.get('status_code'),
                        "msg": response.get('status_msg')}

        # If SAM-request (view=ids) or fmt=json, return without adding further keys
        # if query_params.get('view', '') == 'ids':
        if 'ids' in query_params.getlist('view'):
            return self.service.list_resources_v2(query_params)

        # Else return fullblown response
        resp = self.service.list_resources_v2(query_params)

        # Convert Immutable MultiDict to mutable list of tuples
        # http://werkzeug.pocoo.org/docs/0.13/datastructures/#werkzeug.datastructures.MultiDict
        # processed_params = [tup for tup in query_params.iteritems(multi=True)]
        processed_params = [tup for tup in query_params.items(multi=True)]

        # Keys used for generating searchviews and facets
        resp['params'] = processed_params

        resp['collection_search'] = query_params.get('collection', False)

        resp['filters'] = _generate_filters_v2(resp['server_filters'],
                                               processed_params)
        resp['active_facets'] = _generate_facets_v3(resp['server_facets'],
                                                    processed_params)

        # 'non_query_params' is used to generate a remove_link for the q-param
        # which is not processed in _generate_filter()
        query = query_params.get('q')
        if query:
            other_params = [i for i in processed_params if i != ('q', query)]
            resp['non_query_params'] = _urlencode_v2(other_params)

        # Just testing - remove?
        resp['total_facets'] = self.facets

        # Client-params dependent on valid response
        if resp.get('status_code') == 0:

            total = resp['total']
            start = resp['start']
            size = resp['size']

            # Append to service-response
            resp['size_list'] = _generate_sizes(processed_params, size)
            resp['sort_list'] = _generate_sorts(processed_params,
                                                resp['sort'],
                                                resp['direction'])
            resp['view_list'] = _generate_views(processed_params,
                                                query_params.get('view',
                                                                 'list'))
            resp['view'] = query_params.get('view', 'list')

            if resp.get('result'):
                rm_tup = ('start', str(start))
                if start > 0:
                    resp['first'] = _urlencode(processed_params,
                                               remove=rm_tup)
                    resp['previous'] = _urlencode(processed_params,
                                                  remove=rm_tup,
                                                  insert=('start',
                                                          start - size))

                if total <= 10000 and (start + size < total):
                    last_start = total // size * size
                    if last_start == total:
                        last_start = total - size
                    resp['last'] = _urlencode(processed_params,
                                              remove=rm_tup,
                                              insert=('start', last_start))

                if (start + size < total) and (start + size <= 10000):
                    resp['next'] = _urlencode(processed_params,
                                              remove=rm_tup,
                                              insert=('start',
                                                      start + size))

        else:
            resp['message'] = "Something went wrong..."

        return resp

    def get_resource(self, collection, resource, fmt=None):

        def _generate_hierarchical_structure(string_list):
            # Takes a list of strings with possible '/' as hierarchical seperators
            # Returns a dict-structure with 'label', 'path' and possibly 'children'-keys

            def addHierItem(key, hierStruct, hierList, parent):
                if parent != "":
                    path = parent + "/" + key
                else:
                    path = key

                hierItem = {"label": key, "path": path}

                childrenList = []
                children = hierStruct.get(key)
                for childKey in sorted(children):
                    addHierItem(childKey, children, childrenList, path)

                if len(childrenList) > 0:
                    hierItem["children"] = childrenList

                hierList.append(hierItem)

            hierList = []
            hierStruct = {}
            for item in sorted(string_list):
                splitList = item.split("/")

                curLevel = hierStruct
                for key in splitList:
                    hierData = curLevel.get(key, {})
                    curLevel[key] = hierData
                    curLevel = hierData

            for key in sorted(hierStruct):
                addHierItem(key, hierStruct, hierList, "")

            return hierList

        def format_record(record):
            result = {}
            for key, value in record.items():
                # First handle all specialcases
                # If 'series' then treat uniquely
                if key == 'series':
                    output = []
                    currentLevel = []
                    urlpath = {}
                    collection = record.get('collection')

                    if collection:
                        urlpath['collection'] = collection.get('id')

                    for idx in value.split('/'):
                        currentLevel.append(idx)
                        urlpath['series'] = '/'.join(currentLevel)
                        level = {}
                        level['label'] = idx
                        level['new_link'] = self._generate_new_link(urlpath)
                        output.append(level)
                    result[key] = output

                # If key is list of strings
                elif key in ['admin_tags']:
                    output = []
                    for idx in value:
                        item = {}
                        item['label'] = idx
                        item['new_link'] = self._generate_new_link(key, idx)
                        output.append(item)
                    result[key] = output

                elif key in ['collection_tags']:
                    result[key] = _generate_hierarchical_structure(value)
                    
                elif key in ['resources']:
                    result[key] = value

                # If key is dict
                elif isinstance(value, dict) and key in self.filters:
                    # If id-dict
                    if value.get('id'):
                        _id = value.get('id')
                        label = value.get('label')
                        item = {}
                        item['label'] = label
                        item['id'] = _id
                        item['new_link'] = self._generate_new_link(key, _id)
                        result[key] = item
                    else:
                        result[key] = value

                # If key is list (of id-dicts)
                elif isinstance(value, list) and key in self.filters:
                    output = []

                    for _dict in value:

                        # hierarchical concept or entity
                        if isinstance(_dict.get('id'), list):
                            hierarchy = []
                            for i, v in enumerate(_dict.get('id')):
                                item = {}
                                item['id'] = v
                                item['label'] = _dict.get('label')[i]
                                item['new_link'] = '='.join([key, str(v)])
                                hierarchy.append(item)
                            output.append(hierarchy)

                        # flat concept or entity
                        else:
                            _id = _dict.get('id')
                            label = _dict.get('label')
                            item = {}
                            item['id'] = _id
                            item['label'] = label
                            item['new_link'] = self._generate_new_link(key, _id)
                            output.append(item)

                    result[key] = output

                else:
                    result[key] = value

            return result

        def format_collection(collection):

            # Enhance with dynamically fetched structures from searchengine
            series, collection_tags = self.service.list_collection_structures(collection.get('id'))
            collection['series'] = series
            collection['collection_tags'] = collection_tags

            # Pop 'structure'-key - at least for now. Reintroduce when we can work with descriptions on
            # individual series-levels
            collection.pop('structure', None)

            return collection

        response = self._get_request('/'.join([self.service_url,
                                               self.resources.get(collection),
                                               resource]))

        if response.get('status_code') == 0:
            res = response.get('result')
            if collection == 'records':
                if fmt == 'json':
                    return res
                else:
                    return format_record(res)
            elif collection == 'collections':
                return format_collection(res)
            else:
                return res

        elif response.get('status_code') == 1:
            return {
                'error': {
                    'code': 404,
                    'msg': 'Resourcen eksisterende ikke',
                    'id': resource
                }
            }
        elif response.get('status_code') == 2:
            return {
                'error': {
                    'code': 404,
                    'msg': 'Resourcen er slettet',
                    'id': resource
                }
            }
        else:
            return {
                'error': {
                    'code': response.get('status_code'),
                    'msg': response.get('status_msg'),
                    'id': resource
                }
            }

    def autocomplete(self, term, limit=10, domain=None):
        url = "https://aarhusiana.appspot.com/autocomplete_v3"
        params = [('t', term), ('limit', limit)]
        if domain and domain in ['events', 'people', 'organisations', 'locations', 'collections']:
            params.append(('domain', domain))
        response = requests.get(url, params=params)

        try:
            payload = json.loads(response.content)
            return payload.get('result')
        except ValueError as e:
            return {'status_code': 5, 'status_msg': e}

    def batch_records(self, id_list):
        if id_list:
            url = 'https://openaws.appspot.com/resolve_records_v2'
            data = {'view': 'record', 'oasid': json.dumps(id_list)}
            response = requests.post(url, data=data)
            try:
                payload = json.loads(response.content)
                if payload.get('status_code') == 0:
                    return payload.get('result')
            except ValueError as e:
                return {'status_code': 5, 'status_msg': e}
        else:
            return []

    def _generate_new_link(self, key, value=None):
        """Takes one dict of key(s) and value(s) OR two strings"""
        if value:
            # value = str(value) if isinstance(value, int) else value
            return self._urlencode_old({key: value})
        else:
            return self._urlencode_old(key)

    def _urlencode_old(self, params, decode=True):
        path = {}
        if type(params) == dict:
            iterable = params.items()
        else:
            iterable = params
        for key, value in iterable:

            if key in path:
                # path[key] += ';' + unicode(value).encode('utf-8')
                path[key] += ';' + value
            else:
                # path[key] = unicode(value).encode('utf-8')
                path[key] = value

        return urlencode(path)
        # encoded = urlencode(path)
        # if decode:
        #     return encoded.decode('utf-8')
        # else:
        #     return encoded

    def _get_request(self, url, params=None):
        response = requests.get(url, params=params)
        try:
            response_to_dict = json.loads(response.content)
            return response_to_dict
        except ValueError as e:
            return {'status_code': 5, 'error': e}

