#!/usr/bin/python3
import sys
import subprocess

from funzioni_trasformate import crea_esercizio
from tqdm import tqdm

num_esercizi = 1

#valori = ['1','2','3']#,'e','\pi']
valori_diff = ['0','1','y_0']
valori_t_diff = ['0','1','t_0']
val_lim = ['0','+\\infty','-\\infty']


test = False
def compila_documento(tipo=None):
	stringone = ''
	i = 0
	while tqdm(i<num_esercizi):
		stringone += "\subsection{Esercizio %d}\n %s \n"%(i,crea_esercizio(i,test))
		i+=1
	return stringone


print()
print()
flag_compila=False
if len(sys.argv)>1:
	num_esercizi = int(sys.argv[1])
else:
	num_esercizi = 10
	flag_compila=True

if len(sys.argv)==3:
	flag_compila=True

NOME_TEMP = "template.tex"
NOME_OUT = "esercizio"



t= open(NOME_TEMP,"r")
template = t.read()
t.close()

stringone = compila_documento()

template = template.replace('ESERCIZI',stringone)

t_out = open(NOME_OUT+'.tex',"w")
t_out.write(template)
t_out.close()

print()
if flag_compila:
	subprocess.run(["pdflatex",NOME_OUT],stdout=subprocess.DEVNULL)
	#subprocess.run(["pdflatex",NOME_OUT])
	subprocess.run(["rm",NOME_OUT+'.aux'])
	subprocess.run(["rm",NOME_OUT+'.log'])
	subprocess.run(["rm",NOME_OUT+'.toc'])
	subprocess.run(["rm",NOME_OUT+'.out'])
