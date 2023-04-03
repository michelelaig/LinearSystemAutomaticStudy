
from sympy import solve,symbols,latex,Matrix,eye,simplify
from sympy import im,re
from aux import l,vecreale,str_autovec_r,EDT,torna_ao,pt,ppt
from sympy import pprint
from aux import add_columns
###Stringhe prescritte###
consegna = "Si studi la risposta libera di un sistema che ha le seguenti caratteristiche: \[A = %s\]\n"
autva_r = "\nGli autovalori reali sono $\lambda_i = %s$"
autva_c = ", i complessi sono $\lambda_i = %s$.\n"
autve_r = "\nGli autovettori associati ai reali sono $ u_i: [  %s ]$\n"
autve_c = "\nGli autovettori associati ai complessi sono $ u_a = %s, u_b = %s$"
U_V_str = "\nDa cui posso ricavare le matrici \[U=T^{-1} = %s, V = T = %s\]"
D_str   = "\nChe mi trasformano la matrice in \[ D = TAT^{-1} = %s \]"
ao_str  = "\nCon $\\alpha = %s, \omega =%s $\n"
eDT_str = "\nDa cui posso ricavare: \[ \Phi(t) = e^{At} = T^{-1} e^{Dt} T =  T^{-1} %s T\]\n"
eAT_str = "\n\[ = %s \]"

def vecs_ab(vecs):
	#Dato che le dimensioni sono 2 o 3, ci saranno sempre max 2 autovec complessi
	if not len(vecs):
		return []
	v = vecs[list(vecs.keys())[0]][1][0]
	if v.rows==2:
		u_a = Matrix([re(v[0]),re(v[1])])
		u_b = Matrix([im(v[0]),im(v[1])])
		#print('ciao')
		
	else:
		u_a = Matrix([re(v[0]),re(v[1]),re(v[2])])
		u_b = Matrix([im(v[0]),im(v[1]),im(v[2])])
	
	return [u_a,u_b]

def autocose(A : Matrix):
	#ritorna le autovalorivettori
	vecst = A.eigenvects()
	#pprint(vecst)
	#pprint(vecst)
	vals_r = []
	vals_i = []
	vecs_r = {}
	vecs_i = {}
	for v in vecst:
		vec = v[2][0]
		if vecreale(vec):
			vals_r.append(v[0])
			vecs_r[v[0]] = [v[1],v[2]]
		else:
			vals_i.append(v[0])
			vecs_i[v[0]] = [v[1],v[2]]

	vals_i.reverse()#Per mettere prima l'autovalore con im(lambda)>0
	vecs_t = {v: [vecs_i[v][0],vecs_i[v][1]] for v in vals_i}
	vecs_i = vecs_t
	return list(vecs_r.keys()),vals_i,vecs_r,vecs_i

def generaU(A,dim,vecs_r,vecs_i):
	#Ritorna la matrice degli autovettori sinistri e alpha, omega se ci sono
	if not len(vecs_i) or A.cols >= 4:
		#Caso in cui non ci sono vettori complessi, sympy mi trova direttamente la matrice di
		#trasformazione
		return A.jordan_form()[0],[]
	#pprint(vecs_i)
	U = Matrix()
	for v in vecs_r:
		U = add_columns(U,vecs_r[v][1])
	n_vecs_r = U.cols
	i = n_vecs_r
	uab = []
	if i != dim:
		uab = vecs_ab(vecs_i)
		if not len(uab):
			return "ERRORE NON GESTITO",[]
		for v in uab:
			U = U.col_insert(i,v)
			i+=1
	return U,uab

def stringa_autovalori_complessi(vals_i):
	#se ci sono autovalori complessi ritorna la lista latexizzata, altrimenti il fine riga
	return autva_c%l(vals_i) if len(vals_i) else ".\n"

def stringa_autovettori_complessi(uab):
	#se ci sono autovecs complessi ritorna la lista latexizzata, altrimenti nulla.
	return autve_c%(l(uab[0]),l(uab[1])) if len(uab) else ".\n"

