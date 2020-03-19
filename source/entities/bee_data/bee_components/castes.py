"""
File Name: Castes
File Purpose: Holds data on finite state machines that control behavior for all types of bees
Notes:
"""

from fysom import Fysom


#  Worker finite state machine


def worker_fysom():
    return Fysom({
        # await orders > harvest > offload >...
        'initial': 'await orders',
        'events': [
            {'name': 'go to flower', 'src': 'await orders', 'dst': 'harvest'},
            {'name': 'harvest complete', 'src': 'harvest', 'dst': 'head back'},
            {'name': 'begin offload', 'src': 'head back', 'dst': 'offload'},
            {'name': 'offload complete', 'src': 'offload', 'dst': 'await orders'}
        ],
    })


# Scout finite state machine


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
