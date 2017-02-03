#!/usr/bin/python3
import subprocess
import re

stat = {
    'correct': 0,
    'incorrect': 0
}


def run(command_list):
    process = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error = process.stderr.decode("utf-8")  # returning the stderr text, if any
    if len(error) > 0:
        return error
    return process.stdout.decode("utf-8")


def run_sql_file(file_name):
    return run(['psql', '-f', file_name])


def build_regex_for_line(line_elements):
    regex = r'\s' + line_elements[0].strip()
    for elem in line_elements[1:]:
        regex += r'\s*\|\s' + elem.strip()

    return regex


def clear_sql_output_line(line):
    return re.sub(r'\s*\|\s*', ', ', line)


def test_output(checked, headers, expected, prefix_lines=None):
    splitted = checked.split('\n')

    if prefix_lines is not None:
        for i in range(len(prefix_lines)):
            if prefix_lines[i] != splitted[i]:
                _expected = prefix_lines[i]
                got = clear_sql_output_line(splitted[i]).strip()
                if _expected != got:
                    return {
                        'error': 'Output error before the SELECT',
                        'expected': _expected + ' | length: ' + str(len(_expected)),
                        'got': got + ' | length: ' + str(len(got))
                    }

        for i in range(len(prefix_lines)):
            splitted.pop(0)

    if re.match(build_regex_for_line(headers), splitted[0]) is None:
        _expected = ', '.join(headers)
        got = clear_sql_output_line(splitted[0]).strip()
        if _expected != got:
            return {
                'error': 'Error in headers',
                'expected': _expected + ' | length: ' + str(len(_expected)),
                'got': got + ' | length: ' + str(len(got))
            }

    data_lines = splitted[2:-3]
    if len(data_lines) != len(expected):
        return {
            'error': 'Wrong number of output lines',
            'expected': str(len(expected)) + ' lines',
            'got': str(len(data_lines)) + ' lines'
        }

    for i in range(len(data_lines)):
        if re.match(build_regex_for_line(expected[i]), data_lines[i]) is None:
            _expected = ', '.join(expected[i])
            got = clear_sql_output_line(data_lines[i]).strip()
            if _expected != got:
                return {
                    'error': 'Output error',
                    'expected': _expected + ' | length: ' + str(len(_expected)),
                    'got': got + ' | length: ' + str(len(got))
                }

    return True


def test_sql_file(file_name, headers, expected_values, prefix_lines=None):
    global stat

    output = run_sql_file(file_name)
    test_result = test_output(output, headers, expected_values, prefix_lines)
    if test_result is True:
        print(file_name + ' works as expected')
        stat['correct'] += 1
    else:
        print('\n!! Error detected')
        print('File: ', file_name)
        print('Error: ' + test_result['error'])
        print('Expected: ' + test_result['expected'])
        print('Got: ' + test_result['got'])
        print('Full output:\n' + output + '\n')
        stat['incorrect'] += 1


def main():
    global stat

    # build tables and populate data
    run_sql_file('clean-db.sql')
    run_sql_file('build-mentors-table.sql')
    run_sql_file('build-mentor-candidates-table.sql')
    run_sql_file('build-schools-table.sql')

    run_sql_file('1-fake-mentor-candidates.sql')

    test_sql_file(
        'test-1-fake-mentor-candidates.sql',
        ['count'],
        [["10000"]]
    )

    run_sql_file('2-optimize-queries.sql')
    test_sql_file(
        'test-2-optimize-queries.sql',
        ['table_name', 'index_name', 'column_names'],
        [
            ['mentor_candidates', 'mentor_candidates_birth_year_city_idx', 'city, birth_year'],
            ['mentor_candidates', 'mentor_candidates_city_idx', 'city'],
            ['schools', 'schools_city_idx', 'city']
        ]
    )

    run_sql_file('3-alter-schools-table.sql')
    test_sql_file(
        'test-3-alter-schools-table.sql',
        ['column_name', 'data_type'],
        [
            ["id", "integer"],
            ["code", "character varying"],
            ["city", "character varying"],
            ["country", "character varying"],
            ["contact_person", "integer"],
            ["address", "character varying"],
        ]
    )

    run_sql_file('4-alter-mentor-candidates-table.sql')
    test_sql_file(
        'test-4-alter-mentor-candidates-table.sql',
        ['id'],
        [
            ["10000"]
        ]
    )

    print(
        '\n\n' + str(stat['correct'] + stat['incorrect']) +
        ' tests ran: \n\t' + str(stat['correct']) +
        ' correct\n\t' + str(stat['incorrect']) + ' incorrect')

    return stat

if __name__ == '__main__':
    main()
