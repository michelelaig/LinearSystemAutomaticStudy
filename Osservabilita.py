from aux import l,add_columns,crea_T_inv,partizione_matrice,append_down
from aux import sempl_span
from sympy import Matrix
from sympy import pprint
###Stringhe studio Osservabilità

str_rango = "\nO ha rango $ %s $ quindi il suo nucleo ha dimensione $ %s $.\n"
str_I =		"\nCalcolando trovo \[ \nI = ker(O) = %s\]\n"
str_T_inv=	"\nE $T^{-1}$ viene \[ \nT^{-1} = %s \]\n"
equaz2 =	"\[ \n%s = %s \]"
str_3 =		"Calcoliamo allora le matrici del sistema, e vedremo che risultano partizionate come avevamo previsto:\n"
equaz3 =	"\[ \n%s = %s = %s \]\n"
equaz4 =	"\[ \n%s = %s = %s = %s \]\n"
equaz5 =	"\[ \n%s = %s = %s = %s = %s \]\n"


def crea_O(C:Matrix,A:Matrix):
	O = C	
	for i in range(1,A.rows):
		O = O.col_join(C*(A**i))

	return O 





	

def stringa_oss(A11,A22):
	inoss = "".join(l(val)+ "\ " for val in A11.eigenvals())
	oss = "".join(l(val)+"\ " for val in A22.eigenvals())
	return (
		"Quindi infine mi viene che gli autovalori osservabili sono $ %s $ e gli inosservabili sono $ %s $.\n"
		% (oss, inoss)
	)

def studioOsservabilita(A,C):
	out="\nStudiamone l'osservabilità. Calcoliamo allora $O$ e troviamo $\mathfrak{I} = \\text{ker}(O)$:\n"
	
	O = crea_O(C,A)
	det = 999 if O.cols-O.rows else O.det()

	out += "\[\n O = \\begin{pmatrix}C \\\\ ... \\\\ CA^{n-1}  \end{pmatrix} = %s, |O| = %s \]\n"%(l(O),det)

	if O.rank()==O.cols:#era con le righe
		return out+"$O$ ha rango pieno quindi finisco qui.\n",[]
	
	rango = O.rank()
	m = O.rows-rango
	out += str_rango%(l(rango),l(m))
	I = O.nullspace()
	I = sempl_span(I)




	out +=str_I%(l(I))

	
	if not len(I):
		out +="Eccezione 2: I è vuota"
		return out,I
	



	T_inv = crea_T_inv(I,A.cols)	
	out += str_T_inv%(l(T_inv))
	#print(T_inv)
	T = T_inv**-1

	out += equaz2%("T",l(T))
	out += str_3
	Atilde = T*A*T_inv
	out += equaz4%("\overset{\sim}{A}","T A  T^{-1}",(l(T)+l(A)+l(T_inv)),l(T*A*T_inv))
	out += equaz5%("\overset{\sim}{C}","CT^{-1}",l(C)+l(T_inv),l(C*T_inv),"( 0\ \ \overset{\sim}{C}_2)")
	A11,A12,A22 = partizione_matrice(Atilde,m)
	out += "Con le matrici \[ A_{11} = %s , A_{22} = %s \]"%(l(A11),l(A22))
	
	out += stringa_oss(A11,A22)



	return out, I
