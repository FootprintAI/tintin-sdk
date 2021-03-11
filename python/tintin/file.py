import os
import requests
import logging

from configparser import ConfigParser
from importlib.resources import read_text

from tintin.auth import MinioAuth
from tintin.logging import httpclient_logging_activate

CFG = None

def init_config():
    global CFG
    if CFG is not None:
        return
    CFG = ConfigParser()
    CFG.read_string(read_text('tintin', 'config.txt'))

logging.basicConfig(level=logging.DEBUG)

def download(dst: str, filepaths: [str], verbose: bool = False):
    """download.

    download multiple files into local dst folder

    Args:
        dst (str): dst
        filepaths ([str]): filepaths
        verbose (bool): verbose
    """

    init_config()

    if verbose:
        httpclient_logging_activate()

    token = os.environ.get(CFG.get('env', 'minio_token_name'))
    for filepath in filepaths:
        normalized_filepath = normalized_http_path(filepath)
        normalized_localpath = normalized_local_path(filepath)
        r = requests.get(normalized_filepath, auth=MinioAuth(token))
        if r.status_code is not 200:
            logging.info('{} has invalid response code: {}, error msg:{}'.format(normalized_localpath, r.status_code,
                        r.content))
            return False
        dst_path = os.path.join(dst, normalized_localpath)
        writefile(dst_path, r)
        logging.info('{} has been downloaded.'.format(dst_path))

    return True

def normalized_http_path(filepath: str) -> str:
    """normalized_http_path.

        normalized any given filepath into https address

    Args:
        filepath (str): filepath

    Returns:
        str:
    """
    if filepath.startswith('https://') or filepath.startswith('http://'):
        return filepath
    if filepath.startswith('/'):
        filepath = filepath[len('/'):] # strip leading '/'
    api_url = CFG.get('endpoint', 'api_url')
    project = get_project_id()
    normalized_path = os.path.join(api_url, 'api/v1/project', project, 'minio/object', filepath)
    return normalized_path

def get_project_id() -> str:
    prefix = 'project-'
    project = os.environ.get(CFG.get('env', 'project_name'))
    if project.startswith(prefix):
        return project[len(prefix):]
    return project

def normalized_local_path(filepath: str) -> str:
    """normalized_local_path.

        De-normalize https path into object path

    Args:
        filepath (str): filepath

    Returns:
        str:
    """
    api_url = CFG.get('endpoint', 'api_url')
    project = get_project_id()
    prefix = '{}/api/v1/project/{}/minio/object/'.format(api_url, project)
    if filepath.startswith(prefix):
        return filepath[len(prefix):]
    return filepath

def writefile(filename:str, r):
    """writefile.

        writefile is an utility function which create filename's parent folders
        if not exists and write r.content into filename

    Args:
        filename (str): filename
        r:
    """
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'wb') as f:
        f.write(r.content)

