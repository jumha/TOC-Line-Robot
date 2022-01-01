import bullCow

from transitions import Machine
from transitions.extensions import MachineFactory

import pygraphviz




from utils import send_text_message

diagram_cls = MachineFactory.get_predefined(graph = True)

class TocMachine(object):
#class TocMachine(GraphMachine):


    states=["initial", "gaming", "finish"]


    def __init__(self, userId):
        self.userId = userId

        self.number = 1234

        self.choice = 5

        self.machine = diagram_cls(model=self, states=TocMachine.states, initial='initial')

        self.machine.add_transition(trigger='start', source='initial', dest='gaming', conditions= ["is_going_to_gaming"])

        self.machine.add_transition(trigger='wrong', source='gaming', dest='gaming')

        self.machine.add_transition(trigger='correct', source='gaming', dest='finish')

        self.machine.add_transition(trigger='restart', source='finish', dest='gaming')

        self.machine.add_transition(trigger='loss', source='gaming', dest='finish')

        self.machine.add_transition(trigger='quit', source='*', dest='initial')
        #self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_gaming(self, event):
        text = event.message.text
        return text.lower() == "新遊戲"



