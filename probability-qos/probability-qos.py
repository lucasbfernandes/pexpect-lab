import pexpect
import time
import argparse
import os
import pandas
import math
import constants


P4_PROJECT_PATH = '/home/lucasbfernandes/Work/UFU/projects/p4-dev/projects/multipath-probability-qos'
PEXPECT_PROJECT_PATH = '/home/lucasbfernandes/Work/UFU/side/pexpect-lab/probability-qos'


def get_command_line_arguments():
    parser = argparse.ArgumentParser(description='Probability qos project runner')
    parser.add_argument('-n', help='Number of performance tests', type=int, action="store", required=True)
    parser.add_argument('-d', nargs='+', help='Distributions names', type=str, required=True)
    return parser.parse_args()


def delete_results_directory(distribution):
    if os.path.exists(distribution):
        pexpect.run('rm -r {path}/{d}'.format(path=PEXPECT_PROJECT_PATH, d=distribution))
        print('Deleted {d} directory with path {path}/{d}'.format(path=PEXPECT_PROJECT_PATH, d=distribution))


def create_results_directory(distribution):
    pexpect.run('mkdir {path}/{d}'.format(path=PEXPECT_PROJECT_PATH, d=distribution))
    print('Directory {d} created with path {path}/{d}'.format(path=PEXPECT_PROJECT_PATH, d=distribution))


def move_result_log(index, distribution):
    pexpect.run('cp /tmp/p4s.s1.log {path}/{d}/test{index}.log'.format(index=index, d=distribution, path=PEXPECT_PROJECT_PATH))
    print('Result file generated with path {path}/{d}/test{index}.log'.format(index=index, d=distribution, path=PEXPECT_PROJECT_PATH))


def build_deviation_results_row(deviation_results_dict, column_names):
    deviation_results_row = []
    for column_name in column_names:
        if not column_name == 'drop_rate':
            deviation_results_row.append(int(math.floor(deviation_results_dict[column_name])))
        else:
            deviation_results_row.append(deviation_results_dict[column_name])
    return deviation_results_row


def get_deviation_results_array(deviation_results):
    deviation_results_array = []
    column_names = ['max_flow', 'total_flow', 'drop_rate', 'packets_dropped', 'total_dropped', 'total_passed']
    for key in deviation_results:
        deviation_results_array.append([int(key)] + build_deviation_results_row(deviation_results[key], column_names))
    return deviation_results_array


def get_deviation_row_data_dict(row):
    return {
        'max_flow': math.sqrt(row['max_flow']),
        'total_flow': math.sqrt(row['total_flow']),
        'drop_rate': math.sqrt(row['drop_rate']),
        'packets_dropped': math.sqrt(row['packets_dropped']),
        'total_dropped': math.sqrt(row['total_dropped']),
        'total_passed': math.sqrt(row['total_passed'])
    }


def compute_deviation_results(df, deviation_results):
    for index, row in df.iterrows():
        deviation_results[row['seconds']] = get_deviation_row_data_dict(row)


def compute_variance_row(row_dict, variance_results, key):
    return {
        'max_flow': variance_results[key]['max_flow'] + row_dict['max_flow'],
        'total_flow': variance_results[key]['total_flow'] + row_dict['total_flow'],
        'drop_rate': variance_results[key]['drop_rate'] + row_dict['drop_rate'],
        'packets_dropped': variance_results[key]['packets_dropped'] + row_dict['packets_dropped'],
        'total_dropped': variance_results[key]['total_dropped'] + row_dict['total_dropped'],
        'total_passed': variance_results[key]['total_passed'] + row_dict['total_passed']
    }


def get_variance_row_data_dict(row, mean_results):
    row_second = row['seconds']
    return {
        'max_flow': math.pow(mean_results[row_second]['max_flow'] - row['max_flow'], 2),
        'total_flow': math.pow(mean_results[row_second]['total_flow'] - row['total_flow'], 2),
        'drop_rate': math.pow(mean_results[row_second]['drop_rate'] - row['drop_rate'], 2),
        'packets_dropped': math.pow(mean_results[row_second]['packets_dropped'] - row['packets_dropped'], 2),
        'total_dropped': math.pow(mean_results[row_second]['total_dropped'] - row['total_dropped'], 2),
        'total_passed': math.pow(mean_results[row_second]['total_passed'] - row['total_passed'], 2)
    }


def compute_variance_row_results(row_dict, variance_results, key):
    if key in variance_results:
        variance_results[key] = compute_variance_row(row_dict, variance_results, key)
    else:
        variance_results[key] = row_dict


