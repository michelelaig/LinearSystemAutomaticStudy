from sympy import eye,pprint,simplify,expand,factor,solve,Matrix
from sympy.abc import s,t
from sympy.core import add
from random import randint

from aux import l,L,invL,coeffs,tipi_prim

from sympy.physics.control.lti import TransferFunction as symTransFun
from sympy.physics.control.control_plots import bode_plot as symBode

#from control import tf as conTransFun
#from control import nyquist_plot as conNyquistPlot

from lcapy import expr


import matplotlib.pyplot as plt

from tqdm import tqdm


def graficiBodeUniDim(f_sym,det_sym):
	out = ''
	#pprint(f_sym)
	if f_sym == 0:
		return "Il numeratore della funzione è zero quindi niente grafici"
	f_sym = factor(simplify(f_sym))
	det_sym = factor(det_sym)
	#pprint(factor(f_sym))
	tf = symTransFun(f_sym,det_sym,s)
	plt.figure(0,clear=True)
	bode = symBode(tf,show=False)
	randid = randint(1000000,9000000)
	bode.savefig('./figures/bode_%d.png'%(randid))
	#pprint(tf)
	out+= "\[ W(s) = %s \]"%l(tf)
	out+= "\includegraphics[scale = 0.5]{figures/bode_%d.png}\n\n"%(randid)
	return out
	

def graficiNyquistUniDim(num,den):
	out = ""
	randid = randint(1000000,9000000)
	if num==[0]:
		return "Il numeratore della funzione è 0 quindi niente"
	#tfc = conTransFun(num,den)
	#nyquist = conNyquistPlot(tfc)
	#nyquist.savefig('./figures/nyquist_%d.png'%(randid))
	#print(str(num))
	tfc = expr("(%s)/(%s)"%(str(num),str(den)))
	tfc.nyquist_plot()
	plt.savefig("./figures/nyquist_%d.png"%(randid))

	out+="\includegraphics[scale = 0.5]{figures/nyquist_%d.png}"%(randid)
	out+= "nel tempo continuo è \[ %s \]"%l(invL(num/den))
	return out


def graficiBode(num,det):
	out = ""
	if num.rows>1 or num.cols>1:
		for r in num:
			out+= "\nValore $ %s $ della matrice delle funzioni di trasferimento:\n"%l(r)
			out+= graficiBodeUniDim(r,det)
	if num.rows==1 and num.cols==1:
		out+= "\nIl grafico di bode è:\n"
		out+= graficiBodeUniDim(num[0],det)
	return out

funz_caratt_1 = "\nLe funzioni caratteristiche sono \[\\begin{array}{rcl}  H(s) & = & \Phi(s)B \\\\ \Psi(s) & = & C \Phi(s)\\\\ W(s) & = & C(sI-A)^{-1}B  \end{array} \]\n"
funz_caratt_2 = "\ne quindi \[ H(s)  =  %s \ \Psi(s) = %s \]\n\[ W(s)  =  %s = %s  \] "


def f_l(N,D):
	return "\\frac{%s}{%s}"%(l(N),l(D))


def strap_type(l):
	out = []
	for i in l:
		out.append(float(i))
	return out




def graficiNyquist(num,det):
	out = ""
	if num[0]==0:
		return "No Nyquist"
	if num.rows>1 and num.cols==1:
		for r in range(num.rows):
			out+= "\nValore $ %s $ della matrice delle funzioni di trasferimento:\n"%l(r)
			#La roba dei coefficienti è obsoleta
			#num_c = strap_type(num.row(r)[0].as_poly().all_coeffs())
			#det_c = strap_type(det.as_poly().all_coeffs())
			out+= graficiNyquistUniDim(num.row(r)[0],det)
	if num.rows==1 and num.cols==1:
		#print(num)
		#print(det)
		out+= "\nIl grafico di Nyquist è:\n"
		out+= graficiNyquistUniDim(num[0],det)
	return out

