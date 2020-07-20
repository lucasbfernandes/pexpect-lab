#!/usr/bin/gnuplot

set terminal png size 800,600
set xtics 5
set term png
set output ARG1.'/bandwidth-output.png'
set datafile separator ";"
plot ARG1.'/final_results.log' using 1:2 with lines title 'Contracted bandwidth', ARG1.'/final_results.log' using 1:8 with lines title 'Used bandwidth', ARG1.'/final_results.log' using 1:3 with lines title 'Incoming bandwidth'
