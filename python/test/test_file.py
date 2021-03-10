import os
import unittest
from unittest import mock

from tintin.file import download

class TestFileDownload(unittest.TestCase):
    m = mock.patch.dict(os.environ, {'TINTIN_SESSION_TEMPLATE_PVC_NAME': 'x163vyx2rw4e7q6rqpglo9dkn580z7',
    'TINTIN_SESSION_TEMPLATE_PROJECT_TOKEN_MINIO_DOWNLOAD': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIqLmZvb3RwcmludC1haS5jb20iLCJleHAiOjIyNDU5ODAzNDQsImp0aSI6IjhkYmVkN2I5LWNiNGQtNDczYS05YjQ0LTJkNmMwNzZkNGZhYSIsImlhdCI6MTYxNTI2MDM0NCwiaXNzIjoiYXV0aG9yaXphdGlvbi5mb290cHJpbnQtYWkuY29tIiwibmJmIjoxNjE1MjYwMzQ0fQ.jQdrVJFqz7AtbYFg8AfKbEg39Dmaq3yfLUKdjU8xjlQHJEySOOZ0WqmDAheHXUJZGL2wi-bHGr_5ao-zb6Nfkg',
        })
    def test_http_download(self):
        self.m.start()
        self.assertEqual(download('/tmp',
            ['https://api.tintin.footprint-ai.com/api/v1/project/x163vyx2rw4e7q6rqpglo9dkn580z7/minio/object/test/1.jpg'],
        ), True)
        self.m.stop()

    def test_localpath_download(self):
        self.m.start()
        self.assertEqual(download('/tmp',
            ['/test/1.jpg'],
        ), True)
        self.m.stop()

    def test_localpath_download_notfound(self):
        self.m.start()
        self.assertEqual(download('/tmp',
            ['/test/notfound.jpg'],
        ), False)
        self.m.stop()



if __name__ == '__main__':
    unittest.main()
