from aux import coeffs,l,Matr_colonne,Matr_righe
from sympy import pprint,Matrix,eye,Rational,degree,zeros
from sympy.abc import s





def vettore(n):
	out = Matrix()
	for _ in range(n):
		out = out.row_insert(out.rows,Matrix([0]))
	return out

def riga(n):
	out = Matrix()
	for _ in range(n):
		out = out.col_insert(out.cols,Matrix([0]))
	return out

def coefficienti_bene(Nw_,Dw_):
	Nw = []
	#print(len(Nw_))
	#print(len(Dw_))
	if len(Nw_)<len(Dw_)-1:
		#print("ok")
		for _ in range(len(Dw_)-len(Nw_)-1):
			#print("b")
			Nw = [0]+Nw
	if Dw_[0]!=1:
		tmp = Dw_[0]
		for el in Nw_:
			Nw.append(el*tmp)
			#print(Nw)
		Dw = [Rational(el,tmp) for el in Dw_]
		return Nw,Dw
	return Nw+Nw_,Dw_

def A_can_ragg(Dw):
	n = len(Dw)-1
	v1 = vettore(n)
	A = eye(n)
	A.col_del(n-1)
	A = v1.row_join(A)
	A=A.tolist()
	bs = [-b for b in Dw[::-1][:-1]]
	A[n-1]=bs

	return Matrix(A)

def forma_can_ragg(Nw,Dw):
	Nw,Dw = coefficienti_bene(Nw,Dw)

	A = A_can_ragg(Dw)
	B = vettore(A.cols-1).row_insert(A.cols,Matrix([1]))
	C = Matrix([Nw[::-1]])

	return A,B,C

def forma_can_oss(Nw,Dw):
	Nw,Dw = coefficienti_bene(Nw,Dw)
	A = A_can_ragg(Dw).transpose()#nn va bene
	B = Matrix(Nw[::-1])
	C = riga(A.cols-1).col_insert(A.cols,Matrix([1]))
	return A,B,C

def better_can_ragg(q,p,matrici,Dw):

	n = degree(Dw,s)
	
	l = []
	for i in range(n-1):
		l.append(Matr_colonne([eye(p) if j==i+1 else zeros(p,p) for j in range(n)]))
	sopra = Matr_righe(l)

	sotto = Matr_colonne([eye(p)*(-c) for c in coeffs(Dw)[1::][::-1]])

	Ar = Matr_righe([sopra,sotto])

	Br = Matr_righe([zeros(p,p)*(n-1)]+[eye(p)])

	Cr = Matr_colonne([matrici[i] for i in matrici])
	return Ar,Br,Cr



def realizzazione(W):
	out = ""
	Nw,Dw = W[:2]
	q,p = Nw.shape
	print(f"q: {q},p: {p}")

	'''
	if Nw.shape==(1,1):
					
		nw = coeffs(Nw[0])
		dw = coeffs(Dw)

		Ar,Br,Cr =  forma_can_ragg(nw,dw)
		Ao,Bo,Co =  forma_can_oss(nw,dw)
	
		out = "\[ W(s) = \\frac{%s}{%s} \]\n"%(str(nw),str(dw))
		out+= "\subsubsection{Forma Canonica Raggiungibile}\n"
		out+= "Con la realizzazione cano ragg viene \[ A = %s, B = %s, C= %s \]\n"%(l(Ar),l(Br),l(Cr))
		out += "\[ W(s) = %s \n\]"%l(Cr*((s*eye(Ar.cols)-Ar)**-1)*Br)
		out+= "\subsubsection{Forma Canonica Osservabile}\n"
		out+= "Con la realizzazione cano oss viene \[ A = %s, B = %s, C= %s \]\n"%(l(Ao),l(Bo),l(Co))
		out += "\[ W(s) = %s \n\]"%l(Co*((s*eye(Ao.cols)-Ao)**-1)*Bo)
	
		return out,[Ar,Br,Cr],[Ao,Bo,Co]
	'''
	

	matrici = {d : zeros(q,p) for d in range(degree(Dw))}
	for i in range(q*p):
		c = coeffs(Nw[i])[::-1]
		for deg in range(len(c)):
			matrici[deg][i] = c[deg]
	Ar,Br,Cr = better_can_ragg(q,p,matrici,Dw)


	#Ao,Bo,Co =  forma_can_oss(nw,dw)

	out = "\[ W(s) = \\frac{%s}{%s} \]\n"%(l(Nw),l(Dw))
	out+= "\subsubsection{Forma Canonica Raggiungibile}\n"
	out+= "Con la realizzazione cano ragg viene \[ A = %s, B = %s, C= %s \]\n"%(l(Ar),l(Br),l(Cr))
	#out += "\[ W(s) = %s \n\]"%l(Cr*((s*eye(Ar.cols)-Ar)**-1)*Br)
	#out+= "\subsubsection{Forma Canonica Osservabile}\n"
	#out+= "Con la realizzazione cano oss viene \[ A = %s, B = %s, C= %s \]\n"%(l(Ao),l(Bo),l(Co))
	#out += "\[ W(s) = %s \n\]"%l(Co*((s*eye(Ao.cols)-Ao)**-1)*Bo)

	return out,[Ar,Br,Cr],[]#[Ao,Bo,Co]


	#return "ValueError"

#W = [Matrix([s**2+1]),(s**2)*((s+1)**2)]
#W = [Matrix([(s**2-1)]),((s+1)*(s**2+4*s+5))]
#W = [Matrix([[s+1],[2]]),s*(s+1)]
W = [Matrix([[s,0,1],[1,s+1,0]]),s**2+1]
realizzazione(W)
