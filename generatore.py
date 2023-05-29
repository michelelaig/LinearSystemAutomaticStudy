#!/usr/bin/python3
import sys
import subprocess
from random import randint,choice
from funzioni import crea_esercizio,realizzazione,funzioneTrasferimento
from sympy.abc import s
from sympy import Matrix,Rational

num_esercizi = 1

valori_diff = ['0','1','y_0']
valori_t_diff = ['0','1','t_0']
val_lim = ['0','+\\infty','-\\infty']

array_test = [77,88,99,111,122,133]
array_test = [159]
test = False
def compila_documento(tipo):
	stringone = ''
	i = 0
	if tipo=="test":
		for i in array_test:
			print(i)
			stringone += "\section{Esercizio %d }\n %s \n"%(i,crea_esercizio(i,True))
	elif tipo == "real":

		W = [Matrix([[s,0,1],[1,s+1,0]]),s**2+1]

		st,a,b= realizzazione(W)
		stringone+=st
	elif tipo == "W":
		k = Rational(1,10)
		Wn = Matrix([s**2+1])
		Wd = (s**2)*((s+1)**2)
		W = [[Wn,Wd]]

		st,a = funzioneTrasferimento(None,None,None,None,None,None,W =W)
		stringone+=st
	else:
		while(i<num_esercizi):
			stringone += "\section{Esercizio %d }\n %s \n"%(i,crea_esercizio(i,test))
			i+=1
	return stringone


print()
print()
flag_compila=False
if len(sys.argv)>1:
	if sys.argv[1]=="test":
		tipo = "test"
		num_esercizi = 0
	elif sys.argv[1]=="real":
		tipo = "real"
		num_esercizi = 0
	elif sys.argv[1]=="W":
		tipo =  "W"
		num_esercizi = 0
	else:
		num_esercizi = int(sys.argv[1])
else:
	tipo = "real"	
	flag_compila=True

if len(sys.argv)==3:
	flag_compila=True

NOME_TEMP = "template.tex"
NOME_OUT = "esercizio"



with open(NOME_TEMP,"r") as t:
	template = t.read()
stringone = compila_documento(tipo)

template = template.replace('ESERCIZI',stringone)

with open(f'{NOME_OUT}.tex', "w") as t_out:
	t_out.write(template)
print()
if flag_compila:
	subprocess.run(["pdflatex",NOME_OUT],stdout=subprocess.DEVNULL)
	#subprocess.run(["pdflatex",NOME_OUT])
	subprocess.run(["rm", f'{NOME_OUT}.aux'])
	subprocess.run(["rm", f'{NOME_OUT}.log'])
	subprocess.run(["rm", f'{NOME_OUT}.toc'])
	subprocess.run(["rm", f'{NOME_OUT}.out'])
