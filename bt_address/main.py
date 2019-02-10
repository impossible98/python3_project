import json
from urllib import request
from datetime import datetime


def main():
    addresses = []
    with open('origin.txt') as f:
        for i in f.readlines():
            addresses.append(i.strip('\n'))

    addresses2 = list(set(addresses))
    global addresses3
    addresses3 = []
    for i in addresses2:
        url = get_html(i)[0]
        code = get_html(i)[1]
        if code == 200:
            print('%s is available.' % i)
            addresses3.append(url)
        else:
            print('%s is unavailable.' % i)

    addresses3.sort()
    write_into_file(addresses3)


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    }

    req = request.Request(url, headers=headers)
    try:
        # timeout=3
        response = request.urlopen(req, timeout=3)
        return (url, response.code)
    except Exception:
        return (url, 400)


def write_into_file(addresses):
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    hour = datetime.now().hour
    addresses_list = {
        'year': year,
        'month': month,
        'day': day,
        'hour': hour,
        'count': len(addresses3),
        'addresses': addresses,
    }

    result = json.dumps(addresses_list, indent=4)
    with open('bt_address.json', 'w') as f:
        f.write(result)


if __name__ == '__main__':
    main()
