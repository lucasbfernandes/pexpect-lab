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