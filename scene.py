import abc


class Scene:
    def __init__(self):
        self.bindings()

    @abc.abstractmethod
    def bindings(self):
        """Binding objects that require injection."""
