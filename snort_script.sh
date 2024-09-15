#!/bin/bash
# Clear the output file before running Snort
echo -n "" > snort_output.txt
# Run Snort and redirect output to snort_output.txt
sudo snort -q -A console -c /etc/snort/snort.conf > snort_output.txt 2>&1
