#!/bin/bash
# logit.sh 
# created by Arlo Gittings
# last modified 2021-07-06
# description:
# 	a bash wrapper for creating journal entries.
# Usage:
#	logit


# Flie structure creation
project_dir="${HOME}/projects/logit"     		# change to instalation path
nvim_config="${HOME}/.config/nvim/logit.vim"
base_dir="${HOME}/docs/jnl"
year=`date +%Y`
month=`date +%m` 
filename="`date +%d.%H%M`.jnl"
outfile="${base_dir}/${year}/${month}/${filename}"
vimfile="logit.vim"

source ${project_dir}/bin/activate        

if [ -d ${base_dir}/${year}/${month} ]; then 	# check to make sure this
	~/projects/logit/logit.py > ${outfile} 		# month's directory exists
else											# if it doesn't, make it.
	mkdir -p ${base_dir}/${year}/${month}
	~/projects/logit/logit.py > ${outfile}
fi

nvim -u ${nvim_config} ${outfile}
