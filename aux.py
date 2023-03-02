from sympy import latex,im,Matrix,pprint,eye
from sympy import E,cos,sin,Heaviside,DiracDelta,simplify

from sympy.core import numbers,Rational,Integer,Mul
from sympy.abc import t,s
from sympy.integrals import laplace_transform,inverse_laplace_transform



from lcapy import expr
from lcapy.discretetime import z

from math import gcd
from typing import List

lin_ind_3 = [Matrix([1,0,0]),Matrix([0,1,0]),Matrix([0,0,1])]


tipi_prim = [int,float,numbers.One,numbers.Zero,Rational,Integer,numbers.NegativeOne]



def discretizza(ydFn_str):
	e = expr(ydFn_str)
	if e==0:
		return 0
	return e.discrete_time()

def trasforma_in_Zeta(yFn):
	if type(yFn) is int and yFn == 0:
		return 0
	return yFn.ZT()

def da_t_a_z(f):
	if f==0:
		return 0
	if type(f) in tipi_prim:
		return f*(z/(z-1))
	#print(f)
	#print(type(f))
	f = discretizza(str(f).replace('t','n').replace('Delna','Delta')).ZT()
	return f 




def coeffs(f):
	if type(f) in tipi_prim:
		return [f]
	else:
		return f.as_poly().all_coeffs()

def Chi4(dim,X):
	#pprint(dim)
	#pprint(X)
	tmp = X
	X4 = Matrix()
	base_canonica = eye(dim).columnspace()[::-1]
	for v in base_canonica:
		if tmp.row_join(v).rank()>tmp.rank():
			tmp = tmp.row_join(v)
			X4 = X4.row_join(v)
	return X4



def shorter(espressione):
	if len(str(espressione))<10:
		return espressione
	e = espressione.expand()
	f = espressione.simplify()
	if len(str(e))<=len(str(f)):
		return e
	else:
		return f




def pt(t,s):
	if t:
		print(s)

def ppt(t,s):
	if t:
		print(s)




def l(s):
	return latex(s,mat_delim="(")



def L(f):
	if type(f)==Mul:
		#print(type(f.args[0]))
		if type(f.args[0]) in tipi_prim:	
			return f.args[0]* laplace_transform(f/f.args[0], t, s, noconds=True)
	return laplace_transform(f, t, s, noconds=True)	





def invL(F):
	out = inverse_laplace_transform(F,s,t)
	#print(out)
	return out



def Matr_colonne(l):
	out = Matrix()
	for v in l:
		out = out.row_join(Matrix(v))
	return out

def concatena_matrici_orizzontalmente(L):
	# Inizializziamo una matrice vuota
	result = Matrix()

	# Per ogni matrice M nella lista L
	for M in L:
		# Concateniamo M orizzontalmente alla matrice risultato
		if M.rows!=0:
			result = result.row_join(Matrix(M))

	# Ritorniamo la matrice risultato
	return result

def Zassenhaus(s1,s2):
	if not len(s1) or not len(s2):
		return []
	s1m = Matr_colonne(s1)
	s2m = Matr_colonne(s2)

	tmp = s2m.T.row_join(Matrix([[0 for i in range(s2m.cols)] for j in range(s2m.rows)]).T)
	tmp = s1m.T.row_join(s1m.T).col_join(tmp).echelon_form()
	#pprint(tmp)
	#pprint(tmp.T.columnspace())
	out = []
	for v in tmp.T.columnspace():
		flag_int = True
		for x in range(s1m.rows):
			if v[x]!=0:
				flag_int = False
		if flag_int:
			#print(v)
			out.append(Matrix(v[s1m.rows::]))
	out = sempl_span(out)
	return out

def intersezione_spazi_vettoriali(I, R):
	return Matr_colonne(Zassenhaus(I,R))




def add_columns(M,C):
	out = M
	for col in C:
		out = out.col_insert(out.cols,col)
	return out

def add_rows(M,R):
	out = M
	for row in R:
		out = out.row_insert(out.rows,row)
	return out

def append_down(M,R):
	out = M
	for r in R:
		for i in range(r.rows):
			out = add_rows(out,[Matrix(r.row(i))])
	return out


def torna_ao(D):
	#pprint(D)
	if D.cols==3:
		a = D.columnspace()[1][1]
		o = -D.columnspace()[1][2]
	if D.cols==2:
		a = D.columnspace()[0][0]
		o = -D.columnspace()[0][1]
	return [a,o]

def vecreale(v):
	for el in v:
		#print(el)
		if im(el)!=0:
			return False
	return True

def str_autovec_r(vec_r) -> str:
	#pprint(vec_r)
	out = ""
	for v in vec_r:
		'''
		if vec_r[v][0]!=1:
			s = ""
			for vmult in vec_r[v][1]:
				s += l(vmult)+", "
			s = s[0:-2]
			out += "%s :\left( %s \\right) "%(l(v),s)
		else:
			out += "%s : %s "%(l(v),l(vec_r[v][1][0]))
		'''
		#DATESTARE
		if vec_r[v][0] != 1:
			s = ", ".join(l(vmult) for vmult in vec_r[v][1])
			out += "%s: (%s)" % (l(v), s)
		else:
			out += "%s: %s" % (l(v), l(vec_r[v][1][0]))
	return out

def EDT(D:Matrix,dim,vecs_r,ao)->Matrix:
	if not ao or dim!=3:
		return simplify((D*t).exp())
	out = Matrix()
	if dim==3:
		a,o = ao
		out = Matrix([
			[E**(list(vecs_r.keys())[0] * t), 0, 0],
			[0, E**(a * t) * cos(o * t), -E**(a * t) * sin(o * t)],
			[0, E**(a * t) * sin(o * t), E**(a * t) * cos(o * t)]
		])
	
	return out




def crea_T_inv_Chi(X1:Matrix,X2:Matrix,X3:Matrix,X4:Matrix)->Matrix:
	tmp = add_columns(Matrix(),X1.columnspace()+X2.columnspace()+X3.columnspace()+X4.columnspace())
	return tmp

def crea_T_inv(I,n):
	#Per ora metto quelli che so essere lin indip per come è fatta la matrice
	if not I:
		return eye(n)
	#n_gia_presenti = len(I)
	#identita = eye(n).columnspace()
	#prima_parte = identita[n_gia_presenti::]	
	#seconda_parte = identita[:n_gia_presenti]
	#identita = prima_parte+seconda_parte
	identita = eye(n).columnspace()[len(I):] + eye(n).columnspace()[:len(I)]

	out = Matr_colonne(I)
	for c in identita:
		#out = max(out.row_join(c), key=lambda x: x.rank())
		tmp = out.row_join(c)
		if tmp.rank()>out.rank():
			out = tmp
		if out.is_square:
			break
	return out



def mcd(v):
	den = v[0]
	for i in v:
		den = gcd(den,i)
	return den
			

def sempl_span(I):
	if not len(I):
		return I
	den = 1
	for v in I:
		for n in v:
			if n.is_Rational:
				den = n.denominator
				break
	#if den==1:
	#	return I
	out = []
	for v in I:
		new_vec = Matrix([old*den for old in v])
		out.append(new_vec)
	if den!=1:
		return out
	out = []
	for v in I:
		den = mcd(v)
		new_vec =Matrix([Rational(old,den) for old in v])
		out.append(new_vec )
	
	return out

def gradino(a):
	return Heaviside(a)
def impulso(a):
	return DiracDelta(a)
def partizione_matrice(Atilde,m):
	A11 = Atilde[0:m,0:m]
	A12 = Matrix()
	A22 = Atilde[m:,m:]

	return A11,A12,A22
