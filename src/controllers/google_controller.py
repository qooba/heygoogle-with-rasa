import os
import json
import logging
from services.security import Security
from services.agent import AgentFactory
from controllers.controller import routes, Controller
from rasa.core.channels.channel import UserMessage

logger = logging.getLogger(__name__)

class GoogleController(Controller):
    def __init__(self, security: Security):
        super().__init__()
        self.security=security

    @routes.get('/')
    async def hello(self, request):
        text = request.rel_url.query['text']
        response=await AgentFactory.load().handle_text(text)
        logger.info(json.dumps(response))
        return self.json(response)

    @routes.post("/google_action")
    async def google_webhook(self, request):
        req = await request.json()
        print(json.dumps(req))
        authorization= request.headers['Google-Assistant-Signature']
        print(authorization)
        print(request.headers)

        #self.security.verify_token(authorization)

        session_id = req['session'].get('id', None)
        locale = req['user']['locale']
        lang = locale[:2]
        if req['intent']['name'] == 'actions.intent.MAIN':
            response_text=os.environ['WELCOME_TEXT']
        else:
            text = req['intent']['query']
            user_message=UserMessage(text=text, sender_id=session_id)
            response=await AgentFactory.load().handle_message(user_message)
            logger.info(json.dumps(response))
            response_text=response[0]['text']

        resp={
          "session": {
            "id": "example_session_id",
            "params": {}
          },
          "prompt": {
            "override": False,
            "firstSimple": {
              "speech": response_text,
              "text": response_text
            }
          },
          "scene": {
            "name": "Main",
            "slots": {},
            "next": {
              "name": "Main"
            }
          }
        }

        return self.json(resp)
#
#
#    @routes.post('/google_action')
#    def google_action(item: dict, authorization: str = Header(None)):
#        print(item, file=sys.stderr)
#        print(authorization, file=sys.stderr)
#        context = ConversationContext()
#        context.request = item
#        context: ConversationContext = handler_manager.invoke(context)
#        print(context.response, file=sys.stderr)
#        return json.loads(context.response)