def compute_variance_results(df, variance_results, mean_results):
    for index, row in df.iterrows():
        row_dict = get_variance_row_data_dict(row, mean_results)
        compute_variance_row_results(row_dict, variance_results, row['seconds'])


def compute_variance_row_mean(variance_results, row_count, key):
    return {
        'max_flow': variance_results[key]['max_flow'] / row_count[key],
        'total_flow': variance_results[key]['total_flow'] / row_count[key],
        'drop_rate': variance_results[key]['drop_rate'] / row_count[key],
        'packets_dropped': variance_results[key]['packets_dropped'] / row_count[key],
        'total_dropped': variance_results[key]['total_dropped'] / row_count[key],
        'total_passed': variance_results[key]['total_passed'] / row_count[key]
    }


def compute_variance_results_mean(variance_results, row_count):
    for key in variance_results:
        variance_results[key] = compute_variance_row_mean(variance_results, row_count, key)


def build_variance_results_row(variance_results_dict, column_names):
    variance_results_row = []
    for column_name in column_names:
        if not column_name == 'drop_rate':
            variance_results_row.append(int(math.floor(variance_results_dict[column_name])))
        else:
            variance_results_row.append(variance_results_dict[column_name])
    return variance_results_row


def get_variance_results_array(variance_results):
    variance_results_array = []
    column_names = ['max_flow', 'total_flow', 'drop_rate', 'packets_dropped', 'total_dropped', 'total_passed']
    for key in variance_results:
        variance_results_array.append([int(key)] + build_variance_results_row(variance_results[key], column_names))
    return variance_results_array


def compute_row(row_dict, final_results, key):
    return {
        'max_flow': final_results[key]['max_flow'] + row_dict['max_flow'],
        'total_flow': final_results[key]['total_flow'] + row_dict['total_flow'],
        'drop_rate': final_results[key]['drop_rate'] + row_dict['drop_rate'],
        'packets_dropped': final_results[key]['packets_dropped'] + row_dict['packets_dropped'],
        'total_dropped': final_results[key]['total_dropped'] + row_dict['total_dropped'],
        'total_passed': final_results[key]['total_passed'] + row_dict['total_passed']
    }


def get_row_data_dict(row):
    return {
        'max_flow': row['max_flow'],
        'total_flow': row['total_flow'],
        'drop_rate': row['drop_rate'],
        'packets_dropped': row['packets_dropped'],
        'total_dropped': row['total_dropped'],
        'total_passed': row['total_passed']
    }


def compute_row_results(row_dict, final_results, row_count, key):
    if key in final_results:
        final_results[key] = compute_row(row_dict, final_results, key)
        row_count[key] += 1
    else:
        final_results[key] = row_dict
        row_count[key] = 1


def compute_final_results(df, final_results, row_count):
    for index, row in df.iterrows():
        row_dict = get_row_data_dict(row)
        compute_row_results(row_dict, final_results, row_count,  row['seconds'])


def compute_row_mean(final_results, row_count, key):
    return {
        'max_flow': final_results[key]['max_flow'] / row_count[key],
        'total_flow': final_results[key]['total_flow'] / row_count[key],
        'drop_rate': final_results[key]['drop_rate'] / row_count[key],
        'packets_dropped': final_results[key]['packets_dropped'] / row_count[key],
        'total_dropped': final_results[key]['total_dropped'] / row_count[key],
        'total_passed': final_results[key]['total_passed'] / row_count[key]
    }


def build_final_results_row(final_results_dict, column_names):
    final_results_row = []
    for column_name in column_names:
        if not column_name == 'drop_rate':
            final_results_row.append(int(math.floor(final_results_dict[column_name])))
        else:
            final_results_row.append(final_results_dict[column_name])
    return final_results_row


def get_final_results_array(final_results):
    final_results_array = []
    column_names = ['max_flow', 'total_flow', 'drop_rate', 'packets_dropped', 'total_dropped', 'total_passed']
    for key in final_results:
        final_results_array.append([int(key)] + build_final_results_row(final_results[key], column_names))
    return final_results_array


def compute_final_results_mean(final_results, row_count):
    for key in final_results:
        final_results[key] = compute_row_mean(final_results, row_count, key)


def run_performance_tests_setup(distributions):
    for distribution in constants.SENDER_OPTS:
        delete_results_directory(distribution)

    for distribution in distributions:
        create_results_directory(distribution)


