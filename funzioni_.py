from TempoContinuo import studioTempoContinuo
from Osservabilita import studioOsservabilita
from Raggiungibilita import studioRaggiungibilita
from FunzioneTrasferimento import funzioneTrasferimento
from Kalman import scomposizioneKalman
from Discretizzazione import discretizzazioneDaW
from Realizzazione import realizzazione

from tqdm import tqdm

from aux import l,gradino,impulso
from random import choice
from sympy import Matrix,Rational,pprint,eye

from sympy.abc import t
from sympy import cos,E,sin

val_mat = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,
		1,-1,-1,-1,-1,-1,2,2,2,-2,-2,3,3,-3,-3]

def c(l):
	return choice(l)

def genera_matrice():
	dim = choice([2,2,3])
	dim = 3
	controllo_lunghezza = 100
	while controllo_lunghezza >60:
		if dim==2:
			mat = Matrix([[c(val_mat),c(val_mat)],[c(val_mat),c(val_mat)]])
		else:
			mat = Matrix([[c(val_mat),c(val_mat),c(val_mat)],[c(val_mat),c(val_mat),c(val_mat)],[c(val_mat),c(val_mat),c(val_mat)]])
		controllo_lunghezza = len(str(mat.eigenvals()))
	return mat

def crea_esercizio(num,test):
	#Il caso predefinito
	A = genera_matrice()
	B = Matrix([1,0,1])
	C = Matrix([[1,-1,0]])
	D = Matrix([0])
	x_0 = Matrix([0,0,0,0])
	u_t = [impulso(t)]#,gradino(t),sin(t)]
	#77,88,99 sono valori speciali con matrici predefinite
	if num==77:
		#caso autovettori complessi
		A = Matrix([[-3,-1,0],[2,-1,0],[-1,-1,-1]])
		B = Matrix([1,0,1])
		C = Matrix([[1,-1,0]])
		x_0 = Matrix([0,0,0])

	if num==88:
		A = Matrix([[1,-3,-2],[2,-4,-2],[-1,1,0]])
		B = Matrix([2,1,0])
		C = Matrix([[1,-2,-1]])
		x_0 = Matrix([0,0,0])

	if num==99:
		A = Matrix([[3,2,-4],[0,1,0],[2,1,-3]])
		B = Matrix([1,1,0])
		C = Matrix([[1,-1,0]])
		x_0 = Matrix([0,0,0])
	if num==111:
		A = Matrix([[-1,0],[0,-2]])
		B = Matrix([1,-1])
		C = Matrix([[1,1]])
		D = Matrix([0])
		x_0 = Matrix([0,0])
	if num==122:
		A = Matrix([[-3,1,0,0],[0,-1,0,0],[0,0,-2,0],[0,1,1,-1]])
		B = Matrix([1,0,0,0])
		C = Matrix([[1,1,0,0]])
		D = Matrix([0])
		x_0 = Matrix([0,0,0,0])
	if num==133:
		A = Matrix([-10])
		B = Matrix([1])
		C = Matrix([1])
		D = Matrix([0])
		x_0 = Matrix([0])
	



	out = "Studiare il sistema \[S:\\begin{cases}\overset{\cdot}{x} = %s x+ %su\\\\y = %s x\end{cases}\]"%(l(A),l(B),l(C))
	out +="\subsection{Studio Risposta Libera}\n"
	s, Xl_flag = studioTempoContinuo(A,B,C,D,x_0,u_t,test)
	out += s
	'''
	if not Xl_flag:
		return out
	if A.rows>1:
		out +="\n\subsection{Studio Osservabilità}\n"
		s, I = studioOsservabilita(A,C)
		out += s
			
		out +="\n\subsection{Studio Raggiungibilità}\n"
		s, R_ = studioRaggiungibilita(A,B)
		out += s
		out +="\n\subsection{Scomposizione di Kalman}\n"
		out += scomposizioneKalman(A,B,C,I,R_,test)
	'''
	out +="\n\subsection{Studio Funzione di trasferimento}\n"
	s,W = funzioneTrasferimento(A,B,C,D,x_0,u_t)
	out += s
	s,d = discretizzazioneDaW(W)
	out+=s
	out+="\n\subsection{Realizzazione}\n"
	s,azz,uff = realizzazione(W)
	out+=s
	s,W = funzioneTrasferimento(uff[0],uff[1],uff[2],D,x_0,u_t)
	out+=s
	
	return out
