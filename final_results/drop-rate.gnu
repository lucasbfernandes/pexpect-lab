#!/usr/bin/gnuplot

set terminal png size 800,600
set xtics 5
set term png
set output ARG1.'/drop-rate.png'
set datafile separator ";"
plot ARG1.'/final_results.log' using 1:5 with lines title 'Drop rate'
