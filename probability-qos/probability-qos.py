import pexpect
import time
import argparse
import os


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
    time.sleep(120)


def main():
    arguments = get_command_line_arguments()
    print('Starting performance tests')
    run_performance_tests_setup()
    for i in range(arguments.n):
        print('Running test: #{index}'.format(index=i+1))
        run_performance_tests()
        print('Finished test: #{index}'.format(index=i+1))
        move_result_log(i+1)


main()
