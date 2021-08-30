import unittest

import datetime
import json

from app.main import db
from app.main.model.chat import Chat
from app.test.base import BaseTestCase


class TestChatModel(BaseTestCase):

    def test_chat_list(self):
        response = self.client.get('/chat/', content_type='application/json')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_chat_creation(self):
        self.client.post('/chat/test', content_type='application/json')
        response = self.client.get('/chat/test', content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data['name'] == 'test')


if __name__ == '__main__':
    unittest.main()