def invLaplace(y_s):
	if type(y_s) in tipi_prim:
		return "\n\[ y(t) = \mathcal{L}^{-1}[y(s)] = %s \]"%invL(y_s)
	if type(y_s.apart()==add.Add):
		out = "\n\[ y(t) = \mathcal{L}^{-1}[  %s] = %s = %s\]"
		tmp = ""
		tmp1 = ""
		ar=[]
		for y in y_s.apart().args:
			tmp = l(y)+"+"
			tmp1 += l(invL(y))+"+"
			ar.append(invL(y))
		tmp1 = tmp1[::-1]
		tmp = tmp[::-1]
		y_t = 0
		for ys in ar:
			y_t+=ys
			
		return out%(tmp,tmp1,l(y_t))
	return "\n\[ y(t) = \mathcal{L}^{-1}[y(s)] = %s \]"%invL(y_s)


def solo_bode_nyquist(W :Matrix)->str:
	W_num = W[0]
	P_d = W[1]
	out = ""
	graficiB = graficiBode(W_num,P_d)
	out += graficiB

	plt.figure(1,clear=True)
	graficiN = graficiNyquist(W_num,P_d)
	out += graficiN
	
	return out



def funzioneTrasferimento(A:Matrix,B:Matrix,C:Matrix,D:Matrix,X_0,U_t,W=None):
	out = ""
	if W:
		for w in W:
			out+="\subsection{$ %s $}"%l(w[0][0])
			out += solo_bode_nyquist(w)
			#print(w[0][0])
			#out += solo_bode_nyquist([w[0],(w[0][0]+w[1])])

		return out,W	
	Phi_inv = (s*eye(A.cols)-A)
	out += "\n\[ (sI-A) = %s, |sI-A| = %s \]"%(l(Phi_inv),l(factor(Phi_inv.det())))
	Phi_i_det = factor(Phi_inv.det())
	Phi_num = simplify((Phi_inv**-1)*Phi_i_det)
	out += "\n\[ \Phi(s) = (sI-A)^{-1} = %s \]\n"%(f_l(Phi_num,Phi_i_det))
	P_d = Phi_i_det
	out+= funz_caratt_1
	H_num = simplify(Phi_num*B)
	Psi_num = simplify(C*Phi_num)
	'''
	pprint(C)
	pprint(H_num)
	pprint(D)
	pprint(P_d)
	pprint(C*H_num)
	'''
	W_num = simplify(C*H_num)+(D*P_d)
	
	#W_num = Matrix([s-10])
	#P_d = (s**2+3*s+2)*(s**2+1)

	out+= funz_caratt_2%(f_l(H_num,P_d),f_l(Psi_num,P_d),f_l(W_num,P_d),l(simplify(W_num/P_d)))
	graficiB = graficiBode(W_num,P_d)
	out += graficiB

	plt.figure(1,clear=True)
	graficiN = graficiNyquist(W_num,P_d)
	out += graficiN
	out +="\n\subsubsection{Vediamo le risposte:}"
	'''
	for u_t in tqdm(U_t):
		u_s = L(u_t)
		out += "\n\[ u(t) = %s \\to U(s) = \mathcal{L}[u(t)] = %s \]"%(l(u_t),l(u_s))
		yF = simplify(W_num*u_s/(P_d))
		out += "\n\[ y_F(s) = W(s) U(s)  = %s\] \n"%l(yF)
		out += "\n\[ y_F(t) = \mathcal{L}^{-1}[y_F(s)] = %s \]"%l(invL(yF))





	for x_0 in tqdm(X_0):
		yL_num = simplify(Psi_num*x_0)
		out +="\n\[ y_L = \Psi(s) x_0 = %s %s = %s \]\n"%(f_l(Psi_num,P_d),l(x_0),f_l(yL_num,P_d))
		for u_t in U_t:
			u_s = L(u_t)
			yF = simplify(W_num*u_s/(P_d))
			y_s = (W_num/P_d)*u_s 
			out += "\n\[ y(s) = y_L(s) + y_F(s) = %s \]"%l(y_s)
			y_t	= invL(y_s)
			out += "\n\[ y(t) = \mathcal{L}^{-1}[y(s)] = %s \]"%l(y_t)
	'''


	return out,[W_num,P_d]





