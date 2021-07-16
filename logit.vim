" logit.vim
"== --- === --- === --- === --- === --- === --- === --- === --- === --- === --- 
"   created by Arlo Gittings
"   last modified: 2021-07-06
"   description:
" 	    custom config for logit. move it to your config directory and set 
" 	    the path inside of the shell script.
"== --- === --- === --- === --- === --- === --- === --- === --- === --- === --- 

set bs=2
set ts=4
set shiftwidth=4
syntax on
set ai
set nowrap

" Some basic-ish mappings and moving around
let mapleader = ";"
inoremap jkkj <esc>

inoremap <leader>h <left>
inoremap <leader>hh <home>

inoremap <leader>j <down>
inoremap <leader>jj <esc>GA

inoremap <leader>k <up>
inoremap <leader>kk <esc>ggi

inoremap <leader>l <right>
inoremap <leader>ll <end>


inoremap <leader>sep <esc>10i=== --- <esc>a
