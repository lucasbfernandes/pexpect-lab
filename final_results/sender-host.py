import pexpect
import argparse
import constants


def get_distribution_command(distribution):
    if distribution in constants.SENDER_OPTS:
        return constants.SENDER_OPTS[distribution]
    else:
        return None


def get_command_line_arguments():
    parser = argparse.ArgumentParser(description='Probability qos project runner')
    parser.add_argument('-d', '--distributions', nargs='+', help='Distributions names', type=str, required=True)
    return parser.parse_args()


def run_ditg(distribution):
    command = get_distribution_command(distribution)
    if command:
        ditg_sender = pexpect.spawn('{path} {command}'.format(path=constants.DITG_SEND_PATH, command=command))
        ditg_sender.wait()


def main():
    arguments = get_command_line_arguments()
    for distribution in arguments.distributions:
        run_ditg(distribution)


main()
