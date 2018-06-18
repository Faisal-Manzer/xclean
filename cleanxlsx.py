import sys
import pyexcel as pe
import threading
import data_cleaner as dc
import os
import time

cols = None
filename = None
output = 0
header = {
    'Name': 'Name',
    'Email': 'Email',
    'Number': 'Number',
    'Address': 'Address',
    'To_Join': False
}
num_email_ver = 0
num_email_bounced = 0
num_email_error = 0


def array_init(total_input):
    global name_cols
    global email_cols
    global number_cols, number_code
    global address_cols, city_cols, country_cols

    name_cols = [['Name']] + [None] * total_input

    email_cols = [['Emails']] + [None] * total_input

    number_cols = [['Numbers']] + [None] * total_input
    number_code = [['Country Code']] + [None] * total_input

    address_cols = [['Address']] + [None] * total_input
    city_cols = [['City']] + [None] * total_input
    country_cols = [['Country']] + [None] * total_input


def clean_sheet(start, end):
    global cols, output, num_email_ver, num_email_bounced, num_email_error
    global name_cols
    global email_cols
    global number_cols, number_code
    global address_cols, city_cols, country_cols

    for index in range(start, end):
        if name_cols[index+1] is None:
            output += 1

            name_cols[index+1] = [dc.sanitize_name(cols[header['Name']][index])]

            if not header['Email'] == '':
                email_details = dc.sanitize_emails(cols[header['Email']][index])
                num_email_ver += email_details['verified']
                num_email_bounced += email_details['bounce']
                num_email_error += email_details['error_found']
                if not header['To_Join']:
                    email_cols[index+1] = email_details['emails']
                elif header['To_Join']:
                    email_cols[index+1] = [','.join(email_details['emails'])]

            if not header['Number'] == '':
                numbers_details = dc.sanitize_number(cols[header['Number']][index])
                if not header['To_Join']:
                    number_code[index+1] = numbers_details['code']
                    number_cols[index+1] = numbers_details['numbers']
                else:
                    code_str = ''
                    num_str = ''
                    for number_code_str in numbers_details['code']:
                        code_str += str(number_code_str) + ','
                    for number_str in numbers_details['numbers']:
                        num_str += str(number_str) + ','
                    code_str = code_str[0:-1]
                    num_str = num_str[0:-1]

                    if len(numbers_details['code']) == 1:
                        code_str = int(code_str)
                        num_str = int(num_str)

                    number_code[index+1] = [code_str]
                    number_cols[index + 1] = [num_str]

            if not header['Address'] == '':
                address_details = dc.sanitize_address(cols[header['Address']][index])
                address_cols[index+1] = [address_details['address']]
                city_cols[index+1] = [address_details['city']]
                country_cols[index+1] = [address_details['country']]


def start_thread(start, end, factor):

    index_length = int((end - start) / factor + 1)
    thread_array = []
    for index in range(index_length):
        index_start = index * factor
        index_end = (index + 1) * factor

        if end < index_end:
            index_end = end

        new_factor = int(factor / 10)

        if new_factor > 1:
            thread_array += [threading.Thread(target=start_thread, args=(index_start, index_end, new_factor))]
        else:
            thread_array += [threading.Thread(target=clean_sheet, args=(index_start, index_end))]

        thread_array[index].start()

    for index in range(len(thread_array)):
        thread_array[index].join()


def start_cleaning(file_name=None, header_g=None):

    global cols, filename, header
    global name_cols
    global email_cols
    global number_cols, number_code
    global address_cols, city_cols, country_cols

    if file_name is not None:
        filename = file_name

    if header_g is not None:
        header = header_g

    try:
        print("Starting Cleaning Process...")
        print(filename)

        sheet = pe.get_sheet(file_name=filename, name_columns_by_row=0)
        cols = sheet.column

        total_input = len(cols[header['Name']])
        print('Total input:', total_input)
        
        array_init(total_input)
        start_thread(0, total_input, 1000)

        print('Output:', output)

        new_sheet = pe.Sheet(name_cols)

        if header['Email'] != '':
            new_sheet.column += pe.Sheet(email_cols)

        if header['Number'] != '':
            new_sheet.column += pe.Sheet(number_cols)
            new_sheet.column += pe.Sheet(number_code)

        if header['Address'] != '':
            new_sheet.column += pe.Sheet(address_cols)
            new_sheet.column += pe.Sheet(city_cols)
            new_sheet.column += pe.Sheet(country_cols)

        main_save_path = os.path.dirname(filename) + '/cleaned_' + os.path.basename(filename)
        print('Saved At: ', main_save_path)
        sheet.save_as(main_save_path)

        return {
            'status': True,
            'saved_file': main_save_path,
            'email_verified': num_email_ver,
            'email_bounced': num_email_bounced,
            'email_error': num_email_error
        }

    except Exception as error:
        print(error)
        return {'status': False, 'error': error}


if __name__ == '__main__':
    start_time = time.time()
    filename = sys.argv[1]
    start_cleaning()
    print('Time Taken', time.time() - start_time)
