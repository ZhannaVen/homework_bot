set_for_response = {
    'url': 'ENDPOINT',
    'headers':'HEADERS',
    'params':{'from_date': 'current_timestamp'}
}
print('Запрос к API следующими параметрами: {url}, {headers}, {params}.'.format(**set_for_response))