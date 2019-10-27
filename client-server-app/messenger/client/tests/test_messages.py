import datetime
import sys
import unittest

sys.path.append(".")
sys.path.append("..")

from jim.config import ENCODING
import jim.messages


class TestMessages(unittest.TestCase):
    def setUp(self) -> None:
        self.quit = {}
        self.authenticate = {
            "action": "authenticate",
            "time": datetime.datetime.now().timestamp(),
            "user": {"account_name": "test", "password": "test"},
        }
        self.presence = {
            "action": "presence",
            "time": datetime.datetime.now().timestamp(),
            "type": "status",
            "user": {"account_name": "test", "status": "here"},
        }
        self.msg = {
            "action": "msg",
            "time": datetime.datetime.now().timestamp(),
            "from": "source",
            "to": "destination",
            "encoding": ENCODING,
            "message": "test_message",
        }
        self.success_status = {
            "response": 200,
            "time": datetime.datetime.now().timestamp(),
            "alert": "OK",
        }
        self.fail_status = {
            "response": 500,
            "time": datetime.datetime.now().timestamp(),
            "error": "Internal server error",
        }

    def test_quit(self):
        self.assertEqual(jim.messages.quit(), {"action": "quit"})
        self.assertNotEqual(jim.messages.quit(), {"action": "exit"})

    def test_authenticate(self):
        self.assertEqual(
            [
                jim.messages.authenticate("test", "test")[x]
                for x in ("user", "action")
            ],
            [self.authenticate[x] for x in ("user", "action")],
        )

    def test_presence(self):
        self.assertEqual(
            [
                jim.messages.presence("test", "here")[x]
                for x in ("user", "type", "action")
            ],
            [self.presence[x] for x in ("user", "type", "action")],
        )

    def test_probe(self):
        self.assertTrue(jim.messages.probe()["action"] == "probe")

    def test_join(self):
        self.assertTrue(jim.messages.join("test")["action"] == "join")
        self.assertTrue(jim.messages.join("test")["room"] == "test")

    def test_leave(self):
        self.assertTrue(jim.messages.leave("test")["action"] == "leave")
        self.assertTrue(jim.messages.leave("test_room")["room"] == "test_room")

    def test_msg(self):
        self.assertEqual(
            [
                jim.messages.msg("test_message", "source", "destination")[x]
                for x in ("from", "to", "message", "action")
            ],
            [self.msg[x] for x in ("from", "to", "message", "action")],
        )

    def test_get_contanct(self):
        self.assertEqual(
            [
                jim.messages.get_contacts("test_username")[x]
                for x in ("action", "user")
            ],
            ["get_contacts", "test_username"],
        )

    def test_add_contact(self):
        self.assertEqual(
            [
                jim.messages.add_contact("test", "test_contact")[x]
                for x in ("action", "user", "contact")
            ],
            ["add_contact", "test", "test_contact"],
        )

    def test_del_contact(self):
        self.assertEqual(
            [
                jim.messages.del_contact("test", "test_contact")[x]
                for x in ("action", "user", "contact")
            ],
            ["del_contact", "test", "test_contact"],
        )


if __name__ == "__main__":
    unittest.main()
