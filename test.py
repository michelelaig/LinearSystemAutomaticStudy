from aux import *
def Zassenhaus(s1,s2):
	s1m = Matr_colonne(s1)
	s2m = Matr_colonne(s2)
	
	tmp = s2m.T.row_join(Matrix([[0 for i in range(s2m.cols)] for j in range(s2m.rows)]).T)
	tmp = s1m.T.row_join(s1m.T).col_join(tmp).echelon_form()
	pprint(tmp.T.columnspace())
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
	print(out)





s1 = [Matrix([1,-2,2]),Matrix([2,1,1])]
s2 = [Matrix([1,2,0]),Matrix([1,0,2])]


Zassenhaus(s1,s2)