def run_performance_tests(distribution):
    mn_clean = pexpect.spawn('mn -c')
    mn_clean.expect('Cleanup complete.')

    run_project = pexpect.spawn('python {path}/tools/run_project.py'.format(path=P4_PROJECT_PATH))
    run_project.expect('mininet>')

    apply_commands = pexpect.spawn('python {path}/tools/apply_commands.py'.format(path=P4_PROJECT_PATH))
    apply_commands.wait()

    run_project.sendline('h3 /bin/bash -c "python {path}/receiver-host.py" &'.format(path=PEXPECT_PROJECT_PATH))
    time.sleep(5)

    run_project.sendline('h1 /bin/bash -c "python {path}/sender-host.py -d {d}" &'.format(path=PEXPECT_PROJECT_PATH, d=distribution))
    time.sleep(120)


def run_distributions_tests(distributions, number_of_tests):
    print('Starting performance tests')
    for i in range(number_of_tests):
        print('Running test: #{index}'.format(index=i+1))
        for distribution in distributions:
            if distribution in constants.SENDER_OPTS:
                print('Running test #{index} for distribution {d}'.format(index=i+1, d=distribution))
                run_performance_tests(distribution)
                move_result_log(i + 1, distribution)
            else:
                print('Distribution {d} does not exist'.format(d=distribution))
        print('Finished test: #{index}'.format(index=i+1))


def generate_deviation_results(distribution, deviation_results):
    df = pandas.read_csv('{path}/{d}/variance_results.log'.format(path=PEXPECT_PROJECT_PATH, d=distribution), sep=';', header=None)
    df.columns = ['seconds', 'max_flow', 'total_flow', 'drop_rate', 'packets_dropped', 'total_dropped', 'total_passed']
    compute_deviation_results(df, deviation_results)
    deviation_results_array = get_deviation_results_array(deviation_results)

    deviation_df = pandas.DataFrame(deviation_results_array)
    deviation_df.columns = ['seconds', 'max_flow', 'total_flow', 'drop_rate', 'packets_dropped', 'total_dropped', 'total_passed']
    deviation_df.to_csv('{path}/{d}/deviation_results.log'.format(path=PEXPECT_PROJECT_PATH, d=distribution), index=False, sep=';', header=None)


def generate_variance_results(number_of_tests, distribution, variance_results, mean_results, row_count):
    for i in range(number_of_tests):
        df = pandas.read_csv('{path}/{d}/test{index}.log'.format(path=PEXPECT_PROJECT_PATH, d=distribution, index=i + 1), sep=';', header=None)
        df.columns = ['seconds', 'max_flow', 'total_flow', 'drop_rate', 'packets_dropped', 'total_dropped', 'total_passed']
        compute_variance_results(df, variance_results, mean_results)

    compute_variance_results_mean(variance_results, row_count)
    variance_results_array = get_variance_results_array(variance_results)

    variance_df = pandas.DataFrame(variance_results_array)
    variance_df.columns = ['seconds', 'max_flow', 'total_flow', 'drop_rate', 'packets_dropped', 'total_dropped','total_passed']
    variance_df.to_csv('{path}/{d}/variance_results.log'.format(path=PEXPECT_PROJECT_PATH, d=distribution), index=False, sep=';', header=None)


def generate_mean_results(number_of_tests, distribution, mean_results, row_count):
    for i in range(number_of_tests):
        df = pandas.read_csv('{path}/{d}/test{index}.log'.format(path=PEXPECT_PROJECT_PATH, d=distribution, index=i + 1), sep=';', header=None)
        df.columns = ['seconds', 'max_flow', 'total_flow', 'drop_rate', 'packets_dropped', 'total_dropped', 'total_passed']
        compute_final_results(df, mean_results, row_count)

    compute_final_results_mean(mean_results, row_count)
    final_results_array = get_final_results_array(mean_results)

    final_df = pandas.DataFrame(final_results_array)
    final_df.columns = ['seconds', 'max_flow', 'total_flow', 'drop_rate', 'packets_dropped', 'total_dropped',
                        'total_passed']
    final_df.to_csv('{path}/{d}/final_results.log'.format(path=PEXPECT_PROJECT_PATH, d=distribution), index=False, sep=';', header=None)


def generate_final_results(distributions, number_of_tests):
    for distribution in distributions:
        mean_results = {}
        row_count = {}
        variance_results = {}
        deviation_results = {}

        generate_mean_results(number_of_tests, distribution, mean_results, row_count)
        generate_variance_results(number_of_tests, distribution, variance_results, mean_results, row_count)
        generate_deviation_results(distribution, deviation_results)


def main():
    arguments = get_command_line_arguments()
    run_performance_tests_setup(arguments.d)
    run_distributions_tests(arguments.d, arguments.n)
    generate_final_results(arguments.d, arguments.n)


main()
