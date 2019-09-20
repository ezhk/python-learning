import unittest

import datetime
import sys

sys.path.append('.')

import jim.messages
from jim.config import ENCODING


class TestMessages(unittest.TestCase):
    def setUp(self) -> None:
        self.quit = {}
        self.authenticate = {
            "action": "authenticate",
            "time": datetime.datetime.now().timestamp(),
            "user": {
                "account_name": 'test',
                "password": 'test'
            }
        }
        self.presence = {
            "action": "presence",
            "time": datetime.datetime.now().timestamp(),
            "type": "status",
            "user": {
                "account_name": 'test',
                "status": 'here'
            }
        }
        self.msg = {
            "action": "msg",
            "time": datetime.datetime.now().timestamp(),
            "from": 'source',
            "to": 'destination',
            "encoding": ENCODING,
            "message": 'test_message'
        }
        self.success_status = {
            "response": 200,
            "time": datetime.datetime.now().timestamp(),
            "alert": "OK"
        }
        self.fail_status = {
            "response": 500,
            "time": datetime.datetime.now().timestamp(),
            "error": "Internal server error"
        }

    def test_quit(self):
        self.assertEqual(jim.messages.quit(), {'action': 'quit'})
        self.assertNotEqual(jim.messages.quit(), {'action': 'exit'})

    def test_authenticate(self):
        self.assertEqual([jim.messages.authenticate('test', 'test')[x] for x in ('user', 'action')],
                         [self.authenticate[x] for x in ('user', 'action')])

    def test_presence(self):
        self.assertEqual([jim.messages.presence('test', 'here')[x] for x in ('user', 'type', 'action')],
                         [self.presence[x] for x in ('user', 'type', 'action')])

    def test_probe(self):
        self.assertTrue(jim.messages.probe()['action'] == 'probe')

    def test_join(self):
        self.assertTrue(jim.messages.join('test')['action'] == 'join')
        self.assertTrue(jim.messages.join('test')['room'] == 'test')

    def test_leave(self):
        self.assertTrue(jim.messages.leave('test')['action'] == 'leave')
        self.assertTrue(jim.messages.leave('test_room')['room'] == 'test_room')

    def test_msg(self):
        self.assertEqual([jim.messages.msg('test_message', 'source', 'destination')[x]
                          for x in ('from', 'to', 'message', 'action')],
                         [self.msg[x] for x in ('from', 'to', 'message', 'action')])

    def test_response(self):
        self.assertEqual([jim.messages.response(200, 'OK')[x] for x in ('response', 'alert')],
                         [self.success_status[x] for x in ('response', 'alert')])
        self.assertEqual([jim.messages.response(500, 'Internal server error', False)[x] for x in ('response', 'error')],
                         [self.fail_status[x] for x in ('response', 'error')])


if __name__ == "__main__":
    unittest.main()
