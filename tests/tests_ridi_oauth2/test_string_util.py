import string as string_lib
import unittest

from ridi_oauth2.common.utils.string import DEFAULT_LENGTH, UNICODE_ASCII_CHARACTER_SET, generate_random_str


class StateTestCase(unittest.TestCase):
    def test_generate_state(self):
        state = generate_random_str()
        another_state = generate_random_str()

        self.assertEqual(len(state), DEFAULT_LENGTH)
        self.assertEqual(len(another_state), DEFAULT_LENGTH)

        self.assertNotEqual(state, another_state)

        for char in state:
            self.assertTrue(char in UNICODE_ASCII_CHARACTER_SET)

        custom_state = generate_random_str(chars=string_lib.punctuation)
        for char in custom_state:
            self.assertTrue(char in string_lib.punctuation)
            self.assertFalse(char in UNICODE_ASCII_CHARACTER_SET)
