#!/bin/bash
base_dir="${HOME}/docs/jnl"
year=`date +%Y`
month=`date +%m` 
filename="`date +%d.%H%M`.jnl"
outfile="${base_dir}/${year}/${month}/${filename}"

if [ -d ${base_dir}/${year}/${month} ]; then 	# check to make sure this
	~/projects/logit/logit.py > ${outfile} 		# month's directory exists
else											# if it doesn't, make it.
	mkdir -p ${base_dir}/${year}/${month}
	~/projects/logit/logit.py > ${outfile}
fi

vim ${outfile}
