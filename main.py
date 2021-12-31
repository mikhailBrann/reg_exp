import csv,re

if __name__ == "__main__":
    # невнимательно прочитал задание и взял реальный файл с сайта минфина по ссылке на гите
    # если можно, хотел бы его оставить
    with open('files/minfin.csv', newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)

    
    adress_book = []
    email_pattern = re.compile(r"\w+@\w+.\w+")
    phone_pattern = re.compile(r"((\+7|\(\d+\)){1,5}.(\d|\s|-){5,13}(доб\.[0-9]*)?)")
    initials_pattern = re.compile(r"(([ЁА-Я]{1})([а-я]+\s?)(\s?[ЁА-Я]{1}[а-я]+)(\s?[ЁА-Я]{1}[а-я]+))")
    position_pattern = re.compile(r"((\-|\.|\s|\,|\d|[а-яА-ЯёЁ])*(г\.){1}(\w|\d|\s|\,)+)")
    organization_pattern = re.compile(r"((\w|\s|\d)+учреждение(\w|\s|\d|\»|\«|\-)+)")


    for contact in data:
        result_info = {}
        initials_list = initials_pattern.findall(str(contact))
        organization = organization_pattern.findall(str(contact))
        position = position_pattern.findall(str(contact))
        phone = phone_pattern.findall(str(contact))
        email = email_pattern.findall(str(contact))

        if initials_list:
            initials_split = re.split("(([а-яА-ЯёЁ])+ ([а-яА-ЯёЁ])+ ([а-яА-ЯёЁ])+)", initials_list[0][0])
            initials_split = initials_split[1].split(" ")

            if initials_split[0]: result_info['lastname'] = initials_split[0]
            if initials_split[1]: result_info['firstname'] = initials_split[1]
            if initials_split[2]: result_info['surname'] = initials_split[2]

        if organization:
            if organization[0][0]: result_info['organization'] = organization[0][0]

        if position:
            if position[0][0]: result_info['position'] = position[0][0]

        if phone:
            result_info['phone'] = []

            for phone_item in phone:
                phone_value = re.sub(r"((\+7|\+8|8)?\((\d{3,5})?\)\s?(\d{3,5})\-(\d{2})(\d{1,3})\s?(доб\.(\d+))?)", r"+7(\3)\4-\5-\6 \7", phone_item[0]).strip()
                if phone_value not in result_info['phone']: result_info['phone'].append(phone_value)
        
        if email:
            result_info['email'] = []

            for email_item in email:
                if email_item not in result_info['email']: result_info['email'].append(email_item)
        
        # проверка для отмены записи пустого словаря в результирующий список 
        if bool(result_info) != False: adress_book.append(result_info)
    
    
    with open('files/contact_book.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames = adress_book[0])
        writer.writeheader()
        writer.writerows(adress_book)
