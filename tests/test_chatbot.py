import json
from mock import patch
from unittest import TestCase

import botresponse as botRes
import botinput as botInp
import config
import facebookbot


class test_chat_bot(TestCase):
    @classmethod
    def setUp(cls):
        cls.access_token = getattr(config, 'FACEBOOK_PAGE_ACCESS_TOKEN', 'fake-access-token')
        cls.url = getattr(config, 'FACEBOOK_BASE_URL', 'https://fake.domain.tld/v1/')

    @patch('requests.post')
    def test_send_message(self, mock_post):
        ''' 
        Ensure send_message called with correct parameters
        '''
        test_message = 'This is a test message'
        fake_user = 'fake-user'
        facebookbot.send_message(fake_user, test_message)
        self.assertTrue(mock_post.called, 'Error, mock class was not called')

        expected_headers = {
            'Content-Type': 'application/json'
        }

        expected_params = {
            'access_token': self.access_token
        }

        expected_data = {
            'message': {
                'text': test_message
            },
            'recipient': {
                'id': fake_user
            }
        }

        url, data = mock_post.call_args
        self.assertEqual(url[0], '{}{}'.format(self.url, '/me/messages'))
        self.assertDictEqual(data['headers'], expected_headers)
        self.assertDictEqual(data['params'], expected_params)
        self.assertEqual(data['data'], json.dumps(expected_data))

    @patch('requests.post')
    def test_send_message_response(self, mock_post):
        ''' 
        Ensure send_message_response calls send_message with correct parameters
        '''
        test_message = 'This is a test message'
        fake_user = 'fake-user'
        facebookbot.send_message_response(fake_user, test_message)
        self.assertTrue(mock_post.called, 'Error, mock class was not called')

        expected_headers = {
            'Content-Type': 'application/json'
        }

        expected_params = {
            'access_token': self.access_token
        }

        expected_data = {
            'message': {
                'text': test_message
            },
            'recipient': {
                'id': fake_user
            }
        }

        url, data = mock_post.call_args
        self.assertEqual(url[0], '{}{}'.format(self.url, '/me/messages'))
        self.assertDictEqual(data['headers'], expected_headers)
        self.assertDictEqual(data['params'], expected_params)
        self.assertEqual(data['data'], json.dumps(expected_data))

    def test_get_one_of_method(self):
        '''
        Test getOneOf method
        '''
        # One item
        self.assertEqual(facebookbot.getOneOf([0]), 0)

        # Assert returns an item in multiple items
        test_list = [0, 1, 2]
        self.assertIn(facebookbot.getOneOf(test_list), test_list)

        # Assert multiple calls return correctly
        for x in xrange(0, 50):
            self.assertIn(facebookbot.getOneOf(test_list), test_list, 'Error, failure on multiple calls to getOneOf')

        # Same as above, with different list
        test_list = ['Larry', 'Moe', 'Curly']
        for x in xrange(0, 50):
            self.assertIn(facebookbot.getOneOf(test_list), test_list, 'Error, failure on multiple calls to getOneOf')

        # Assert empty list raises error
        test_list = []
        self.assertRaises(ValueError, facebookbot.getOneOf, test_list)

    def test_user_response_greetings(self):
        '''
        Ensure all user input in greetings returns valid bot response for greetings
        '''

        greetings = getattr(botInp, 'GREETING', [])
        botresponse = getattr(botRes, 'GREETING', [])
        self.assertNotEqual(greetings, [])
        self.assertNotEqual(botresponse, [])
        for greeting in greetings:
            self.assertIn(facebookbot.parse_user_message(greeting), botresponse)

    def test_user_response_bad_words(self):
        '''
        Ensure all user input in bad words returns valid bot response for bad words
        '''

        bad_words = getattr(botInp, 'BAD_WORDS', [])
        botresponse = getattr(botRes, 'BAD_WORDS_RESPONSES', [])
        self.assertNotEqual(bad_words, [])
        self.assertNotEqual(botresponse, [])
        for bad_word in bad_words:
            self.assertIn(facebookbot.parse_user_message(bad_word), botresponse)
