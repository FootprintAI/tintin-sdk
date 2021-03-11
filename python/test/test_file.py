import os
import unittest
from unittest import mock

from tintin.file import download

class TestFileDownload(unittest.TestCase):
    # FIXME: TINTIN_SESSION_TEMPLATE_PVC_NAME contains `project-` prefix, which
    # may not be appropriate for the purpose.
    m = mock.patch.dict(os.environ, {'TINTIN_SESSION_TEMPLATE_PVC_NAME': 'project-8yv8p5x3o42l1m1xjzwrk7dneg690v',
    'TINTIN_SESSION_TEMPLATE_PROJECT_ID': '8yv8p5x3o42l1m1xjzwrk7dneg690v',
    'TINTIN_SESSION_TEMPLATE_PROJECT_TOKEN_MINIO_DOWNLOAD': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIqLmZvb3RwcmludC1haS5jb20iLCJleHAiOjIyNDYxNTk3MzgsImp0aSI6IjVmMmZkZTMyLTU2MDYtNDE5Mi05ZTgyLWEyNzU2N2NlZDg5NyIsImlhdCI6MTYxNTQzOTczOCwiaXNzIjoiYXV0aG9yaXphdGlvbi5mb290cHJpbnQtYWkuY29tIiwibmJmIjoxNjE1NDM5NzM4fQ.ZZNBGLytSNNqJRmLmDdZMI6qtcWhiMcvQMhaQrFle9DJ_q6nFjEe1y4_od_bWBhxRa8NLG2DxeH6vT6a3Q2xeQ',
        })
    def test_http_download(self):
        self.m.start()
        self.assertEqual(download('/tmp',
            ['https://api.tintin.footprint-ai.com/api/v1/project/8yv8p5x3o42l1m1xjzwrk7dneg690v/minio/object/test/1.jpg'],
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
