from sympy import Matrix,cos,E
from sympy.abc import t,k
from aux import gradino

class Sistema():
    def __init__(self, n:int = 0, A:Matrix = None, B : Matrix = None, C : Matrix = None, D : Matrix = None, U_t=None, X_0=None):
        if U_t is None:
            U_t = []
        if X_0 is None:
            X_0 = []
        self.n = n
        self.A = A
        self.B = B
        self.C = C
        self.U_t = U_t
        self.X_0 = X_0
        self.D = D or C*A*B-C*A*B
    def __repr__(self):
        return f"S{self.n}: A={self.A} B={self.B} C={self.C} D={self.D}"
    def get_matrici(self):
        return self.A,self.B,self.C,self.D
    def get_dati(self):
        return self.A,self.B,self.C,self.D,self.U_t,self.X_0




sistema_77 = Sistema(n=77,A = Matrix([[0,1,0,0],[0,-1,0,1],[0,0,0,0],[0,0,1,-2]]),
		B = Matrix([[0,0],[0,0],[2,0],[1,1]]),
		C = Matrix([[1,1,0,0],[2,0,0,0]]),
		D = Matrix([[0,0],[0,0]]))

sistema_88 = Sistema(n=88,A = Matrix([[1,-3,-2],[2,-4,-2],[-1,1,0]]),
		B = Matrix([2,1,0]),
		C = Matrix([[1,-2,-1]]),
		D = Matrix([0]),
		X_0 = Matrix([0,0,0]))

sistema_99 = Sistema(n=99,A = Matrix([[2,1,0],[0,2,1],[0,0,2]]),
		B = Matrix([1,1,0]),
		C = Matrix([[1,-1,0]]),
		D = Matrix([0]),
		X_0 = Matrix([0,0,0]))

sistema_111 = Sistema(n=111,A = Matrix([[0,1],[0,-1]]),
		B = Matrix([[0],[1]]),
		C = Matrix([[1,1],[2,0]]),
		D = Matrix([[0],[0]]))

sistema_122 = Sistema(n=122,		A = Matrix([[0,0],[1,-2]]),
		B = Matrix([[2,0],[1,1]]),
		C = Matrix([[0,1]]),
		D = Matrix([[0,0]]))
        
sistema_133 = Sistema(n=133,		A = Matrix([-10]),
		B = Matrix([1]),
		C = Matrix([1]),
		D = Matrix([0]),
		X_0 = Matrix([0]))

sistema_144  = Sistema(n=144,
         A = Matrix([[2,0,0],[-3,0,1],[3,1,0]]),
        B = Matrix([1,-2,2]),
        C = Matrix([[-2,-1,1]]),
        U_t = [(t+1+cos(t))*gradino(t-2)])

sistema_145 = Sistema(n=145,		A = Matrix([[1,1],[-5,-1]]),
		B = Matrix([0,1]),
		C = Matrix([[0,1]]),
        X_0 = [Matrix([0,1])]
)
sistema_146 = Sistema(n=146,		A = Matrix([[1,0],[1,0]]),
		B = Matrix([0,1]),
		C = Matrix([[0,1]]),
        X_0 = [Matrix([0,1])]
)
sistema_147 = Sistema(n=147,
		A = Matrix([[0,1],[0,-1]]),
		B = Matrix([0,1]),
		C = Matrix([[1,0],[1,2]])
)
sistema_148 = Sistema(n=148,
		A = Matrix([[0,0],[1,-2]]),
		B = Matrix([[2,0],[1,1]]),
		C = Matrix([[0,1]])
)
sistema_149  = Sistema(n=149,
         A = Matrix([[-1,-1,1],[0,0,-1],[0,1,0]]),
        B = Matrix([0,1,1]),
        C = Matrix([[0,0,1]]),
        U_t = [(t)*gradino(t-1),(t-1)*gradino(t-1),(t)*gradino(t)])


sistema_150  = Sistema(n=150,
         A = Matrix([[-2,0,0],[3,0,1],[0,1,0]]),
        B = Matrix([0,1,1]),
        C = Matrix([[0,0,1]]),
        U_t = [(t)*gradino(t-1),(t-1)*gradino(t-1),(t)*gradino(t)])
sistema_151  = Sistema(n=151,
         A = Matrix([[3,-4,-4],[2,-3,-2],[0,0,-1]]),
        B = Matrix([1,1,0]),
        C = Matrix([[-1,2,1]]),
        D = Matrix([[1]]),
        U_t = [(t-1)*gradino(t)- t*gradino(t-1)]
        )
sistema_152= Sistema(n=152,
		A = Matrix([[1,1],[-5,-1]]),
		B = Matrix([0,1]),
		C = Matrix([[0,1]]),
        U_t = [gradino(t),gradino(t-1)]
)

sistema_153  = Sistema(n=153,
         A = Matrix([[-1,-3,1],[0,0,0],[0,-2,0]]),
        B = Matrix([1,0,-2]),
        C = Matrix([[1,2,-1]]),
        U_t = [(t)*gradino(t-1),(t-1)*gradino(t-1),(t)*gradino(t),E**(2*t)*cos(t+2),2*t**2+1]
)

sistema_154  = Sistema(n=154,
         A = Matrix([[-1,0],[0,0]]),
        B = Matrix([0,1]),
        C = Matrix([[0,1],[0,0]]),
        D = Matrix([[0],[1]])
)
sistema_155  = Sistema(n=155,
         A = Matrix([[0,1],[0,0]]),
        B = Matrix([0,1]),
        C = Matrix([[1,0],[1,0]])
        
        #,D = Matrix([[0],[1]])
)
sistema_156 = Sistema(n=156,
    A = Matrix([[-1,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]]),
    B = Matrix([[0,0],[1,0],[0,0],[0,1]]),
    C = Matrix([[0,1,0,1],[0,0,0,0]]),
    D = Matrix([[0,0],[1,0]])
    )

sistema_157 = Sistema(n=157,
    A = Matrix([[-1,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,0]]),
    B = Matrix([[0,0],[1,0],[0,0],[0,1]]),
    C = Matrix([[0,1,1,0],[0,0,1,0]]),
    D = Matrix([[0,0],[1,0]])
    )
sistema_158  = Sistema(n=158,
        A = Matrix([[0,1,1],[0,-1,0],[0,0,-1]]),
    B = Matrix([1,0,0]),
    C = Matrix([[1,0,1]])
    )
sistema_159  = Sistema(n=159,
        A = Matrix([[-2,1,1],[1,-1,0],[1,0,-1]]),
    B = Matrix([1,0,1]),
    C = Matrix([[1,0,-1]])
    )



sistemi = {
    77 : sistema_77,
    88: sistema_88,
    99:sistema_99,
    111:sistema_111,
    122:sistema_122,
    133:sistema_133,
    144 : sistema_144,
    145 : sistema_145,
    146: sistema_146,
    147: sistema_147,
    148: sistema_148,
    149: sistema_149,
    151 : sistema_151,
    152 : sistema_152,
    153 : sistema_153,
    154: sistema_154,
    155: sistema_155,
    156 : sistema_156,
    157 : sistema_157,
    158 : sistema_158,
    159 : sistema_159

}