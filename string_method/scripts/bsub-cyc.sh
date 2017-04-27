#!/bin/bash

# bsub-cyc.sh: A simple bash script for submission management                                                                             """
#
#   Usage:sh bsub-cyc.sh <startcycle> <endcycle>

start_cyc=$1 
end_cyc=$2

# Generate the cycles
python gen-bsub-cyc.py $start_cyc $end_cyc

# Submit each cycle
for (( cyc = $start_cyc; cyc <= end_cyc; cyc++ )); do

  for i in {1..37}; do

    # Uncomment for single machine usage:
    sh as.$i.$cyc.sh
    echo "IMAGE $i CYCLE $cyc FINISHED" >> as.$i.$cyc.o

    # Comment for single machine usage:
#    bsub < as.$i.$cyc.sh
  done  

  echo 'RUNNING ... CYCLE = '$cyc

  # Wait until current cycle finishes
  while true; do
    if [ -e 'string_'$cyc'.dat' ]; then
      sleep 1s
      echo 'CYCLE = '$cyc' COMPLETED'
      break
    else
      sleep 60s
    fi
  done

  # Clean up
  for i in {1..37}; do
    mv as.$i.$cyc.sh 0log/
    mv as.$i.$cyc.o 0log/

  done  

done
