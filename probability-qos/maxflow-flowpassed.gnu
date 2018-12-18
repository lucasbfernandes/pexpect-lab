#!/usr/bin/gnuplot

set term png
set output ARG1.'/maxflow-flowpassed.png'
set datafile separator ";"
plot ARG1.'/final_results.log' using 1:2 with lines title 'Maxflow', ARG1.'/final_results.log' using 1:8 with lines title 'Flowpassed'
