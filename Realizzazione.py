from aux import coeffs,l,Matr_colonne,Matr_righe
from sympy import pprint,Matrix,eye,Rational,degree,zeros
from sympy.abc import s

def better_can_ragg(q,p,matrici,Dw):

	n = degree(Dw,s)
	
	l = []
	for c in coeffs(Dw)[1::][::-1]:
		l.append(eye(p)*(-c))
	sotto = Matr_colonne(l)

	l = []
	for i in range(n-1):
		l_riga = []
		for j in range(n):
			if j==i+1:
				l_riga.append(eye(p))
			else:
				l_riga.append(zeros(p,p))
		l.append(Matr_colonne(l_riga))

	sopra = Matr_righe(l)
	Ar = Matr_righe([sopra,sotto])


	Br = Matr_righe([zeros(p,p)*(n-1)]+[eye(p)])

	Cr = Matr_colonne([matrici[i] for i in matrici])
	return Ar,Br,Cr

def better_can_oss(q,p,matrici,Dw):
	n = degree(Dw,s)
	l = []
	for c in coeffs(Dw)[1::][::-1]:
		l.append(eye(q)*(-c))
	destra = Matr_righe(l)

	l = []
	for i in range(n-1):
		l_col = []
		for j in range(n):
			if j==i+1:
				l_col.append(eye(q))
			else:
				l_col.append(zeros(q,q))
		l.append(Matr_righe(l_col))
	sinistra = Matr_colonne(l)
	Ao = Matr_colonne([sinistra,destra])
	pprint(Ao)
	Bo = Matr_righe([matrici[i] for i in matrici])
	pprint(Bo)
	Co = Matr_colonne([zeros(q,q)]+[eye(q)])
	pprint(Co)
	return Ao,Bo,Co


def realizzazione(W):
	out = ""
	Nw,Dw = W[:2]
	q,p = Nw.shape
	#print(f"q: {q},p: {p}")

	matrici = {d : zeros(q,p) for d in range(degree(Dw))}
	for i in range(q*p):
		c = coeffs(Nw[i])[::-1]
		for deg in range(len(c)):
			matrici[deg][i] = c[deg]
	
	Ar,Br,Cr = better_can_ragg(q,p,matrici,Dw)
	Ao,Bo,Co =  better_can_oss(q,p,matrici,Dw)

	out = "\[ W(s) = \\frac{%s}{%s} \]\n"%(l(Nw),l(Dw))
	out+= "\subsubsection{Forma Canonica Raggiungibile}\n"
	out+= "Con la realizzazione cano ragg viene \[ A = %s, B = %s, C= %s \]\n"%(l(Ar),l(Br),l(Cr))
	out += "\[ W(s) = %s \n\]"%l(Cr*((s*eye(Ar.cols)-Ar)**-1)*Br)
	out+= "\subsubsection{Forma Canonica Osservabile}\n"
	out+= "Con la realizzazione cano oss viene \[ A = %s, B = %s, C= %s \]\n"%(l(Ao),l(Bo),l(Co))
	out += "\[ W(s) = %s \n\]"%l(Co*((s*eye(Ao.cols)-Ao)**-1)*Bo)

	return out,[Ar,Br,Cr],[Ao,Bo,Co]



#W = [Matrix([s**2+1]),(s**2)*((s+1)**2)]
#W = [Matrix([(s**2-1)]),((s+1)*(s**2+4*s+5))]
#W = [Matrix([[s+1],[2]]),s*(s+1)]
#W = [Matrix([[s,0,1],[1,s+1,0]]),s**2+1]
#realizzazione(W)
