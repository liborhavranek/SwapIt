def get_csrf_token_from_response(response):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf_token = soup.find('input', {'id': 'csrf_token'}).get('value')
    return csrf_token