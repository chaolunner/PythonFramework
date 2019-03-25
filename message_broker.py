from rx.subjects import Subject


class MessageBroker:
    def __init__(self):
        self.is_disposed = False
        self.notifiers = {}

    def publish(self, message: object = None):
        notifier = None  # type: Subject
        t = type(message)
        if self.is_disposed:
            return
        if t in self.notifiers:
            notifier = self.notifiers.get(t)
        else:
            return
        notifier.on_next(message)

    def receive(self, t: type = None):
        notifier = None  # type: Subject
        if self.is_disposed:
            raise Exception("Object Disposed Error", "MessageBroker")
        if t in self.notifiers:
            notifier = self.notifiers.get(t)
        else:
            notifier = Subject()
            self.notifiers[t] = notifier
        return notifier

    def dispose(self):
        if self.is_disposed is False:
            self.is_disposed = True
            self.notifiers.clear()
