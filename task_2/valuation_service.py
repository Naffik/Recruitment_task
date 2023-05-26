import csv


def load_data(filename: str) -> list:
    data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            data.append(line)

    return data


def load_currencies(filename: str) -> dict:
    currencies = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            currency = line['currency']
            ratio = float(line['ratio'])
            currencies[currency] = ratio
    # print(currencies)
    return currencies


def load_matchings(filename: str) -> dict:
    matchings = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            matching_id = line['matching_id']
            top_priced_count = line['top_priced_count']
            matchings[matching_id] = top_priced_count
    # print(matchings)
    return matchings


def save_results(filename: str, top_products: dict) -> None:
    fieldnames = ['matching_id', 'total_price', 'avg_price', 'currency', 'ignored_products_count']
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(top_products)


def convert_to_pln(price: float, ratio: float) -> float:
    return price * ratio


def calculate_total_price(price: float, quantity: int) -> float:
    return price * quantity


def get_top_products(data: list, currencies: dict, matchings: dict) -> list:

    top_products = []

    for matching_id, top_products_count in matchings.items():
        matching_data = [product for product in data if int(product['matching_id']) == int(matching_id)]
        matching_data.sort(key=lambda product: calculate_total_price(float(product['price']),
                                                                     int(product['quantity'])), reverse=True)
        ignored_products_count = len(matching_data) - int(top_products_count)
        matching_data = matching_data[:int(top_products_count)]

        for product in matching_data:
            price = float(product['price'])
            quantity = int(product['quantity'])
            currency = product['currency']
            ratio = currencies.get(currency)
            pln_price = convert_to_pln(price, ratio)
            total_price = calculate_total_price(pln_price, quantity)
            avg_price = total_price / quantity
            top_products.append({'matching_id': product['matching_id'],
                                 'total_price': total_price,
                                 'avg_price': avg_price,
                                 'currency': product['currency'],
                                 'ignored_products_count': ignored_products_count})
    # print(top_products)

    return top_products


if __name__ == '__main__':
    data = load_data('data.csv')
    currencies = load_currencies('currencies.csv')
    matchings = load_matchings('matchings.csv')
    top_products = get_top_products(data, currencies, matchings)
    save_results('top_products.csv', top_products)
