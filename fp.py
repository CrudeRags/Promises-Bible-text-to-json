#!/bin/python

import re
import sys
import json

def Get_Sentences(infile):				#Get text blocks - A text block is problem, promise and prayer
	blocks = []
	with open(infile) as fp:
		for result in re.findall('Start_: (.*?)End_',fp.read(),re.S):
			blocks.append(result)
	return blocks

def Get_Index(arr,string):
	for s in arr:
		if(string in s):
			return(arr.index(s))

def Get_Line(arr,string):
	for s in arr:
		if(string in s):
			return(arr.pop(arr.index(s)))

def Strip_Quotes(arr):			#Remove quotation marks
	new_arr = []
	temp_string = ""

	for ar in arr:
		mini_dict = {}
		if("Promise:" in ar):
			try:
				ar = ar.split("Promise:").pop()
			except:
				continue
		if ar:
			try:
				if temp_string:
					ar = temp_string + ar
					temp_string = False
				text,ref = ar.rsplit('\" ',1)
				text = text.strip('"')
				mini_dict["text"] = text
				mini_dict["title"] = ref
				new_arr.append(mini_dict)
			except ValueError:
				temp_string = ar
				continue
	return new_arr

def Block_Process(block):
	b_d = {}												#basic dictionary
	s_b_d = {}											#Super Basic Dictionary - excluding prayer and problem
	raw_text=[]
	raw_text = str(block).splitlines()
	title = raw_text.pop(0)
	problem = Get_Line(raw_text,'Problem:')
	if problem:
		problem = problem.split('roblem: ').pop()
	raw_promises = raw_text[Get_Index(raw_text,'Promise:'):Get_Index(raw_text,'Prayer:')]
	promises = Strip_Quotes(raw_promises)
	raw_prayer = raw_text[Get_Index(raw_text,'Prayer:'):]
	p_prayer = " ".join(raw_prayer)
	prayer = p_prayer.split("rayer: ").pop()
	b_d["section"] = title
	b_d["problem"] = problem
	b_d["verses"] = promises
	b_d["prayer"] = prayer
	s_b_d["section"] = title
	s_b_d["verses"] = promises
	return b_d,s_b_d

master_array = []
mod_master_array = []
blocks = Get_Sentences(str(sys.argv[-1]))
for block in blocks:
	if block:
		basic_dict,super_basic_dict = Block_Process(block)
		master_array.append(basic_dict)
		mod_master_array.append(super_basic_dict)

with open('Promises-Solve.json','w') as outfile:
	json.dump(master_array, outfile, sort_keys = True, indent = 4, ensure_ascii = False)

with open('Promises_basic.json','w') as outfile:
	json.dump(mod_master_array, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
