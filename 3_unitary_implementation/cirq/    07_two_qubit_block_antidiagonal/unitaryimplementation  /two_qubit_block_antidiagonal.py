class BlockAntidiagonalMatrix(cirq.Gate):
    def __init__(self, a, b):
        super(BlockAntidiagonalMatrix, self)
        identity = np.array([[1, 0], [0, 1]])
        self.a = np.array(a)
        self.b = np.array(b)
        self.block_b = BlockDiagonalMatrix_2(identity, self.b)
        self.block_a = BlockDiagonalMatrix_2(identity, -self.a)
        self.cs = CsMatrix_2(0, 1, 0, 1)
    
    def _num_qubits_(self):
        return 2
    
    def _decompose_(self, qubits):
        q0, q1 = qubits
        yield self.block_a(q0, q1)
        yield self.cs(q0, q1)
        yield self.block_b(q0, q1)  
        
    def _circuit_diagram_info_(self, args):
        return f"block anti-diagonal matrix with({self.a, self.b})"
