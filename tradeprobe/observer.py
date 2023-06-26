from abc import ABCMeta, abstractmethod


class Observer:

    __metaclass__ = ABCMeta

    @abstractmethod
    def handle_event(self, event):
        raise NotImplementedError("Implement handle_event()")
