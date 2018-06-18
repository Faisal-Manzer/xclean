import re
import phonenumbers
from geo import GeoText
from validate_email import validate_email


def sanitize_name(name):
    if name is not None:
        name = str(name).title()
    else:
        name = ''
    return name


def sanitize_number(number_list):
    number_splitter = re.compile("[0-9+\- ]+")
    plus_finder = re.compile("^\+.+")

    splitted_numbers = re.findall(number_splitter, str(number_list))

    verified_number = []
    verified_country_code = []

    for number in splitted_numbers:
        try:
            is_plus = plus_finder.match(number)
            if is_plus:
                number_details = phonenumbers.parse(number, None)
            else:
                number_details = phonenumbers.parse(number, 'IN')

            if (not is_plus and len(number) == 10) or is_plus:
                verified_number += [number_details.national_number]
                verified_country_code += [number_details.country_code]
        except Exception as error:
            print('Number:', number, 'Error:', error, 'List:', number_list)

    return {'numbers': verified_number, 'code': verified_country_code}


def sanitize_address(address):
    address = str(address).title()
    city = ''
    country = ''

    try:

        geo_address = GeoText(address)

        cities = geo_address.cities
        countries = geo_address.countries

        if len(cities) > 0:
            city = cities[len(cities) - 1]

        if len(countries) > 0:
            country = countries[len(countries) - 1]
    except Exception as error:
        print('Address', address, 'Error', error)

    return {'address': address, 'city': city, 'country': country}


def sanitize_emails(email_list):
    is_email = re.compile("[a-zA-Z\-._0-9]+@[a-zA-Z\-._0-9]+\.[a-zA-Z\-._0-9]+")

    error_found = 0
    bounce = 0
    verified = 0

    verified_emails = []

    emails = re.findall(is_email, email_list)

    for email in emails:
        try:
            if validate_email(email, verify=True):
                verified_emails += [email]
                verified += 1
            else:
                bounce += 1
        except Exception as error:
            error_found += 1
            print('Email', email, 'Error', error)

    return {'emails': verified_emails, 'error_found': error_found, 'bounce': bounce, 'verified': verified}
