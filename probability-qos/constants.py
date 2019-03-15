import os

SENDER_OPTS = {
    'constant': '-T UDP -a 10.0.2.10 -c 70 -C 10000 -t 100000 -l sender.log -x receiver.log',
    'uniform': '-T UDP -a 10.0.2.10 -u 30 70 -C 10000 -t 100000 -l sender.log -x receiver.log',
    'exponential': '-T UDP -a 10.0.2.10 -e 50 -C 10000 -t 100000 -l sender.log -x receiver.log',
    'normal': '-T UDP -a 10.0.2.10 -n 70 10 -C 10000 -t 100000 -l sender.log -x receiver.log',
    'poisson': '-T UDP -a 10.0.2.10 -o 50 -C 10000 -t 100000 -l sender.log -x receiver.log'
    # 'pareto': '-T UDP -a 10.0.2.10 -e 50 -C 10000 -t 100000 -l sender.log -x receiver.log',
    # 'cauchy': '-T UDP -a 10.0.2.10 -e 50 -C 10000 -t 100000 -l sender.log -x receiver.log',
    # 'gamma': '-T UDP -a 10.0.2.10 -e 50 -C 10000 -t 100000 -l sender.log -x receiver.log',
    # 'weibull': '-T UDP -a 10.0.2.10 -e 50 -C 10000 -t 100000 -l sender.log -x receiver.log'
}

GNUPLOT_SCRIPTS = [
    'maxflow-totalflow.gnu',
    'maxflow-flowpassed.gnu',
    'drop-rate.gnu'
]

CONFIDENCE_ZSCORES = {
    95: 1.960
}

P4_PROJECT_PATH = os.environ.get('P4_PROJECT_PATH') or '/home/lucasbfernandes/Work/UFU/projects/p4-dev/projects/multipath-probability-qos'
PEXPECT_PROJECT_PATH = os.environ.get('PEXPECT_PROJECT_PATH') or '/home/lucasbfernandes/Work/UFU/side/pexpect-lab/probability-qos'
DITG_RECV_PATH = os.environ.get('DITG_RECV_PATH') or '/home/lucasbfernandes/Downloads/D-ITG-2.8.1-r1023/bin/ITGRecv'
DITG_SEND_PATH = os.environ.get('DITG_SEND_PATH') or '/home/lucasbfernandes/Downloads/D-ITG-2.8.1-r1023/bin/ITGSend'
