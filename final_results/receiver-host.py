import pexpect
import constants


def main():
    ditg_receiver = pexpect.spawn('{path}'.format(path=constants.DITG_RECV_PATH))
    ditg_receiver.expect('Finish on UDP port', timeout=300)

main()
