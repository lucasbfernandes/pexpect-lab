#!/usr/bin/gnuplot

set terminal png size 2715,1527
set xtics 1
set term png
set output ARG1.'/drop-rate.png'
set datafile separator ";"
plot ARG1.'/final_results.log' using 1:5 with lines title 'Drop rate'
