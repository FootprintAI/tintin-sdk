import os
import unittest
from unittest import mock

from tintin.file import FileManager 

debug = False
host = 'https://api.tintin.footprint-ai.com'
project_id = '1vpe4zw1y68gnj308j7xol0krd3529'
m = mock.patch.dict(os.environ, { 'TINTIN_SESSION_TEMPLATE_PROJECT_ID': project_id,
'TINTIN_SESSION_TEMPLATE_PROJECT_TOKEN_MINIO_DOWNLOAD': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIqLmZvb3RwcmludC1haS5jb20iLCJleHAiOjIyNTc3ODA4ODgsImp0aSI6IjQ0ODkxNDVlLTAzZWEtNDA2Yy1iZTFmLWViMWUxNjcxNmJlOCIsImlhdCI6MTYyNzA2MDg4OCwiaXNzIjoiYXV0aG9yaXphdGlvbi5mb290cHJpbnQtYWkuY29tIiwibmJmIjoxNjI3MDYwODg4fQ.uMRPw5JIW9O35MqsPhLJ2FR-fzx7IadRz51cVmeX_f94O3900M8r2B4ikcCdoDAXQpsTvfZpj88gBewtoOdz_Q',
})

class TestBFileDownload(unittest.TestCase):
    global m
    global host
    global debug

    def test_http_file_download(self):
        m.start()
        mgr = FileManager(host, debug)
        self.assertEqual(mgr.download('/tmp',
            ['https://api.tintin.footprint-ai.com/api/v1/project/{}/minio/object/testupload/testdata/1.txt'.format(project_id)],
        ), True)
        m.stop()

    def test_localpath_file_download(self):
        m.start()
        mgr = FileManager(host, debug)
        self.assertEqual(mgr.download('/tmp',
            ['/testupload/testdata/1.txt'],
        ), True)
        m.stop()

    def test_localpath_download_notfound(self):
        m.start()
        mgr = FileManager(host, debug)
        self.assertEqual(mgr.download('/tmp',
            ['/testupload/testdata/notfound.jpg'],
        ), False)
        m.stop()

    def test_localpath_dir_download(self):
        m.start()
        mgr = FileManager(host, debug)
        self.assertEqual(mgr.download('/tmp',
            ['/testdata'],
            debug,
        ), True)
        m.stop()

class TestAFileUpload(unittest.TestCase):
    global m
    global host
    global debug

    def test_folder_upload(self):
        m.start()
        mgr = FileManager(host, debug)
        # should upload to destination with /testupload/testdata/...
        self.assertEqual(mgr.upload('/testupload', './testdata'), True)
        m.stop()

    def test_file_upload(self):
        m.start()
        mgr = FileManager(host, debug)
        # should upload to destination /testupload/testdata/1.txt individual file
        self.assertEqual(mgr.upload('/testupload', './testdata/1.txt'), True)
        m.stop()

if __name__ == '__main__':
    unittest.main()
