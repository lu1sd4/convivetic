from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

from django.conf import settings

import requests

class TokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (
			six.text_type(user.pk) + six.text_type(timestamp) +
			six.text_type(user.is_active)
		)
account_activation_token = TokenGenerator()

class YoutubeTokenGenerator():

	token_validation_api_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
	token_refresh_url = 'https://www.googleapis.com/oauth2/v4/token'

	def get_youtube_token(self):
		token = settings.ACCESS_TOKEN
		get_params = { 'access_token' : token }
		validation = requests.get(self.token_validation_api_url, params = get_params)
		if('error_description' in validation.json()):
			print('invalid token')
			refresh_token = settings.REFRESH_TOKEN
			client_id = settings.CLIENT_ID
			client_secret = settings.CLIENT_SECRET
			grant_type = 'refresh_token'
			post_data = {
				'refresh_token' : refresh_token,
				'client_id' : client_id,
				'client_secret' : client_secret,
				'grant_type' : grant_type
			}
			refresh = requests.post(self.token_refresh_url, post_data)
			print(refresh.content)
			token = refresh.json()['access_token']
			settings.ACCESS_TOKEN = token
		else:
			print('valid token')
		return token

youtube_token = YoutubeTokenGenerator()