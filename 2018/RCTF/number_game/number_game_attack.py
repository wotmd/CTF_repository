#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import hashlib
import string
import itertools
import time
from itertools import permutations


conn = remote('149.28.139.172', 10002)

##bulls and cows solver
TYPE_MODE_TEST = 'TEST'
TYPE_MODE_DEBUG = 'DEBUG'
TYPE_MODE_GAME = 'GAME'
CONFIG_MODE = TYPE_MODE_GAME

CONFIG_POOL = ["0","1","2","3","4","5","6","7","8","9"]
CONFIG_NUM_DIGIT = 4

POTEN = [] # POTENTIAL OF STRIKE, BALL PAIRS
#POTEN = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (3, 0)]
for s in range(CONFIG_NUM_DIGIT + 1):
	for b in range(CONFIG_NUM_DIGIT + 1):
		if s + b <= CONFIG_NUM_DIGIT:
			POTEN.append((s, b))
WIN_KEY = '%dS0B'%(CONFIG_NUM_DIGIT)

def is_allowed_number(number):
	_number = str(number)
	return len(_number) == CONFIG_NUM_DIGIT and \
		   len(set(_number)) == CONFIG_NUM_DIGIT and \
		   all(int(i) in CONFIG_POOL for i in _number)

SET_POOL = set(CONFIG_POOL)
ALL_NUMBERS = [int(''.join(number)) for number in permutations(CONFIG_POOL,4)]

#print(ALL_NUMBERS)
CONFIG_POOL = [0,1,2,3,4,5,6,7,8,9]

TEST_ACCELERATION_INDEX = {}
def get_to_index(SB_history):
	a = TEST_ACCELERATION_INDEX
	for key in SB_history:
		if key not in a:
			return None
		a = a[key]
	return a['Q']

def set_to_index(SB_history, new_question):
	a = TEST_ACCELERATION_INDEX
	for key in SB_history[:-1]:
		a = a[key]
	a[SB_history[-1]] = {'Q': new_question}

def calc_s_and_b(q, a):
	_q = str(q).rjust(4, '0')
	_a = str(a).rjust(4, '0')
	s = 0
	b = 0
	for i in range(CONFIG_NUM_DIGIT):
		if _q[i] == _a[i]:
			s += 1
		elif _q[i] in _a:
			b += 1
	return s, b

def calc_pool(q, s, b, pool):
	result = 0
	_q = str(q)
	for a in pool:
		_s, _b = calc_s_and_b(_q, a)
		if s == _s and b == _b:
			result += 1
	return result

def update_pool(q, s, b, pool):
	result = []
	_q = str(q).rjust(4, '0')
	for a in pool:
		_s, _b = calc_s_and_b(_q, a)
		if s == _s and b == _b:
			result.append(a)
	return result

def calc_best_question(a_pool, history):
	q_pool = []
	before_count = len(a_pool)
	if before_count == 1:
		return a_pool[0], True
	before_count = float(before_count)

	duplicates = set()
	for q in ALL_NUMBERS:
		q_str = str(q).rjust(4, '0')
		for i in CONFIG_POOL:
			if i not in history:
				q_str = q_str.replace(str(i), 'X')
		if q_str in duplicates:
			continue
		duplicates.add(q_str)
		q_pool.append(q)

	best = 0.0
	recom = None
	_q = 0
	dups = []

	if CONFIG_MODE == TYPE_MODE_DEBUG:
		print 'A Pool: %s'%(a_pool)
	for q in q_pool:
		result = {}
		cache = {}
		total = 0.0
		for s, b in POTEN:
			remain_count = calc_pool(q, s, b, a_pool)
			if remain_count == 0:
				continue
			total += remain_count
			key = '%dS%dB'%(s,b)
			cache[key] = remain_count
			result[key] = remain_count

		is_duplicate = False
		for dup in dups:
			if dup.keys() == cache.keys():
				check = []
				for key in cache:
					check.append( cache[key] == dup[key] )
				if all(check):
					is_duplicate = True
					break

		if is_duplicate:
			continue
		dups.append(cache)

		if CONFIG_MODE == TYPE_MODE_DEBUG:
			print 'Answer: %s'%(q)
		score = 0.0
		for key in sorted(result.keys(), key=lambda x: result[x], reverse=True):
			probability = result[key] / before_count
			if key == WIN_KEY:
				score += probability * (before_count - result[key] + 1) / before_count
			else:
				score += probability * (before_count - result[key]) / before_count
		score *= 10
		if CONFIG_MODE == TYPE_MODE_DEBUG:
			print 'Score: %.2f'%(score)
		if best < score:
			best = score
			recom = result
			_q = q


	if CONFIG_MODE == TYPE_MODE_DEBUG or CONFIG_MODE == TYPE_MODE_GAME:
		guessNum = str(_q).rjust(4, '0')
		guessNum = guessNum[0]+" "+guessNum[1]+" "+guessNum[2]+" "+guessNum[3]
		#print(guessNum)
		conn.sendline(guessNum)
		print 'Recommend Answer: %s'%( guessNum )
	result = recom
	score = 0.0
	for key in sorted(result.keys(), key=lambda x: result[x], reverse=True):
		probability = result[key] / before_count
		if key == WIN_KEY:
			score += probability * (before_count - result[key] + 1) / before_count
		else:
			score += probability * (before_count - result[key]) / before_count
	score *= 10
	if CONFIG_MODE == TYPE_MODE_DEBUG or CONFIG_MODE == TYPE_MODE_GAME:
		print 'Score: %.2f'%(score)

	return _q, len(result) <= 1 # FINISH

