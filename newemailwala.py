import pyexcel as pe
from validate_email import validate_email
import re
import threading
import time
import os


def verify_all_emails(filepath, email_col_name, name_col_name):
    def get_verified_email(start, end):
        nonlocal email_re
        nonlocal major_col
        nonlocal new_col
        nonlocal err_no
        nonlocal bounce_no
        try:
            for ii in range(start, end):
                emails_tov = major_col[email_col_name][ii]
                name_tov = major_col[name_col_name][ii]
                email_arr = re.findall(email_re, emails_tov)

                for j in range(0, len(email_arr)):
                    try:
                        if validate_email(email_arr[j], verify=True):
                            new_col += [[name_tov, email_arr[j]]]
                        else:
                            bounce_no += 1
                    except Exception as err:
                        err_no += 1
                        print(err)
        except Exception as err:
            print(err)

    email_re = re.compile("([a-zA-Z._0-9]+@[a-zA-Z._0-9]+\.[a-zA-Z.0-9]+)")
    err_no = 0
    bounce_no = 0
    new_col = [[name_col_name, 'Verified Email']]

    try:
        print('Start point')
        sheet = pe.get_sheet(file_name=filepath, name_columns_by_row=0)
        major_col = sheet.column
        print("Total input", len(major_col[name_col_name]))

        start_time = time.time()
        t = []

        for i in range(0, 999):
            t += [threading.Thread(target=get_verified_email, args=(i * 10 + 1, (i + 1) * 10))]
            t[i].start()

        for i in range(0, 999):
            t[i].join()
        end_time = time.time()

        print(end_time - start_time)
        new_sheet = pe.Sheet(new_col)
        new_sheet.save_as(os.path.dirname(filepath) + '/verified_email_' + os.path.basename(filepath))

        print('Total Email Found', len(new_col))
        print('Total Error', err_no)
        print('Total bounce', bounce_no)

        return {
            'status': True,
            'bounced': str(bounce_no),
            'error': str(err_no),
            'found': str(len(new_col))
        }
    except Exception as err:
        print(err)
        return {
            'status': False,
            'error': err
        }
