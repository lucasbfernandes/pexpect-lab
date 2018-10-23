import pexpect

def main():
    ditg_receiver = pexpect.spawn('/home/lucasbfernandes/Downloads/D-ITG-2.8.1-r1023/bin/ITGRecv')
    ditg_receiver.expect('Finish on UDP port', timeout=300)

main()
