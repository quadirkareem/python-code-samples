#!/usr/bin/python

import sys

def get_col_name(col):
	col_name = ''
	while True:
		if col < 1 :
			break
		rem = col % 26
		col = col / 26
		if rem == 0 :
			col_name = 'Z' + col_name
			col -= 1
		else :
			col_name = chr(64 + rem) + col_name
	return col_name

col = int(sys.argv[1])
col_name = get_col_name(col)
print "%d ==> %s" % (col, col_name)

