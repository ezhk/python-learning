import unittest

import sys

sys.path.append('.')

import jim.utils as utils
import jim.messages as messages
import jim.exceptions as exceptions


class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.raw_data = b'{"test_key": "test_value"}'
        self.parse_data = {'test_key': 'test_value'}

    def test_json_operation(self):
        self.assertEqual(utils.parse_raw_json(self.raw_data), self.parse_data)
        self.assertEqual(utils.make_raw_json(self.parse_data), self.raw_data)

    def test_valid_message(self):
        with self.assertRaises(exceptions.MessageError):
            utils.is_valid_message({})
        self.assertFalse(utils.is_valid_message({'action': 'join'}))
        self.assertTrue(utils.is_valid_message(
            messages.presence("John Galt", "Кто такой Джон Голт?")))

    def test_valid_response(self):
        self.assertFalse(utils.is_valid_response(''))
        self.assertFalse(utils.is_valid_response({'status': 200}))
        self.assertTrue(utils.is_valid_response(messages.response(200)))

    def test_raise_username(self):
        self.assertTrue(utils.raise_invalid_username('test'))
        with self.assertRaises(exceptions.UsernameError):
            utils.raise_invalid_username('test$')
        with self.assertRaises(exceptions.UsernameError):
            utils.raise_invalid_username('test1234567890123456789012345')


if __name__ == "__main__":
    unittest.main()
