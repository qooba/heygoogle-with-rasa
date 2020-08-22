import abc
import sys
import di
from nlu import Nlu
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from models import ConversationContext, Route, User


class HandlerManager(ab.IHandlerManager):
    def __init__(self, factory: di.IFactory):
        self.factory = factory

    def invoke(self, context: ConversationContext):
        handlers = self.factory.create_all(ab.IHandler)
        handlers.sort(key=lambda x: x.position, reverse=False)
        for h in handlers:
            context = h.invoke(context)

        return context


class BaseHandler:

    def __init__(self):
        self._position = 0

    @property
    def position(self) -> int:
        return self._position

    @abc.abstractmethod
    def invoke(self, context: ConversationContext):
        raise NotImplementedError('invoke')


class ContextHandler(BaseHandler):
    def __init__(self):
        self._position = 0

    def invoke(self, context: ConversationContext):
        return context


class UserHandler(BaseHandler):
    def __init__(self):
        self._position = 1

    def invoke(self, context: ConversationContext):
        user = User()
        user.idToken = context.request['user'].get('idToken', None)
        user.locale = context.request['user']['locale']
        user.lang = user.locale[:2]
        user.lastSeen = context.request['user'].get('lastSeen', None)
        user.userStorage = context.request['user'].get('userStorage', None)
        context.user = user
        return context


class RouteHandler(BaseHandler):
    def __init__(self, nlu: ab.INlu):
        self.nlu = nlu
        self._position = 2

    def invoke(self, context: ConversationContext):

        context.route = Route()
        context.data = {}
        text = context.request['inputs'][0]["rawInputs"][0].get("query",'')
        context.route.intent = context.request["inputs"][0]["intent"]
        context.data['is_main'] = context.route.intent == "actions.intent.MAIN"
        nlu_response = self.nlu.parse_nlu(text,context.user.lang)
        intent = nlu_response['intent']['name']

        if intent:
            context.route.intent = intent
            context.data = {item['entity']: item['value']
                        for item in nlu_response['entities']}
        elif context.user.lastSeen is None and context.route.intent == "actions.intent.MAIN":
            context.route.intent = "actions.intent.INIT"

        return context


class ReplyHandler(BaseHandler):

    def __init__(self, reply_factory: ab.IReplyFactory):
        self.reply_factory = reply_factory
        self._position = 3

    def invoke(self, context: ConversationContext):
        try:
            reply_builder: ab.IReplyBuilder = self.reply_factory.create(context)
            context.response = reply_builder.prepare(context)
        except Exception as ex:
            print(ex, file=sys.stderr)
            context.route.intent = "actions.intent.UNKNOWN"
            reply_builder: ab.IReplyBuilder = self.reply_factory.create(context)
            context.response = reply_builder.prepare(context)

        return context


class DispatchHandler(BaseHandler):
    def __init__(self):
        self._position = 4

    def invoke(self, context: ConversationContext):
        return context


class ContextKeeperHandler(BaseHandler):
    def __init__(self):
        self._position = 5

    def invoke(self, context: ConversationContext):
        return context
