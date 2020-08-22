import os
import os.path
import rasa
import logging
import json
import redis
from datetime import datetime
from aiohttp import web
from functools import lru_cache
from rasa.core.interpreter import NaturalLanguageInterpreter, RasaNLUInterpreter
from rasa.core.agent import Agent
from controllers.controller import routes, IController
from bootstrapper import Bootstapper

ROOT = os.path.dirname(__file__)
container=Bootstapper().bootstrap()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = web.Application()

    controllers = container.resolve_all(IController)
    for controller in controllers:
        routes.add_class_routes(controller)

    app.add_routes(routes)
    web.run_app(app, port=80)


