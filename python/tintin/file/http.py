import os
import logging

from tintin.api import TintinApi
from tintin.env import Environ
from tintin.logging import httpclient_logging_activate
from tintin.util import write_response_to_file
from tintin.util import list_all_files

from tintin.file.file_manager import FileManagerInterface

class FileManager(FileManagerInterface):
    """FileManager
        Implements http interface for upload/download files
    """
    def __init__(self, host: str, verbose: bool):
        """__init__.

        Args:
            host (str): host
            verbose (bool): verbose
        """
        self.host = host
        self.env = Environ()
        self.ApiStub = TintinApi(host, self.env)
        self.verbose = verbose

        if verbose:
            logging.basicConfig(level=logging.DEBUG)
            httpclient_logging_activate()
        else:
            logging.basicConfig(level=logging.INFO)

    def list(self, prefix: str) -> [str]:
        """list.

        Args:
            prefix (str): prefix

        Returns:
            [str]:
        """
        list_uri = 'api/v1/project/{}/minio/object?prefix={}&recursive=True'.format(self.__get_project_id(), prefix)
        resp = self.ApiStub.get(list_uri)
        if resp.status_code != 200:
            logging.info('{} has invalid response code: {}, error msg:{}'.format(prefix, resp.status_code, resp.content))
            return []
        local_object_paths: [str] = [];
        for obj in resp.json()['objectInfoList']:
            local_object_paths.append(obj['name'])
        return local_object_paths


    def upload(self, prefix: str, local_dir: str):
        """upload.

        Args:
            prefix (str): prefix
            local_dir (str): local_dir
        """
        local_file_paths = list_all_files(local_dir)
        if not local_file_paths:
            logging.info('nothing to be uploaded')
            return False
        for local_file_path in local_file_paths:
            dst_path = os.path.join(prefix, local_file_path)
            logging.info('{} has been upload.'.format(dst_path))
            object_uri = 'api/v1/project/{}/minio/object/{}'.format(self.__get_project_id(), dst_path)
            with open(local_file_path, 'rb') as f:
                resp = self.ApiStub.put(object_uri, f.read())
                if resp.status_code != 200:
                   logging.info('{} has invalid response code: {}, error msg:{}'.format(local_file_path, resp.status_code, resp.content))
                   return False
        return True

    def download(self, dst: str, filepaths: [str], recursive: bool = False):
        """download.

        Args:
            dst (str): dst
            filepaths ([str]): filepaths
            recursive (bool): recursive
        """
        local_file_paths:[str] = []
        for filepath in filepaths:
            object_path = self.__get_object_path(filepath)
            local_file_paths.append(object_path)

        if recursive:
            local_file_paths_with_recursive:[str] = []
            # resolve filepaths all
            for local_file_path in local_file_paths:
                local_file_paths_with_recursive.extend(self.list(local_file_path))
            local_file_paths = local_file_paths_with_recursive

        for local_file_path in local_file_paths:
            object_uri = 'api/v1/project/{}/minio/object/{}'.format(self.__get_project_id(), local_file_path)
            resp = self.ApiStub.get(object_uri)
            if resp.status_code != 200:
                logging.info('{} has invalid response code: {}, error msg:{}'.format(local_file_path, resp.status_code, resp.content))
                return False
            dst_path = os.path.join(dst, local_file_path)
            write_response_to_file(dst_path, resp)
            logging.info('{} has been downloaded.'.format(dst_path))

        return True

    def __get_object_path(self, networkorlocalpath: str) -> str:
        """__get_object_path.

        Args:
            networkorlocalpath (str): networkorlocalpath

        Returns:
            str:
        """
        minio_network_prefix = os.path.join(self.host, 'api/v1/project',
                self.__get_project_id(), 'minio/object/')
        if networkorlocalpath.startswith(minio_network_prefix):
            return networkorlocalpath[len(minio_network_prefix):]
        # check leading /
        if networkorlocalpath.startswith('/'):
            return networkorlocalpath[len('/'):]
        return networkorlocalpath

    def __get_project_id(self) -> str:
        """__get_project_id. (private)

        Args:

        Returns:
            str:
        """
        prefix = 'project-'
        project = self.env.project_name
        if project.startswith(prefix):
            return project[len(prefix):]
        return project

