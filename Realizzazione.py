from aux import coeffs,l
from sympy import pprint,Matrix,eye,Rational
from sympy.abc import s





def vettore(n):
	out = Matrix()
	for i in range(n):
		out = out.row_insert(out.rows,Matrix([0]))
	return out

def riga(n):
	out = Matrix()
	for i in range(n):
		out = out.col_insert(out.cols,Matrix([0]))
	return out

def coefficienti_bene(Nw_,Dw_):
	Nw = []
	Dw = []
	#print(len(Nw_))
	#print(len(Dw_))
	if len(Nw_)<len(Dw_)-1:
		#print("ok")
		for b in range(len(Dw_)-len(Nw_)-1):
			#print("b")
			Nw = [0]+Nw
			#print(Nw)
	if Dw_[0]!=1:
		tmp = Dw_[0]
		for el in Nw_:
			Nw.append(el*tmp)
			#print(Nw)
		for el in Dw_:
			Dw.append(Rational(el,tmp))
		return Nw,Dw
	return Nw+Nw_,Dw_

def A_can_ragg(Dw):
	n = len(Dw)-1
	v1 = vettore(n)
	A = eye(n)
	A.col_del(n-1)
	A = v1.row_join(A)
	A=A.tolist()
	bs = []
	for b in Dw[::-1][0:-1]:
		bs.append(-b)
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
	A = A_can_ragg(Dw).transpose()
	B = Matrix(Nw[::-1])
	C = riga(A.cols-1).col_insert(A.cols,Matrix([1]))
	return A,B,C


def realizzazione(W):
	out = ""
	Nw = W[0]
	Dw = W[1]

	if Nw.rows==1 and Nw.cols==1:
		for nw in Nw:
			nw = coeffs(nw)
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



#W = [Matrix([(s**2-1)]),((s+1)*(s**2+4*s+5))]

#realizzazione(W)
