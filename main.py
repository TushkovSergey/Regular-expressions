from pprint import pprint
import re
import csv

def open_csv():
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",", )
        contacts_list = list(rows)
    return contacts_list

def write_csv():
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(phonebook)

def correct_phonebook(contacts_list):
    phonebook = []
    for string in contacts_list:
        name_combination_1 = re.findall('\w+', string[0])
        name_combination_2 = re.findall('\w+', string[1])
        if len(name_combination_1) == 3:
            corrected_name = [name_combination_1[0], name_combination_1[1], name_combination_1[2]]
        elif len(name_combination_1) == 2:
            corrected_name = [name_combination_1[0], name_combination_1[1], string[2]]
        elif len(name_combination_1) == 1 and len(name_combination_2) == 1:
            corrected_name = [name_combination_1[0], string[1], string[2]]
        elif len(name_combination_1) == 1 and len(name_combination_2) == 2:
            corrected_name = [name_combination_1[0], name_combination_2[0], name_combination_2[1]]
        pos_number = 3
        while pos_number != len(string):
            corrected_name.append(string[pos_number])
            pos_number = pos_number + 1
        match = 0
        for number, phonebook_string in enumerate(phonebook):
            if phonebook_string[0] == corrected_name[0] and phonebook_string[1] == corrected_name[1]:
                match = number
                break

        if match == 0:
            phonebook.append(corrected_name)
        else:
            common_corrected_name = []
            for position_number, position in enumerate(phonebook[match]):
                if position == '':
                    common_corrected_name.append(corrected_name[position_number])
                else:
                    common_corrected_name.append(phonebook[match][position_number])
            phonebook[match] = common_corrected_name
    return phonebook

def correct_phone(phonebook):
    for string_number, string in enumerate(phonebook):
        if string[-2] == 'phone':
            pass
        elif 'доб.' in string[-2]:
            corrected_phone = re.sub(r'(\+7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\-*(\d{2})\-*(\d{2})\s*\(*\D*\s*(\d*)\)*', r'+7(\2)\3-\4-\5 доб.\6', string[-2])
            phonebook[string_number][-2] = corrected_phone
        else:
            corrected_phone = re.sub(r'(\+7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\-*(\d{2})\-*(\d{2})', r'+7(\2)\3-\4-\5', string[-2])
            phonebook[string_number][-2] = corrected_phone
    pprint(phonebook)
    return phonebook

contacts_list = open_csv()
phonebook = correct_phonebook(contacts_list)
phonebook = correct_phone(phonebook)
write_csv()