def interactive_game():
	pool = ALL_NUMBERS
	history = set()
	count = 0
	while True:
		q, is_finished = calc_best_question(pool, history)
		
		if is_finished:
			# START NEW GAME
			print 'Game Finished! Answer: %d, Question Count: %d'%(q, count)
			pool = ALL_NUMBERS
			history.clear()
			count = 0
			
			guessNum = str(q).rjust(4, '0')
			guessNum = guessNum[0]+" "+guessNum[1]+" "+guessNum[2]+" "+guessNum[3]
			#print(guessNum)
			conn.sendline(guessNum)
			print(conn.recvline())
			return
			
		count += 1
		result = conn.recvline()
		if "Nope" in result:
			print(result)
		else:
			print(result)
			print 'Game Finished! Answer: %d, Question Count: %d'%(q, count)
			pool = ALL_NUMBERS
			history.clear()
			count = 0
			return
		result = result[6:]
		bulls, cows = result.split(",")
		
		s = int(bulls.strip())
		b = int(cows.strip())
		#print("s:%d b:%d" %(s,b))
		pool = update_pool(q, s, b, pool)

		# HISTORY UPDATE (USED NUMBER)
		for i in range(CONFIG_NUM_DIGIT):
			history.add(q % 10)
			q /= 10


alphabet = string.digits+string.ascii_letters

result = conn.recvline()
print(result)

shaHash=result.split(" == ")[1].strip()

prefix = result.split(")")[0].strip()
prefix = prefix.split("+")[1].strip()
print(prefix)
print(conn.recvuntil('Give me XXXX:'))

for cand in itertools.product(alphabet, repeat=4):
	cand = ''.join(cand)
	cand_word = cand+prefix
	cand_word = cand_word.encode('utf8')
	digest = hashlib.sha256(cand_word).hexdigest()
	if digest == shaHash: # and ord(digest[3]) >= 0xF0:
		conn.sendline(cand)
		break

level = 0
		
##stage1
conn.recvuntil("GLHF")
conn.recvline()
conn.recvline()
while(1):
	if level == 8:
		print(recv)
		conn.interactive()
	level+=1
	recv = conn.recv(1)
	recv += conn.recv(1)
	recv += conn.recv(1)
	if "==" in recv:
		print(conn.recvline())
		conn.recvline()
	elif "Gi" in recv:
		print(recv)
	else:
		print(conn.recvline())
		conn.recvline()
	interactive_game()
conn.interactive()
"""
guessNum=""
conn.recvuntil()

Question = solver.recvline()
guessNum = Question[12:].strip()
guessNum = guessNum[0]+" "+guessNum[1]+" "+guessNum[2]+" "+guessNum[3]
print(guessNum)

conn.sendline(guessNum)
result = conn.recvline()
if "Nope" in result:
	print(result)
else:
	break
result = result[6:]
bulls, cows = result.split(",")
bullsNcows = bulls.strip()+" "+cows.strip()
solver.sendline(bullsNcows)
solver.close()

conn.sendline(guessNum)
	
conn.interactive()






"""



