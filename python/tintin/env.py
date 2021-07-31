import os

from configparser import ConfigParser
from importlib.resources import read_text

class Environ():
    def __init__(self):
        cfg = ConfigParser()
        cfg.read_string(read_text('tintin', 'config.txt'))

        self.minio_token_name = os.environ.get(cfg.get('env', 'minio_token_name'))
        self.project_name = os.environ.get(cfg.get('env', 'project_name'))
        self.minio_access_key = os.environ.get(cfg.get('env', 'minio_access_key'))
        self.minio_access_secret = os.environ.get(cfg.get('env',
            'minio_access_secret'))
        self.minio_bucket = os.environ.get(cfg.get('env', 'minio_bucket'))
        self.minio_endpoint = os.environ.get(cfg.get('env', 'minio_endpoint'))

        print('self.minio_token_name:', self.minio_token_name)
        print('self.project_name:', self.project_name)
        print('self.minio_access_key:', self.minio_access_key)
        print('self.minio_access_secret:', self.minio_access_secret)
        print('self.minio_bucket:', self.minio_bucket)
        print('self.minio_endpoint:', self.minio_endpoint)

