import requests


def check_headers(scope):
    value = ''
    head_not_founded = []
    count_headers = 0
    domain, port = scope.split(',')
    checked_headers = ['Content-Security-Policy', 'X-Content-Type-Options',
                       'X-Frame-Options', 'Strict-Transport-Security']
    Bad_headers = ['Server', 'X-Powered-By']
    count = 0
    if port == '80':
        url = f'http://{domain}/'
    elif port == '443':
        url = f'https://{domain}/'
    else:
        url = f'https://{domain}:{port}/'
    print(f"URL: {url}")
    request = requests.get(url, verify=False)
    headers = request.headers
    for header in Bad_headers:
        for header_r in headers:
            if header_r == header and headers[header_r] != '':
                if count_headers == 0:
                    print("Bad Headers:")
                    count_headers = 1
                value_header = headers[header_r]
                print(f'{header} : {value_header}')
                break
    print()
    for header in checked_headers:
        try:
            value = str(headers[f'{header}'])
            if value != '' or count == 0:
                if count == 0:
                    count = 1
                    print("Headers needs to check:")
                    print(f"{header}: {value}")
                else:
                    print(f"{header}: {value}")
        except:
            head_not_founded.append(f'{header}')
    print()
    print("Missing headers:")
    for header in head_not_founded:
        print(f'{header}')
    print()
