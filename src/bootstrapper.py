import di
from typing import Callable
from functools import lru_cache
from services.security import Security
from services.agent import AgentFactory
from controllers.controller import IController
from controllers.google_controller import GoogleController


class Bootstapper:

    def bootstrap(self):
        c = Bootstapper.container()
        c.register_instance(di.IContainer, c)
        c.register_instance(di.IFactory, di.Factory(c))

        # services
        c.register_singleton(Security)

        # controllers
        c.register(IController, GoogleController, "google")

        AgentFactory.listen()
        AgentFactory.load()

        return c

    @staticmethod
    @lru_cache()
    def container():
        return di.Container()
