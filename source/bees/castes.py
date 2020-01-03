from fysom import *


def worker_fysom():
    return Fysom({
            # await orders > harvest > offload >...
            'initial': 'await orders',
            'events': [
                {'name': 'go to flower', 'src': 'await orders', 'dst': 'harvest'},
                {'name': 'harvest complete', 'src': 'harvest', 'dst': 'head back'},
                {'name': 'begin offload', 'src': 'head back', 'dst': 'offload'},
                {'name': 'offload complete', 'src': 'offload', 'dst': 'await orders'}
            ]
        })


def scout_fysom():
    return Fysom({
        # scout > report > dance >...
        'initial': 'scout',
        'events': [
            {'name': 'begin search', 'src': 'dance', 'dst': 'scout'},
            {'name': 'found flower', 'src': 'scout', 'dst': 'report'},
            {'name': 'dance complete', 'src': 'report', 'dst': 'scout'}
        ]
    })
