import os
import configparser
import requests
from requests.exceptions import HTTPError

def send_email(html):
    # Given HTML template, sends Stock Listing Digest email using MailGun's API
    # Adapted from http://matthiaseisen.com/pp/patterns/p0198/

    # Args:
    #  * html - HTML to send via email

    # Returns:
    #  * none

    ## api params (using configparser)
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'settings.cfg'))
    key = config.get('MailGun', 'api')
    domain = config.get('MailGun', 'domain')
    
    ## requests params
    request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(domain)
    payload = {
        'from': 'tingi.dev@gmail.com',
        'to': 'tingi.dev@gmail.com',
        'subject': 'Stock Listing Digest',
        'html': html,
    }

    try:
        r = requests.post(request_url, auth=('api', key), data=payload)
        r.raise_for_status()
        print('Succes!')
    except HTTPError as e:
        print('Error {}'.format(e.response.status_code))
