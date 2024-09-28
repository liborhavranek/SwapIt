from bs4 import BeautifulSoup


def get_csrf_token_from_response(response):
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf_token = soup.find('input', {'id': 'csrf_token'}).get('value')
    return csrf_token
