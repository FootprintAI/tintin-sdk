import os
import unittest
from unittest import mock

from tintin.file import download

class TestFileDownload(unittest.TestCase):
    # FIXME: TINTIN_SESSION_TEMPLATE_PVC_NAME contains `project-` prefix, which
    # may not be appropriate for the purpose.
    m = mock.patch.dict(os.environ, {'TINTIN_SESSION_TEMPLATE_PVC_NAME': 'project-1vpe4zw1y68gnj38q7xol0krd3529n',
    'TINTIN_SESSION_TEMPLATE_PROJECT_TOKEN_MINIO_DOWNLOAD': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIqLmZvb3RwcmludC1haS5jb20iLCJleHAiOjIyNDYxNTQwMzgsImp0aSI6IjUyYzI2ODYyLTE1OGYtNGMxZS04N2VhLWY1ZDFhZWQxM2E1ZSIsImlhdCI6MTYxNTQzNDAzOCwiaXNzIjoiYXV0aG9yaXphdGlvbi5mb290cHJpbnQtYWkuY29tIiwibmJmIjoxNjE1NDM0MDM4fQ.LVY5vpzLLQz5FBEUYs_pN8XmoqTYRzr-IBdTZL5O0-3oe3LdmksXZYxiB1ydSCii1s-Q9Not7XZAO7G4mGzWMg',
        })
    def test_http_download(self):
        self.m.start()
        self.assertEqual(download('/tmp',
            ['https://api.tintin.footprint-ai.com/api/v1/project/1vpe4zw1y68gnj38q7xol0krd3529n/minio/object/test/1.jpg'],
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