def stringa_procedimento_Jordan(A):
	return (
		""
		if A.is_diagonalizable()
		else "La matrice $A$ non è diagonalizzabile, quindi devo fare Jordan.\n"
	)



def evoluzioneLibera(eAt,x_0):
	return "L'evoluzione libera  a partire dallo stato $ %s $ è \[ x_L = (\sum_{i=0}^{i=n} e^{\lambda_i t}u_i v_i)x_0=\Phi(t) \cdot x_0 = %s \]\n"%(l(x_0),l(eAt*x_0)),eAt*x_0

def evoluzioneForzata(eAt,B,u):
	return "L'evoluzione forzata con $u = %s$ è \[ x_F = \Phi(t) * B u = %s u = %s \]\n"%(l(u),l(eAt*B),l(eAt*B*u)),eAt*B

def rispostaLibera(x_L: Matrix,C :Matrix):
	y_L = C*x_L
	return "La risposta libera è \[ y_L = \Psi(t) x_0 = %s \]\n"%l(y_L),y_L

def rispostaForzata(x_F,C,D,u):
	#pprint(C*x_F)
	#pprint(D)
	#pprint(C*x_F+D)

	return "La risposta forzata è \[ y_F = (C \Phi(t) B + D)u  = (%s+%s) \cdot u = %s\]\n"%(l(C*x_F),l(D),l((C*x_F+D)*u)),C*x_F+D

def risposta(y_L,y_F,u):
	return "La risposta totale è \[ y = y_L + y_F = %s + %s u = %s\]\n"%(l(y_L),l(y_F),l(y_L+y_F*u)),0


def studioTempoContinuo(A : Matrix,B: Matrix,C: Matrix,D_s: Matrix,X_0: Matrix,u,test):
	#ppt(test,A)
	lambda_ = symbols("lambda")
	out = consegna%(l(A))
	out+="Il determinante di $A-\lambda$ è $ %s $.\n"%l((A-lambda_*eye(A.rows)).det())
	vals_r,vals_i,vecs_r,vecs_i = autocose(A)


	out += autva_r%(vals_r)
	#pprint(x_0)	
	#pt(test,"autovalori reali: "+str(vals_r))
	
	out += stringa_autovalori_complessi(vals_i)

	str_aut_r = str_autovec_r(vecs_r)
	out += autve_r%str_aut_r#I reali ci stanno sempre tanto(?)

	if str_aut_r=="ERRORE":
		return out 
	
	U,uab = generaU(A,A.rows,vecs_r,vecs_i)	#T-1
	if U=="ERRORE NON GESTITO":
		return out + "\nErrore molteciplità algebrica e geometrica diverse.\n",False
	
	out += stringa_autovettori_complessi(uab)

	out += stringa_procedimento_Jordan(A)

	#Variabili ausiliarie
	V = U**-1
	T,T_1 = V,U
	D = T*A*T_1
	
	out+= U_V_str%(l(U),l(V))
	out+=D_str%(l(D))
	
	ao = []
	if len(vals_i) and A.cols <4:
		ao = torna_ao(D)#[alpha,omega]
		out+=ao_str%(l(ao[0]),l(ao[1]))

	#if not A.is_diagonalizable():
	#	return out + "e non è diagonalizzabile",False
	
	eDt = EDT(D,D.cols,vecs_r,ao)	
	out += eDT_str%l(eDt)
	eAt = T_1 * eDt * T
	out += eAT_str%l(eAt)
	for x_0 in X_0:
		s, x_L = evoluzioneLibera(eAt,x_0)
		out += s
		s,y_L = rispostaLibera(x_L,C)
		out += s

	out+="\subsubsection{Osservabilità}\n I modi naturali osservabili sono quelli tali che \n\[ C \cdot u_i   \\neq 0\]\n"
	out+="\subsubsection{Eccitabilità}\n I modi naturali eccitabili sono quelli tali che \n\[v_i' \cdot B \\neq 0\]\n"


	return out,True
	
