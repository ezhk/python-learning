"""
Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. Для этого:
1. Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке ASCII (например, €);
2. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
3. Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""

import yaml

if __name__ == "__main__":
    init_dict = {
        "list": ["item", "quantity", {
            "first key": "Карл",
            "second key": "у Клары"
        }],
        "int": 1,
        "dict": {
            "tea": "чай",
            "coffee": "кофе",
            "euro": "€",
        }
    }

    # записываем исходный словарь
    with open('3.yaml', 'w', encoding='utf-8') as fh:
        yaml.dump(init_dict, fh, default_flow_style=True)

    # проверяем записанное
    with open('3.yaml', 'r', encoding='utf-8') as fh:
        read_data = yaml.load(fh, Loader=yaml.SafeLoader)
        print(f"Исходный словарь: {init_dict}\n\tи прочитанный {read_data}")

    with open('file.yaml', 'w', encoding='utf-8') as fh:
        yaml.dump(init_dict, fh, allow_unicode=True, default_flow_style=False)

    """
    Исходный словарь: {'list': ['item', 'quantity', {'first key': 'Карл', 'second key': 'у Клары'}], 'int': 1, 'dict': {'tea': 'чай', 'coffee': 'кофе', 'euro': '€'}}
        и прочитанный {'dict': {'coffee': 'кофе', 'euro': '€', 'tea': 'чай'}, 'int': 1, 'list': ['item', 'quantity', {'first key': 'Карл', 'second key': 'у Клары'}]}
    Записанный и прочитанный словари совпадают по содержимому (отличается лишь порядок ключей).

    Содержимое файла 3.yaml без allow_unicode и с default_flow_style=True:
    {dict: {coffee: "\u043A\u043E\u0444\u0435", euro: "\u20AC", tea: "\u0447\u0430\u0439"},
      int: 1, list: [item, quantity, {first key: "\u041A\u0430\u0440\u043B", second key: "\u0443\
            \ \u041A\u043B\u0430\u0440\u044B"}]}
    
    Содержимое file.yaml (allow_unicode=True, default_flow_style=False):
    dict:
      coffee: кофе
      euro: €
      tea: чай
    int: 1
    list:
    - item
    - quantity
    - first key: Карл
      second key: у Клары
    """
