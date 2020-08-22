import os
import os.path
import logging
import json
import redis
from datetime import datetime
from aiohttp import web
from functools import lru_cache
from rasa.core.interpreter import NaturalLanguageInterpreter, RasaNLUInterpreter
from rasa.core.agent import Agent
from rasa.core.tracker_store import RedisTrackerStore

logger = logging.getLogger(__name__)

project_name=os.environ['PROJECT_NAME']
language=os.environ['LANGUAGE']
fmodel_history=f'model_history.{language}.log'
os.environ["AWS_DEFAULT_REGION"]="us-east-1"
os.environ["BUCKET_NAME"]=f'{project_name}-{language}'
os.environ["AWS_ENDPOINT_URL"]="http://minio:9000"
os.environ["AWS_ACCESS_KEY_ID"]=os.environ["MINIO_ACCESS_KEY"]
os.environ["AWS_SECRET_ACCESS_KEY"]=os.environ["MINIO_SECRET_KEY"]

class AgentFactory:

    @staticmethod
    @lru_cache()
    def listen():
        r = redis.Redis(host='redis', port=6379, db=0)
        p = r.pubsub()

        def custom_handler(message):
            print(message)
            os.environ['MODEL_NAME']=message['data'].decode().replace('.tar.gz','')
            AgentFactory.load.cache_clear()

        topic_name=f'{project_name}-{language}*'
        print(f"TOPIC SUBSCRIBE: {topic_name}")
        p.psubscribe(**{topic_name:custom_handler})
        thread = p.run_in_thread(sleep_time=0.1)

    @staticmethod
    @lru_cache()
    def load():
        initial_model_name=os.environ['INITIAL_MODEL_NAME']
        try:
            model_name=os.environ['MODEL_NAME']
        except KeyError:
            if os.path.isfile(fmodel_history):
                with open(fmodel_history,'r') as f:
                    model_name=f.readlines()[-1].split()[0]
                    print(model_name)
            else:
                model_name=initial_model_name

        timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        with open(fmodel_history,'a') as f:
            f.write(f'{model_name} {timestamp}\n')

        tracker_store=RedisTrackerStore(None, host='redis', port=6379)

        return Agent.load_from_remote_storage(
            tracker_store=tracker_store,
            remote_storage='aws',
            model_name=model_name)


