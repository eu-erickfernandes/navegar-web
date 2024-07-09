def date_format(date_str):
    reversed_str = date_str.split('/')[::-1]
    formated_str = '-'.join(reversed_str)

    return formated_str