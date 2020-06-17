from Gondwana.helper import *

def test_get_product_type_name():
    testcases = {
        '男装': [
            ' man\'s ',
            'man\'s ',
            ' men\'s ',
            'men\'s ',
        ],
        '女装': [
            ' woman\'s ',
            'woman\'s ',
            ' women\'s ',
            'women\'s ',
            ' lady\'s ',
            'lady\'s ',
            ' ladies\'s ',
            'ladies\'s ',
        ],
        '童装': [
            ' kid\'s ',
            'kid\'s ',
            ' kids\'s ',
            'kids\'s ',
            ' youth ',
            'youth ',
            ' preschool ',
            'preschool ',
            ' newborn ',
            'newborn ',
        ],
    }

    for k, v in testcases.items():
        for item in v:
            assert(k == get_product_type_name(item))

def test_generate_shipping_method():
    testcases = {
        'DHL': [
            '1234567890',
            '1',
        ],
        'USPS': [
            'L1234567890',
            'LA1234567890',
            'LA1234567890',
            'L1234567890A',
        ],
        'N/A': [
            'A123',
            'aaa',
            '332a',
        ]
    }

    for k, v in testcases.items():
        for item in v:
            assert (k == generate_shipping_method(item))
