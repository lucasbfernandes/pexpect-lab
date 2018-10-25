import pexpect
import time
import argparse
import os
import pandas

RESULTS_DIRECTORY = 'results'
P4_PROJECT_PATH = '/home/lucasbfernandes/Work/UFU/projects/p4-dev/projects/multipath-probability-qos'
PEXPECT_PROJECT_PATH = '/home/lucasbfernandes/Work/UFU/side/pexpect-lab/probability-qos'


def get_command_line_arguments():
    parser = argparse.ArgumentParser(description='Probability qos project runner')
    parser.add_argument('-n', help='Number of performance tests', type=int, action="store", required=True)
    return parser.parse_args()


def delete_results_directory():
    if os.path.exists(RESULTS_DIRECTORY):
        print('Deleted results directory with path {path}/results'.format(path=PEXPECT_PROJECT_PATH))
        pexpect.run('rm -r {path}/results'.format(path=PEXPECT_PROJECT_PATH))


def create_results_directory():
    pexpect.run('mkdir {path}/results'.format(path=PEXPECT_PROJECT_PATH))
    print('Results directory created with path {path}/results'.format(path=PEXPECT_PROJECT_PATH))


def move_result_log(index):
    pexpect.run('cp /tmp/p4s.s1.log {path}/results/test{index}.log'.format(index=index, path=PEXPECT_PROJECT_PATH))
    print('Result file generated with path {path}/results/test{index}.log'.format(index=index, path=PEXPECT_PROJECT_PATH))


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
        final_results_row.append(final_results_dict[column_name])
    return final_results_row


def get_final_results_array(final_results):
    final_results_array = []
    column_names = ['max_flow', 'total_flow', 'drop_rate', 'packets_dropped', 'total_dropped', 'total_passed']
    for key in final_results:
        final_results_array.append([key] + build_final_results_row(final_results[key], column_names))
    return final_results_array


def compute_final_results_mean(final_results, row_count):
    for key in final_results:
        final_results[key] = compute_row_mean(final_results, row_count, key)


def run_performance_tests_setup():
    delete_results_directory()
    create_results_directory()


def run_performance_tests():
    mn_clean = pexpect.spawn('mn -c')
    mn_clean.expect('Cleanup complete.')

    run_project = pexpect.spawn('python {path}/tools/run_project.py'.format(path=P4_PROJECT_PATH))
    run_project.expect('mininet>')

    apply_commands = pexpect.spawn('python {path}/tools/apply_commands.py'.format(path=P4_PROJECT_PATH))
    apply_commands.wait()

    run_project.sendline('h3 /bin/bash -c "python {path}/receiver-host.py" &'.format(path=PEXPECT_PROJECT_PATH))
    time.sleep(5)

    run_project.sendline('h1 /bin/bash -c "python {path}/sender-host.py" &'.format(path=PEXPECT_PROJECT_PATH))
    time.sleep(70)


def main():
    arguments = get_command_line_arguments()
    print('Starting performance tests')
    run_performance_tests_setup()

    for i in range(arguments.n):
        print('Running test: #{index}'.format(index=i+1))
        run_performance_tests()
        print('Finished test: #{index}'.format(index=i+1))
        move_result_log(i+1)

    final_results = {}
    row_count = {}
    for i in range(arguments.n):
        df = pandas.read_csv('{path}/results/test{index}.log'.format(path=PEXPECT_PROJECT_PATH, index=i+1), sep=';', header=None)
        df.columns = ['seconds', 'max_flow', 'total_flow', 'drop_rate', 'packets_dropped', 'total_dropped', 'total_passed']
        compute_final_results(df, final_results, row_count)
        print(df.head(5))

    compute_final_results_mean(final_results, row_count)
    final_results_array = get_final_results_array(final_results)

    final_df = pandas.DataFrame(final_results_array)
    final_df.columns = ['seconds', 'max_flow', 'total_flow', 'drop_rate', 'packets_dropped', 'total_dropped', 'total_passed']
    print(final_df.head(5))

    final_df.to_csv('{path}/results/final_results.log'.format(path=PEXPECT_PROJECT_PATH), index=False, sep=';', header=None)


main()
