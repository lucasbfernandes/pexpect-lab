#!/usr/bin/gnuplot

set term png
set output ARG1.'/final_passed_error_margin.png'
set datafile separator ";"
plot ARG1.'/final_results.log' using 1:2 with lines title 'Maxflow', ARG1.'/final_results.log' using 1:8 with lines title 'Flowpassed', ARG1.'/mean_plus_ci_results.log' using 1:8 with lines title 'Flowpassed +Error', ARG1.'/mean_minus_ci_results.log' using 1:8 with lines title 'Flowpassed -Error'
