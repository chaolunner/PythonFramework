from rx.internal.basic import identity, default_comparer
from rx.disposables import AnonymousDisposable
from rx.core import AnonymousObservable
from rx.subjects import Subject
from rx.internal import noop
from rx import Observer


class ReactiveProperty:
    def __init__(self, value=None):
        self.is_disposed = False
        self._value = value
        self.publisher = Subject()

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, value):
        self.set_value(value)
        if self.is_disposed is True:
            return
        p = self.publisher
        if p is not None:
            p.on_next(value)

    def set_value(self, value):
        self._value = value

    def set_value_and_force_notify(self, value):
        self.set_value(value)
        if self.is_disposed is True:
            return
        p = self.publisher
        if p is not None:
            p.on_next(value)

    def subscribe(self, on_next=None, on_error=None, on_completed=None, observer: Observer = None):
        p = self.publisher
        if self.is_disposed is True:
            if observer is not None:
                observer.on_completed()
            return AnonymousDisposable(noop)

        if p is not None:
            subscription = p.subscribe(on_next=on_next, on_completed=on_completed, on_error=on_error, observer=observer)
            if observer is not None:
                observer.on_next(self.value)
            return subscription
        else:
            if observer is not None:
                observer.on_completed()
            return AnonymousDisposable(noop)

    def distinct_until_changed(self, key_mapper=None, comparer=None):
        source = self
        key_mapper = key_mapper or identity
        comparer = comparer or default_comparer

        def subscribe(observer, scheduler=None):
            has_current_key = [False]
            current_key = [None]

            def on_next(value):
                comparer_equals = False
                try:
                    key = key_mapper(value)
                except Exception as exception:
                    observer.on_error(exception)
                    return

                if has_current_key[0]:
                    try:
                        comparer_equals = comparer(current_key[0], key)
                    except Exception as exception:
                        observer.on_error(exception)
                        return

                if not has_current_key[0] or not comparer_equals:
                    has_current_key[0] = True
                    current_key[0] = key
                    observer.on_next(value)

            return source.subscribe(on_next, observer.on_error, observer.on_completed)

        return AnonymousObservable(subscribe)

    def dispose(self):
        if self.is_disposed is False:
            self.is_disposed = True
            p = self.publisher
            if p is not None:
                try:
                    p.on_completed()
                finally:
                    p.dispose()
                    self.publisher = None
