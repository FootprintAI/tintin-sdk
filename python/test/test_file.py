import os
import unittest
from unittest import mock

from tintin.file import FileManager 

class TestFileDownload(unittest.TestCase):
    debug = True
    host = 'https://api.tintin.footprint-ai.com'
    m = mock.patch.dict(os.environ, {'TINTIN_SESSION_TEMPLATE_PVC_NAME': 'project-2x2dw41yr5v9omyvmn0768kzelg3p5',
    'TINTIN_SESSION_TEMPLATE_PROJECT_ID': '2x2dw41yr5v9omyvmn0768kzelg3p5',
    'TINTIN_SESSION_TEMPLATE_PROJECT_TOKEN_MINIO_DOWNLOAD': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIqLmZvb3RwcmludC1haS5jb20iLCJleHAiOjIyNDY2NzUzNzEsImp0aSI6IjFiZjJmZWZhLWQ5ZTItNDI0Ny1hZTFhLTg1NGQyYjNkMDkzNSIsImlhdCI6MTYxNTk1NTM3MSwiaXNzIjoiYXV0aG9yaXphdGlvbi5mb290cHJpbnQtYWkuY29tIiwibmJmIjoxNjE1OTU1MzcxfQ.GhM9n4esNrDvf3dBGSOLoeWDzKwnxACq2BB9zXxY34cQ6T6RyTQOHipNiBsLyDabYjrrCrvtBFSvPpDMayoVMA',
        })
    def test_http_file_download(self):
        self.m.start()
        mgr = FileManager(self.host, self.debug)
        self.assertEqual(mgr.download('/tmp',
            ['https://api.tintin.footprint-ai.com/api/v1/project/2x2dw41yr5v9omyvmn0768kzelg3p5/minio/object/testdata/1.jpg'],
        ), True)
        self.m.stop()

    def test_localpath_file_download(self):
        self.m.start()
        mgr = FileManager(self.host, self.debug)
        self.assertEqual(mgr.download('/tmp',
            ['/testdata/1.jpg'],
        ), True)
        self.m.stop()

    def test_localpath_download_notfound(self):
        self.m.start()
        mgr = FileManager(self.host, self.debug)
        self.assertEqual(mgr.download('/tmp',
            ['/testdata/notfound.jpg'],
        ), False)
        self.m.stop()

    def test_localpath_dir_download(self):
        self.m.start()
        mgr = FileManager(self.host, self.debug)
        self.assertEqual(mgr.download('/tmp',
            ['/testdata'],
            self.debug,
        ), True)
        self.m.stop()

    def test_file_upload(self):
        self.m.start()
        mgr = FileManager(self.host, self.debug)
        self.assertEqual(mgr.upload('/testupload', './testdata'), True)
        self.m.stop()

if __name__ == '__main__':
    unittest.main()
