#!/usr/bin/python
#coding:utf-8
from __future__ import division

import sys
import io
import re
import glob
import os
import codecs
import zipfile
import numpy as np

os.chdir("./webpage_data_5")

markov = np.matrix([[0.0,0.0,0.0,0.0,0.0],
		    [0.0,0.0,0.0,0.0,0.0],
		    [0.0,0.0,0.0,0.0,0.0],
		    [0.0,0.0,0.0,0.0,0.0],
		    [0.0,0.0,0.0,0.0,0.0]])
origin = np.matrix([[0.0,0.0,0.0,0.0,0.0],
		    [0.0,0.0,0.0,0.0,0.0],
		    [0.0,0.0,0.0,0.0,0.0],
		    [0.0,0.0,0.0,0.0,0.0],
		    [0.0,0.0,0.0,0.0,0.0]])
mA     = np.matrix([[1.0],[0.0],[0.0],[0.0],[0.0]])
prob   = np.matrix([[0.0],[0.0],[0.0],[0.0],[0.0]])
finded = np.matrix([[0.0],[0.0],[0.0],[0.0],[0.0]])

filename = []
filelist = []
elilist  = []

pattern = "http://.*\.txt"
num = 5

#eatablish the file name list
for file in glob.glob("*.txt"):
    filelist.append(re.sub("\.txt$", "", file))
    filename.append(file)

#find the url link in files
for file in glob.glob("*.txt"):
    fo = open(file, "r")
    s = ""
    order = filelist.index(re.sub("\.txt$", "", file))
    for line in fo:
	s += line.decode("big5")
    if s.find(sys.argv[1].decode("utf-8")) != -1:
	finded[order] = 1
    match = re.findall(pattern, s)
    for m in match:
	x = re.sub("^http://|\.txt$","",m)
	markov[filelist.index(x), order] = 1
    fo.close()

origin = markov

#avoid dead ends
while 1:
    t = 0
    for j in range(num):
	x = 0
	for i in range(num):
	    x += markov[i, j]
	if x == 0:
	    y = j
	    for k in range(0, j, 1):
		if prob[k] == -1:
		    y = y + 1

	    markov = np.delete(markov, j, 1)
	    markov = np.delete(markov, j, 0)
	    mA     = np.delete(mA    , j, 0)
	    prob[y] = -1
	    elilist.append(y)
	    t = 1
	    break
    if t == 1:
	num = num - 1
    else:
	break

#eatablish the transport matrix
for j in range(num):
    x = 0
    for i in range(num):
	x += markov[i, j]
    for i in range(num):
	if markov[i, j] == 1:
	    markov[i, j] = 1/x
#count the page rank
while 1:
    mB = markov*mA
    t = 0
    for i in range(num):
	if abs(mA[i] - mB[i]) > 0.0000000001:
	    mA = mB
	    break
	else:
	    t = t + 1
    if t == num:
	break

for i in range(num):
    for j in range(len(prob)):
	if prob[j] == 0:
	    prob[j] = mB[i]
	    break

for j in range(5):
    x = 0
    for i in range(5):
	x += origin[i, j]
    for i in range(5):
	if origin[i, j] == 1:
	    origin[i, j] = 1/x

for i in range(len(elilist)-1, -1, -1):
    p = 0.0
    for j in range(5):
	p += origin[elilist[i], j]*prob[j]
    prob[elilist[i]] = p

#output result
rank = 1
sort_result = np.sort(prob, axis=0)
print "Rank\tFileName"
for i in range(4, -1, -1):
    x = -1
    for j in range(5):
	if prob[j] == sort_result[i]:
	    if prob[j] != -1:
		x = j
		prob[j] = -1
		break
    if finded[x] == 1:
	j = j + 1
	print str(rank)+"\t"+filename[j-1]
	rank = rank + 1
