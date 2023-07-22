from aux import l,invL,shorter,impulso,vecreale
from random import choice


from lcapy import difference_equation,expr,nexpr
from lcapy import latex as llatex
from lcapy import simplify as lsimplify
from lcapy.discretetime import z

from sympy import simplify,Rational,eye, factor,Matrix,pprint
from sympy import E
from sympy.abc import s,k,t

iniz_string = "\nLa funzione è \[ W(s) = \\frac{%s}{%s} \]\n\n"

s2 = "Per trovare $W(z)$ passo da $y_F(t)$:\n\[y_F(t) = \mathcal{L}^{-1}\left[ W(s)\\frac{1}{s}\\right]"
s3 = "\n = \mathcal{L}^{-1}\left[ \\frac{%s}{%s}\\frac{1}{s}\\right]\n = %s \]"

s4 = "Ora calcolo, $y_{dF}(k)$, ovvero $y_{dF}(kT_c)$ (Prendendo $T_c =1$):\n"
s5 = "\[ y_{dF}(k) =\left.\left[ %s \\right]\\right|_{t=kT_c}= %s  \]\n"
s6 = "Trasformo in z l'uscita ottenuta: \[[ \\mathcal{Z}\left[y_F(kT_c)\\right] = \\mathcal{Z}\left[ %s \\right] = \]\n\[ =  %s \]\n"
#s6 = "Trasformo in z l'uscita ottenuta: \[[ \\mathcal{Z}\left[y_F(kT_c)\\right] = \\mathcal{Z}\left[ %s \\right] = \]\n"
s7 = "Infine moltiplico per $\\frac{z-1}{z}$ per ottenere $W(z)$: \n\[ W(z) = %s \\frac{z-1}{z} =\]\n\[= %s \]\n"

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

	return out


def discretizzazioneCompleta(sistema):
	A,B,C,D,u_t,x_0 = sistema.get_dati()

	vals_r,vals_i,vecs_r,vecs_i = autocose(A)
	U,uab = generaU(A,A.rows,vecs_r,vecs_i)	#T-1
	V = U**-1
	T,T_1 = V,U
	D = T*A*T_1

	out = f"\[ {l(U*D.exp()*V)}\]"


	'''
	Phi_inv = (s*eye(A.cols)-A)
	P_d = factor(Phi_inv.det())
	Phi_num = simplify((Phi_inv**-1)*P_d)
	H_num = simplify(Phi_num*B)
	pprint(simplify(C*H_num))
	pprint(D*P_d)
	W_num = simplify(C*H_num)+(D*P_d)
	out += discretizzazioneDaW([W_num,P_d])
	'''
	return out