import csv
import random


def create_email(f_name, l_name, b_year, email_provider, email_domain, valid_chars, invalid_chars):
    email = '%s.%s%d@%s.%s' % (f_name,
                               l_name,
                               b_year,
                               random.choice(email_provider),
                               random.choice(email_domain))
    email_valid = check_invalid_chars(email, valid_chars, invalid_chars)
    return email_valid


def check_invalid_chars(string, valid_chars, invalid_chars):
    for index, invalid_char in enumerate(invalid_chars):
        if invalid_char in string:
            string = string.replace(invalid_char, valid_chars[index])
    return string


def create_mentor_table():
    table = []
    first_names = ['Miklós',
                   'Tamás',
                   'Dániel',
                   'Mateusz',
                   'Attila',
                   'Pál',
                   'Sándor',
                   'Prezmek',
                   'John',
                   'Tim',
                   'Matthew',
                   'Andy',
                   'Giancarlo']
    last_names = ['Beöthy',
                  'Tompa',
                  'Salamon',
                  'Ostafil',
                  'Molnár',
                  'Monoczki',
                  'Szodoray',
                  'Ciacka',
                  'Carrey',
                  'Obama',
                  'Lebron',
                  'Hamilton',
                  'Fisichella']
    email_domain = ['hu', 'com', 'pl', 'cz', 'uk', 'at', 'de']
    email_provider = ['gmx', 'freemail', 'gmail', 'hotmail']
    valid_chars = ['a', 'e', 'i', 'o', 'o', 'o', 'u', 'u', 'u']
    invalid_chars = ['á', 'é', 'í', 'ó', 'ö', 'ő', 'ú', 'ü', 'ű']
    cities = ['Budapest', 'Miskolc', 'Krakow', 'Barcelona', 'New York']

    for i in range(10000):
        f_name = random.choice(first_names)
        l_name = random.choice(last_names)
        b_year = random.randint(1960, 1995)
        email = create_email(f_name, l_name, b_year, email_provider, email_domain, valid_chars, invalid_chars)
        city = random.choice(cities)
        phone = '+%d' % random.randint(1000000000, 9999999999)
        level = random.randint(1, 10)
        table.append([f_name,
                      l_name,
                      phone,
                      email,
                      city,
                      level,
                      b_year])
    return table


def write_mentors_into_csv(file):
    table = create_mentor_table()
    with open(file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        [writer.writerow(r) for r in table]


def main(file):
    write_mentors_into_csv(file)


if __name__ == '__main__':
    main('mentor_candidates.csv')
