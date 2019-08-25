"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для этого:
1. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
2. Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""

import json


def write_order_to_json(item, quantity, price, buyer, date):
    construct_order = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date,
    }

    init_data = {'orders': []}
    with open('orders.json', 'r', encoding='utf-8') as fh:
        init_data = json.load(fh)

    init_data['orders'].append(construct_order)
    with open('orders.json', 'w', encoding='utf-8') as fh:
        json.dump(init_data, fh, indent=4)

    return True


if __name__ == "__main__":
    write_order_to_json("Electric Scooter", 1, 30000, "Gena", "2019-06-01")
    write_order_to_json("Sony Camera", 2, 15000, "Cheburashka", "2019-08-25")

    with open('orders.json', 'r', encoding='utf-8') as fh:
        print(f"Текущее содержимое файла orders: {json.load(fh)}")

    """
    Текущее содержимое файла orders: {'orders': [{'item': 'Electric Scooter', 'quantity': 1, 'price': 30000, 'buyer': 'Gena', 'date': '2019-06-01'}, {'item': 'Sony Camera', 'quantity': 2, 'price': 15000, 'buyer': 'Cheburashka', 'date': '2019-08-25'}]}
    
    Содержимое orders.json на диске:
    {
        "orders": [
            {
                "item": "Electric Scooter",
                "quantity": 1,
                "price": 30000,
                "buyer": "Gena",
                "date": "2019-06-01"
            },
            {
                "item": "Sony Camera",
                "quantity": 2,
                "price": 15000,
                "buyer": "Cheburashka",
                "date": "2019-08-25"
            }
        ]
    }
    """
