"""
Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
1. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров «Изготовитель системы»,  «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
2. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
3. Проверить работу программы через вызов функции write_to_csv().
"""

import csv
import re

from chardet.universaldetector import UniversalDetector


def detect_file_encoding(filename):
    """
    Опрелеляем кодировку файла, cp-1251 на маке подкладывает
    злую шутку и если анализировать построчно, можно получить
    MacCyrillic, windows-1251, ISO-8859-9. Поэтому на старте
    анализируем весь файл.
    :param filename: string
    :return detector object: dict, like a
    {
        'encoding': 'windows-1251',
        'confidence': 0.9237003416621283,
        'language': 'Russian'
    }
    """

    detector = UniversalDetector()
    with open(filename, 'rb') as fh:
        for line in fh:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result


def get_data(filenames=('info_1.txt', 'info_2.txt', 'info_3.txt')):
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    main_data = [["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]]

    for fn in filenames:
        file_encoding = detect_file_encoding(fn).get('encoding', 'utf-8')

        inner_prodict_description = {}
        with open(fn, 'r', encoding=file_encoding) as fh:
            for line in fh:

                try:
                    key, value = re.split(':', line, 1)
                except Exception:
                    # пропускаем строки, где нет ":" в качестве разделителя
                    continue

                # Пропускаем те ключи, которые нам не нужны
                if not re.match(r"^(Изготовитель системы|Название ОС|Код продукта|Тип системы)$", key.strip()):
                    continue

                inner_prodict_description.update({key.strip(): value.strip()})
        os_prod_list.append(inner_prodict_description.get("Изготовитель системы", ""))
        os_name_list.append(inner_prodict_description.get("Название ОС", ""))
        os_code_list.append(inner_prodict_description.get("Код продукта", ""))
        os_type_list.append(inner_prodict_description.get("Тип системы", ""))

        main_data.append([os_prod_list[-1], os_name_list[-1], os_code_list[-1], os_type_list[-1]])
    return main_data, os_prod_list, os_name_list, os_code_list, os_type_list


def write_to_csv(filename):
    main_data, _, _, _, _ = get_data()
    print(f"Подготовленные для CSV данные: {main_data}")
    with open(filename, 'w', encoding='utf-8') as fh:
        writer = csv.writer(fh, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(main_data)
    with open(filename, 'r', encoding='utf-8') as fh:
        reader = csv.DictReader(fh, delimiter=';')
        return [line_dict for line_dict in reader]


if __name__ == "__main__":
    print(f"Содержимое файла в виде OrderedDict: {write_to_csv('1.csv')}")

    """
    Подготовленные для CSV данные: [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы'], ['LENOVO', 'Microsoft Windows 7 Профессиональная', '00971-OEM-1982661-00231', 'x64-based PC'], ['ACER', 'Microsoft Windows 10 Professional', '00971-OEM-1982661-00231', 'x64-based PC'], ['DELL', 'Microsoft Windows 8.1 Professional', '00971-OEM-1982661-00231', 'x86-based PC']]
    Содержимое файла в виде OrderedDict: [OrderedDict([('Изготовитель системы', 'LENOVO'), ('Название ОС', 'Microsoft Windows 7 Профессиональная'), ('Код продукта', '00971-OEM-1982661-00231'), ('Тип системы', 'x64-based PC')]), OrderedDict([('Изготовитель системы', 'ACER'), ('Название ОС', 'Microsoft Windows 10 Professional'), ('Код продукта', '00971-OEM-1982661-00231'), ('Тип системы', 'x64-based PC')]), OrderedDict([('Изготовитель системы', 'DELL'), ('Название ОС', 'Microsoft Windows 8.1 Professional'), ('Код продукта', '00971-OEM-1982661-00231'), ('Тип системы', 'x86-based PC')])]
    
    Содержимое 1.csv (в качестве разделителя указан ";"):
    "Изготовитель системы";"Название ОС";"Код продукта";"Тип системы"
    "LENOVO";"Microsoft Windows 7 Профессиональная";"00971-OEM-1982661-00231";"x64-based PC"
    "ACER";"Microsoft Windows 10 Professional";"00971-OEM-1982661-00231";"x64-based PC"
    "DELL";"Microsoft Windows 8.1 Professional";"00971-OEM-1982661-00231";"x86-based PC"
    """
