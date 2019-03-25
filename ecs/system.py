import inject

from message_broker import MessageBroker
from ecs import ebs


class System(ebs.Applicator):
    @inject.params(event_system=MessageBroker)
    def __init__(self, event_system: MessageBroker = None):
        super(System, self).__init__()

        self.componenttypes = ()
        self.event_system = event_system

    def process(self, world, components):
        pass
