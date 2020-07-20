#!/usr/bin/gnuplot

set terminal png size 800,600
set xtics 5
set term png
set output ARG1.'/final_passed_error_margin.png'
set datafile separator ";"
plot ARG1.'/final_results.log' using 1:2 with lines title 'Contracted bandwidth', ARG1.'/final_results.log' using 1:8 with lines title 'Used bandwidth', ARG1.'/mean_plus_ci_results.log' using 1:8 with lines title 'Used bandwidth + Error', ARG1.'/mean_minus_ci_results.log' using 1:8 with lines title 'Used bandwidth - Error'
