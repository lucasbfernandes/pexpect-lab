import pexpect

def main():
    ditg_receiver = pexpect.spawn('/home/lucasbfernandes/Downloads/D-ITG-2.8.1-r1023/bin/ITGSend -T UDP -a 10.0.2.10 -e 25 -C 5000 -t 50000 -l sender.log -x receiver.log')
    ditg_receiver.wait()

main()