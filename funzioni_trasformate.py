from tqdm import tqdm

from aux import l,gradino,impulso,L,da_t_a_z
from random import choice,randint


from sympy.abc import t,c
from sympy import cos,E,sin,pprint
from sympy.core import pi

bin = [0,1,1,1,1,1,1,1,1]

val = [0,1,-1,2,-2]
angoli = [pi,-pi,pi/2,-pi/2,pi/4,-pi/4]
dur = [gradino(t),gradino(t),gradino(t)]

def c(l):
	return choice(l)

def coeff(a):
	if c(bin)==0:
		return 1/a
	else:
		return a

def crea_esercizio(num,test):
	a = c(val[1::])
	b = c(val)
	k = c(val)
	f_arr = [k*(a*t),k*(E**(a*t)),k*(a*t),k*(E**(a*t)),a**t,a*sin(b*t),a*cos(b*t)]


	f = c(f_arr)*c(dur)
	#f = 2*E**(-t)*gradino(t)

	Fl = L(f)
	#print(f)
	#print(Fl)
	Fz = da_t_a_z(f)
	out = "\n\[ f(t) = %s \]\n"%l(f)

	out+= "\n\[ \mathcal{L}\left[f(t)\\right] = %s \]\n"%(l(Fl))

	out+= "\n\[ \mathcal{Z}\left[f(t)\\right] = %s \]\n"%(l(Fz))


	return out
