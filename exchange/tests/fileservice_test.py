import os
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from django.core.files.uploadedfile import SimpleUploadedFile
from exchange import settings
import shutil
import pytest

class FileItemResourceTest(ResourceTestCaseMixin, TestCase):

    def setUp(self):
        super(FileItemResourceTest, self).setUp()

        # turn on streaming_support so that test_view can test the view endpoint
        # without streaming_supported set to True, view endpoint will behave exactly like download
        settings.FILESERVICE_CONFIG['streaming_supported'] = True

        # Create a user.
        self.username = 'admin'
        self.password = 'exchange'

        self.upload_filename = 'fileservice_test_upload.jpg'
        self.download_filename = 'fileservice_test_download.jpg'

        self.upload_file = SimpleUploadedFile(
            name=self.upload_filename,
            content=open(os.path.join(os.path.dirname(__file__), self.upload_filename), 'rb').read(),
            content_type='image/jpg',
        )

        self.upload_url = '/api/fileservice/'
        self.download_url = '/api/fileservice/download/{0}'.format(self.download_filename)
        self.view_url = '/api/fileservice/view/{0}'.format(self.download_filename)

    def test_upload(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(self.upload_url, {'file': self.upload_file}, follow=True)
        self.assertHttpCreated(resp)

    def test_download(self):
        # copy the file we want to download to the fileservice media folder
        shutil.copy(os.path.join(os.path.dirname(__file__), self.download_filename),
                    settings.FILESERVICE_CONFIG['store_dir'])
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.download_url, follow=True)
        self.assertEquals(resp.get('Content-Disposition'), 'attachment; filename="{}"'.format(self.download_filename))

    def test_view(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.view_url, follow=True)
        # pytest.set_trace()
        '''
        the view end point is meant for playing back video with random access which means the progress indicator can be
        dragged around. FO the random access to work properly, instead of django serving up the video, nginx or apache
        have to serve it up and the fileservice adds the 'X-Sendfile' and the equivalent 'X-Accel-Redirect' so that
        they take it from there. Even if that happens, at least one of the headers should technically be present.
        '''
        self.assertTrue(resp.get('X-Sendfile') or resp.get('X-Accel-Redirect'))
