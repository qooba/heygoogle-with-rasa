import os
import boto3
import redis
from botocore.client import Config

def upload_model(project_name: str, language: str, model: str):
    s3=boto3.resource("s3",endpoint_url="http://minio:9000",
        aws_access_key_id=os.environ["MINIO_ACCESS_KEY"],
        aws_secret_access_key=os.environ["MINIO_SECRET_KEY"],
        config=Config(signature_version="s3v4"),region_name="us-east-1")
    bucket_name=f'{project_name}-{language}'
    print(f"BUCKET NAME: {bucket_name}") 
    bucket_exists=s3.Bucket(bucket_name) in s3.buckets.all() or s3.create_bucket(Bucket=bucket_name)
    s3.Bucket(bucket_name).upload_file(f"/builds/root/{project_name}/{language}/models/{model}",model)


def publish_event(project_name: str, language: str, model: str):
    topic_name=f'{project_name}-{language}'
    print(f"TOPIC NAME: {topic_name}") 
    client=redis.Redis(host="redis", port=6379, db=0);
    client.publish(topic_name, model)

if __name__ == '__main__':
    import argparse

    project_name=os.environ["PROJECT_NAME"]

    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--language', metavar='path', required=True,
                        help='the model language')

    args = parser.parse_args()
    model=os.listdir(f"/builds/root/{project_name}/{args.language}/models/")[0]
    print("Uploading model")
    upload_model(project_name=project_name, language=args.language, model=model)

    print("Publishing event")
    publish_event(project_name=project_name, language=args.language, model=model)
