from sympy import Matrix,pprint,eye,pretty
from aux import add_columns,crea_T_inv_Chi,Chi4,pt
from aux import l,lin_ind_3,intersezione_spazi_vettoriali,concatena_matrici_orizzontalmente

from sympy.abc import t


_1_str = "La matrice dei vettori di base di I e R è \[ \chi_1 =  %s \]"
_2_str = "\nDa qui costruiamo la matrice \[ T^{-1} = %s \]"
_3 = "E quindi la matrice \[ T = %s \]"
t_flag_ = [False]

def int_matr(I,R):
	return intersezione_spazi_vettoriali(I,R)

def check_int(M):
	if M.cols>M.rows:
		return "\nERRORE ci sono più colonne che righe wtf.\n",1
	if M.rows > M.cols:
		return "\nCi sono più righe che colonne quindi sicuro l'intersezione c'è.\n",0
	return "Ed il determinante è ininfluente.",0



def crea_T_inv(X1,X2,X3,X4):
	if len(X1) == 0 :
		M = Matrix()
	else:
		M = add_columns(X1[0],X1[0::])
	M = add_columns(M,X2)
	M = add_columns(M,X3)
	M = add_columns(M,X4)
	return M

def Chi(dim,X,C,i):
	#La funzione deve ritornare la matrice composta dai vettori da aggiungere a X per creare C.
	#Se X non c'è torno C
	if X.rows==0:
		return concatena_matrici_orizzontalmente(C)
	#Se X è già al massimo delle dimensioni torno la matrice vuota
	if X.cols==dim:
		return Matrix()
	out = Matrix()
	for v in C:
		#Se v è lin indip coi vettori di X, lo aggiungo alla matrice da ritornare
		if X.rank()<X.row_join(v).rank():
			X = X.row_join(v)
			out = out.row_join(v)
	pt(get_test(),pretty(out))
	return out

intro_sottospazi = "I miei sottospazi di riferimento sono:	\[ \mathfrak{I} = %s, \mathfrak{R} = %s \]\n"
chi2_str = "\n\paragraph{Per quanto riguarda Chi2:} $ \chi_2 | \chi_2 \oplus \chi_1 = \mathfrak{R} $ è \[ \chi_2 = %s \]\n"
chi3_str = "\n\paragraph{Per quanto riguarda Chi3:} $ \chi_3 | \chi_3 \oplus \chi_1 = \mathfrak{I} $ è \[ \chi_3 = %s \]\n"
chi4_str = "\n\paragraph{Per quanto riguarda Chi4:} $ \chi_4 | \chi_1 \oplus \chi_2 \oplus  \chi_3 \oplus \chi_4 = \mathbb{R} $ è \[ \chi_4 = %s \]\n"
T_inv_str= "\paragraph{Ora facciamo T inversa:} \[ T^{-1} = (\chi_1\ \chi_2\ \chi_3\ \chi_4\ ) = %s \]\n"
T_str = "e quindi \[T = %s\]"
Atild_str = "\n\[ \widetilde{A} = TAT^{-1} = %s * T^{-1} = T*%s =%s \]\n"
Btild_str = "\n\[ \widetilde{B} = T B = %s \]\n"
Ctild_str = "\n\[ \widetilde{C} = C T^{-1} = %s \]\n"


def set_flag(test):
	t_flag_[0] = test

def get_test():
	return t_flag_[0]

def scomposizioneKalman(A,B,C,I,R,test):
	set_flag(test)	
		
	out = intro_sottospazi%(l(I),l(R))
	X1 = int_matr(I,R)
	#pprint(X1)
	out += _1_str%l(X1)
	s,check =  check_int(X1)
	out+=	s
	if check:
		return out
	
	X2 = Chi(A.rows,X1,R,2)
	#pprint(X2)

	if X2=="errore x2":
		out+=X2
		return out
	
	out += chi2_str%l(X2)

	X3 = Chi(A.rows,X1,I,3)

	if X3=="errore x3":
		out+=X3
		return out
	out += chi3_str%l(X3)
	#pprint(X3)
	
	X123 = concatena_matrici_orizzontalmente([X1,X2,X3])
	#pprint(X123)
	#print(X123.rank())
	X4 = Chi4(A.cols,X123)
	if X4=="errore x4":
		out+=X4
		return out

	out+= chi4_str%l(X4)


		
	T_inv = crea_T_inv_Chi(X1,X2,X3,X4)
	out+=T_inv_str%l(T_inv)
	#pt(test,"T_inv"+str(T_inv))
	T= T_inv**-1
	out+=T_str%l(T)
	A_ = T*A*T_inv
	B_ = T*B
	C_ = C*T_inv
	out+= Atild_str%(l(T*A),l(A*T_inv),l(A_))
	out+= Btild_str%l(B_)
	out+= Ctild_str%l(C_)

	out += "\[Phi(t) = %s \]\n"%l((A_*t).exp())
	
	return out
