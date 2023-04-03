from aux import l,invL,shorter,impulso
from random import choice


from lcapy import difference_equation,expr,nexpr
from lcapy import latex as llatex
from lcapy import simplify as lsimplify
from lcapy.discretetime import z

from sympy import simplify,Rational
from sympy import E
from sympy.abc import s,k,t

iniz_string = "\subsection{La discretizzazione a partire da W}\nLa funzione è \[ W(s) = \\frac{%s}{%s} \]\n\n"

s2 = "Per trovare $W(z)$ passo da $y_F(t)$:\n\[y_F(t) = \mathcal{L}^{-1}\left[ W(s)\\frac{1}{s}\\right]"
s3 = "\n = \mathcal{L}^{-1}\left[ \\frac{%s}{%s}\\frac{1}{s}\\right]\n = %s \]"

s4 = "Ora calcolo, $y_{dF}(k)$, ovvero $y_{dF}(kT_c)$ (Prendendo $T_c =1$):\n"
s5 = "\[ y_{dF}(k) =\left.\left[ %s \\right]\\right|_{t=kT_c}= %s  \]\n"
s6 = "Trasformo in z l'uscita ottenuta: \[[ \\mathcal{Z}\left[y_F(kT_c)\\right] = \\mathcal{Z}\left[ %s \\right] = \]\n\[ =  %s \]\n"
#s6 = "Trasformo in z l'uscita ottenuta: \[[ \\mathcal{Z}\left[y_F(kT_c)\\right] = \\mathcal{Z}\left[ %s \\right] = \]\n"
s7 = "Infine moltiplico per $\\frac{z-1}{z}$ per ottenere $W(z)$: \n\[ W(z) = %s \\frac{z-1}{z} =\]\n\[= %s \]\n"


def discretizza(ydFn_str):
	e = expr(ydFn_str)
	return 0 if e==0 else e.discrete_time()

def trasforma_in_Zeta(yFn):
	print(yFn)
	print(type(yFn))
	print(type(yFn) is int)
	return 0 if type(yFn) is int and yFn == 0 else yFn.ZT()


def discretizzazioneDaW(W):
	#Nw = W[0]
	periodi = [1]#,Rational(1,10),Rational(1,2)]
	T = 1#choice(periodi)#Rational(1,10)
	Dw = W[1]
	for Nw in W[0]:
		
		out = iniz_string%(l(Nw),l(Dw))
		out+=s2
		yFt = shorter(invL(Nw/(Dw*s)))
		
		#yFt = t*E**(-t)+impulso(t)
		out+= s3%(l(Nw),l(Dw),l(yFt))
		out += s4
		ydFk = yFt.replace(t,T*k)
		out += s5%(l(yFt),l(ydFk))
		#Trick per avere la classe espressione in tempo discreto
		ydFn_str = str(ydFk).replace('k','n')

		yFn = discretizza(ydFn_str)
		
		ZY = trasforma_in_Zeta(yFn)
		#print(ZY.expand().args)
		out += s6%(l(ydFk),l(shorter(ZY)))
		
		#stringa = "="
		#for i in ZY.expand().args:
		#	stringa+="\[ %s \]"%l(i)
		#out +=stringa
		#llatex(ZY.expand()))

		Wz = shorter(ZY*((z-1)/z))
		out += s7%(llatex(ZY),llatex(Wz))

	return out,[]
