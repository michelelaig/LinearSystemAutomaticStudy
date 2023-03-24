from aux import l,add_columns,crea_T_inv,partizione_matrice,append_down
from aux import sempl_span
from sympy import Matrix
from sympy import pprint
###Stringhe studio Osservabilità
str_sist = "Il sistema è \[ \\begin{cases} \overset{\cdot}{x}= %s x+ %s u\\\\y = %s x\end{cases}\]\n"
str_1 = "\nStudiamone l’osservabilità. Calcoliamo allora O e troviamo I = ker(O):\n"
str_2 = "\[\n O = \\begin{pmatrix}C \\\\ CA \\\\ CA^2 \end{pmatrix} = %s, |O| = %s \]\n"
str_no_inoss = "O ha rango pieno quindi finisco qui.\n"
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
	'''
	if A.rows==4:
		O = append_down(C,[C*A,C*A*A,C*A*A*A])
	if A.rows==3:
		O = append_down(C,[C*A,C*A*A])
	if A.rows==2:
		O = append_down(C,[C*A])
	'''
	return O 





	

def stringa_oss(A11,A22):
	oss = ""
	inoss = ""
	for val in A11.eigenvals():
		inoss+=l(val)+ "\ "
	for val in A22.eigenvals():
		oss+=l(val)+"\ "
	out = "Quindi infine mi viene che gli autovalori osservabili sono $ %s $ e gli inosservabili sono $ %s $.\n"%(oss,inoss)
	return out




	
		

def studioOsservabilita(A,C):
	out=str_1
	O = crea_O(C,A)
	if O.cols == O.rows:
		out+=str_2%(l(O),l(O.det()))
	else:
		out+=str_2%(l(O),l(999))
	if O.rank()==O.rows:
		out += "Eccezione 1: "+str_no_inoss
		return out,[]
	
	rango = O.rank()
	m = O.rows-rango
	out += str_rango%(l(rango),l(m))
	I = O.nullspace()
	I = sempl_span(I)




	out +=str_I%(l(I))
	if not len(I):
		out +="2"+str_no_inoss
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
