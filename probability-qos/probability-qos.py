import pexpect
import time
import argparse
import os
RESULTS_DIRECTORY = 'results'


def get_command_line_arguments():
    parser = argparse.ArgumentParser(description='Probability qos project runner')
    parser.add_argument('-n', help='Number of performance tests', type=int, action="store", required=True)
    return parser.parse_args()


def create_results_directory():
    if not os.path.exists(RESULTS_DIRECTORY):
        pexpect.run('mkdir /home/lucasbfernandes/Work/UFU/side/pexpect-lab/probability-qos/results')
        print('Results directory created with path /home/lucasbfernandes/Work/UFU/side/pexpect-lab/probability-qos/results')


def move_result_log(index):
    pexpect.run('cp /tmp/p4s.s1.log /home/lucasbfernandes/Work/UFU/side/pexpect-lab/probability-qos/results/test{index}.log'.format(index=index))
    print('Result file generated with path /home/lucasbfernandes/Work/UFU/side/pexpect-lab/probability-qos/results/test{index}.log'.format(index=index))


def run_performance_tests_setup():
    create_results_directory()


def run_performance_tests():
    mn_clean = pexpect.spawn('mn -c')
    mn_clean.expect('Cleanup complete.')

    run_project = pexpect.spawn('python /home/lucasbfernandes/Work/UFU/projects/p4-dev/projects/multipath-probability-qos/tools/run_project.py')
    run_project.expect('mininet>')

    apply_commands = pexpect.spawn('python /home/lucasbfernandes/Work/UFU/projects/p4-dev/projects/multipath-probability-qos/tools/apply_commands.py')
    apply_commands.wait()

    run_project.sendline('h3 /bin/bash -c "python /home/lucasbfernandes/Work/UFU/side/pexpect-lab/probability-qos/receiver-host.py" &')
    time.sleep(5)

    run_project.sendline('h1 /bin/bash -c "python /home/lucasbfernandes/Work/UFU/side/pexpect-lab/probability-qos/sender-host.py" &')
    time.sleep(120)


def main():
    arguments = get_command_line_arguments()
    print('Starting performance tests')
    run_performance_tests_setup()
    for i in range(arguments.n):
        print('Running test: #{index}'.format(index=i))
        run_performance_tests()
        print('Finished test: #{index}'.format(index=i))
        move_result_log(i)


main()
