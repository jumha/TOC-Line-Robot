import bullCow

from transitions import Machine
from transitions.extensions import MachineFactory

import pygraphviz

from graphviz import Graph, Digraph


from utils import send_text_message

diagram_cls = MachineFactory.get_predefined(graph = True)

class TocMachine():
#class TocMachine(GraphMachine):


    states=["initial", "gaming", "finish"]


    def __init__(self):
        self.machine = diagram_cls(model=self, states=TocMachine.states, initial='initial')

        self.machine.add_transition(trigger='start', source='initial', dest='gaming', conditions= ["is_going_to_gaming"])

        self.machine.add_transition(trigger='wrong', source='gaming', dest='gaming')

        self.machine.add_transition(trigger='correct', source='gaming', dest='finish')

        self.machine.add_transition(trigger='restart', source='finish', dest='gaming')

        self.machine.add_transition(trigger='wrong', source='gaming', dest='finish', conditions= ["is_out_of_choice"])

        self.machine.add_transition(trigger='quit', source='*', dest='initial')
        #self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_gaming(self, event):
        text = event.message.text
        return text.lower() == "新遊戲"

    def is_out_of_choice(self, choice):      
        print(choice)
        return choice <= 0


