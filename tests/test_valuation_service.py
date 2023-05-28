import pytest
from task_2.valuation_service import *


@pytest.fixture(scope='module')
def currencies_file(tmpdir_factory):
    currencies_data = [
        {'currency': 'GBP', 'ratio': '2.4'},
        {'currency': 'EU', 'ratio': '2.1'},
        {'currency': 'PLN', 'ratio': '1'}
    ]
    file_path = tmpdir_factory.mktemp('data').join('currencies.csv')

    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['currency', 'ratio'])
        writer.writeheader()
        writer.writerows(currencies_data)

    return str(file_path)


@pytest.fixture(scope='module')
def data_file(tmpdir_factory):
    data = [
        {'id': '1', 'price': '1000', 'currency': 'GBP', 'quantity': '2', 'matching_id': '3'},
        {'id': '2', 'price': '1050', 'currency': 'EU', 'quantity': '1', 'matching_id': '1'},
    ]
    file_path = tmpdir_factory.mktemp('data').join('data.csv')

    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'price', 'currency', 'quantity', 'matching_id'])
        writer.writeheader()
        writer.writerows(data)

    return str(file_path)


@pytest.fixture(scope='module')
def matchings_file(tmpdir_factory):
    matchings_data = [
        {'matching_id': '1', 'top_priced_count': '1'},
        {'matching_id': '2', 'top_priced_count': '2'},
        {'matching_id': '3', 'top_priced_count': '1'}
    ]
    file_path = tmpdir_factory.mktemp('data').join('matchings.csv')

    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['matching_id', 'top_priced_count'])
        writer.writeheader()
        writer.writerows(matchings_data)

    return str(file_path)


def test_calculate_total_price():
    assert calculate_total_price(10, 5) == 50
    assert calculate_total_price(0, 0) == 0
    assert calculate_total_price(15, 3) == 45


def test_convert_to_pln():
    currencies = {'GBP': 2.4, 'EU': 2.1, 'PLN': 1}
    assert convert_to_pln(100, 2.4) == 240
    assert convert_to_pln(50, 2.1) == 105
    assert convert_to_pln(200, 1) == 200


def test_load_currencies(currencies_file):
    currencies = load_currencies(currencies_file)
    assert currencies['GBP'] == 2.4
    assert currencies['EU'] == 2.1
    assert currencies['PLN'] == 1


def test_load_data(data_file):
    data = load_data(data_file)
    assert len(data) == 2
    assert data[0]['price'] == '1000'
    assert data[1]['currency'] == 'EU'


def test_load_matchings(matchings_file):
    matchings = load_matchings(matchings_file)
    assert len(matchings) == 3
    assert matchings['1'] == '1'
    assert matchings['3'] == '1'


def test_get_top_products(currencies_file, data_file, matchings_file):
    currencies = load_currencies(currencies_file)
    matchings = load_matchings(matchings_file)
    data = load_data(data_file)

    expected_results = [
        {'matching_id': '1', 'total_price': 1050.0, 'avg_price': 1050.0, 'currency': 'EU', 'ignored_products_count': 0},
        {'matching_id': '3', 'total_price': 2000.0, 'avg_price': 1000.0, 'currency': 'GBP', 'ignored_products_count': 0}
    ]

    top_products = get_top_products(data, currencies, matchings)

    assert len(top_products) == 2
    assert top_products[0] == expected_results[0]
    assert top_products[1] == expected_results[1]
