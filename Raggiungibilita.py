from aux import l,add_columns,crea_T_inv,partizione_matrice,sempl_span
from sympy import pprint


str_R = "Ora per studiare la raggiungibilità degli stati calcolo $R = (B\ AB\ ...\ A^{n-1}B)$: \[ R = %s, |R| = %s \] \n"

str_R_rango_0 = "\nR ha rango 0, quindi non ci sono vettori raggiungibili. Finisco qui.\n"
R_rango = "\nVediamo che $rango(R) = %s$ e quindi : \[ \mathfrak{R} = %s \]\n"

R__str = "\nTutti gli stati che hanno questa struttura sono, allora, raggiungibili. Mettiamo in evidenza questa struttura;\n"
R__str_1 = "cambiamo base, e vorremmo avere lo stato espresso come $z = Tx$ tale che, se x è uno stato raggiungibile, allora: \[ z_R = T x_R = \\begin{pmatrix} \star  \\\\ 0 \\\\0\end{pmatrix}\]\n"
A11A22str =  "Con le matrici \[ \overset{\sim}{A}_{11} = %s , \overset{\sim}{A}_{22} = %s  \]"
BTstr = "e le matrici \[ \overset{\sim}{B} = TB = %s  \]\n"
str_T_inv=	"\nE $T^{-1}$ viene \[ T^{-1} = %s \Longrightarrow T = %s \]\n"
formulaRagg = "Ora ne calcoliamo la raggiungibilità: \[ \overset{\sim}{H}(t) = e^{\overset{\sim}{A}t}\overset{\sim}{B} = \\begin{pmatrix} e^{\overset{\sim}{A}_{11}t} &  \star \\\\ 0 & e^{\overset{\sim}{A}_{22}t} \end{pmatrix} \\begin{pmatrix} \overset{\sim}{B}_1 \\\\ 0 \end{pmatrix} = \\begin{pmatrix} e^{\overset{\sim}{A_{11}t}}\overset{\sim}{B_1} \\\\ 0 \end{pmatrix} \]\n"

equaz4 =	"\[ %s = %s = %s = %s \]"


def crea_R(A,B):
	R= B
	tmp = B
	for _ in range(A.cols-1):
		tmp = A*tmp
		R = add_columns(R,[tmp])
	return R

def stringa_ragg(A11,A22):
	ragg = "".join(f"{l(val)}, " for val in A11.eigenvals())
	irrag = "".join(f"{l(val)}, " for val in A22.eigenvals())
	return f"Quindi infine mi viene che gli autovalori ragg sono $ {ragg} $ e gli irrag sono $ {irrag} $"

def studioRaggiungibilita(A,B):
	out =""
	R = crea_R(A,B)
	if R.cols==R.rows:
		out += str_R%(l(R),l(R.det()))
	else:
		out += str_R%(l(R),l(999))

	rango = R.rank()
	m = rango
	if rango==0:
		out+= str_R_rango_0
	R_ = R.columnspace()
	R_ = sempl_span(R_)
	out += R_rango%(l(rango),l(R_))
	out += R__str +R__str_1
	
	T_inv = crea_T_inv(R_,A.cols)
	T = T_inv**-1

	out += str_T_inv%(l(T_inv),l(T))

	Atilde = T*A*T_inv
	Btilde = T*B
	out += equaz4%("\overset{\sim}{A}","T A  T^{-1}",(l(T)+l(A)+l(T_inv)),l(T*A*T_inv))
	#Partizione matrtice
	A11,A12,A22 = partizione_matrice(Atilde,m)
	
	out +=A11A22str%(l(A11),l(A22))
	out += BTstr%(l(Btilde))	

	out += formulaRagg
	out +=stringa_ragg(A11,A22)










	return out, R_



