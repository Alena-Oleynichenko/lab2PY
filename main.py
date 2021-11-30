import re
import json
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-input', type = str, help='Get path file input', dest='input')
parser.add_argument('-output', type = str, help='Get path file output', dest='output')
args = parser.parse_args()

class Validator:
    def __init__(self):
        pass


    def control_telephone(telephone)->bool:
        if re.match(r"(?:\+7|8)-\(\d{3}\)(-\d{3})(-\d{2}){2}", telephone) is not None:
            return True
        return False

    def control_weight(weight)->bool:
        pattern = '\d{2,3}'
        if re.match(pattern, str(weight)) is not None:
            if (int(weight)<150 and int(weight)>40):
                return True
        return False

    def control_snils(snils: str) -> bool:
        if len(snils) == 11:
            return True
        return False

    def control_passport_num(passport_number: int) -> bool:
        if len(str(passport_number)) == 6:
            return True
        return False

    def control_address(address) -> bool:
        if type(address) != str:
            return False
        if re.match(r"^(ул\.)?(Аллея)?\s[\w\.\s-]+\d+$", address) is not None:
            return True
        return False

    def control_work_experience(work_number) -> bool:
        if type(work_number) == int:
            if(work_number<80 and work_number>0):
                return True
        return False

    def control_political_views(political_view: str) -> bool:
        valid_political_views = 'Индифферентные, Социалистические, Умеренные, Либеральные, Консервативные, Коммунистические, Анархистские, Либертарианские'
        if type(political_view) != str:
            return False
        if political_view not in valid_political_views:
            return False
        return True

    def control_worldview(worldview: str) -> bool:
        valid_worldview = 'Секулярный гуманизм, Иудаизм, Деизм, Конфуцианство, Католицизм, Пантеизм, Агностицизм, Атеизм, Буддизм'
        if type(worldview) != str:
            return False
        if worldview not in valid_worldview:
            return False
        return True

    def control_university(university) -> bool:
        invalid_university = 'Дурмстранг, Шамбартон, Хогвартс, Кирин-Тор, Аретуза, Бан Ард, Каражан, Гвейсон Хайль'
        if type(university) != str:
            return False
        if university not in invalid_university:
            return True
        return False

data = json.load(open(args.input, encoding='windows-1251'))

true_data = list()
telephone = 0
weight = 0
snils = 0
passport_num = 0
university = 0
work_experience = 0
worldview = 0
address = 0
political_views = 0
with tqdm(total=len(data)) as progressbar:
    for person in data:
        temp = True
        if not Validator.control_telephone(person['telephone']):
            telephone += 1
            temp = False
        if not Validator.control_weight(person['weight']):
            weight += 1
            temp = False
        if not Validator.control_snils(person['snils']):
            snils += 1
            temp = False
        if not Validator.control_work_experience(person['work_experience']):
            work_experience += 1
            temp = False
        if not Validator.control_worldview(person['worldview']):
            worldview += 1
            temp = False
        if not Validator.control_passport_num(person['passport_number']):
            passport_num += 1
            temp = False
        if not Validator.control_university(person['university']):
            university += 1
            temp = False
        if not Validator.control_address(person["address"]):
            address += 1
            temp = False
        if not Validator.control_political_views(person['political_views']):
            political_views += 1
            temp = False
        if temp:
            true_data.append(person)
        progressbar.update(1)

out = open(args.output, 'w', encoding='utf-8')
new_data = json.dumps(true_data, ensure_ascii=False, indent=4)
out.write(new_data)
out.close()

print(f'Число валидных записей: {len(true_data)}')
print(f'Число невалидных записей: {len(data) - len(true_data)}')
print(f'Число невалидных телефонных номеров: {telephone}')
print(f'Число невалидных маcc: {weight}')
print(f'Число невалидных снилсов: {snils}')
print(f'Число невалидных паспортных номеров: {passport_num}')
print(f'Число невалидных университетов: {university}')
print(f'Число невалидных рабочих стажей: {work_experience}')
print(f'Число невалидных политических взглядов:{political_views}')
print(f'Число невалидных мировоззрений: {worldview}')
print(f'Число невалидных адрессов: {address}')
#
# python.exe main.py -input C:\\labs_py\\106.txt -output C:\\labs_py\\output.txt