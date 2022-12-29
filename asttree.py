"""
All the methods were generated based on the list of nodes from the
"Green Tree Snakes" guide:
https://greentreesnakes.readthedocs.io/en/latest/index.html
"""

import ast

result=[]
res=[]

class Visitor(ast.NodeVisitor):
    parent = None
        
    def visit_Num(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Str(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_FormattedValue(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_JoinedStr(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Bytes(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_List(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Tuple(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Set(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Dict(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Ellipsis(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_NameConstant(self, node):
        print(node)
        
        print(node.id)
        self.generic_visit(node)

    def visit_Name(self, node):
        print("namrrrrrrrrrrrrrrrr")
        print(self.parent)
        if self.parent == "func":
            res.append({'line': node.lineno, 'operation': node.id})
            print(self.parent)
            self.parent = ""
            print("rrrrrrrrrrr")
            
        elif self.parent == "subscript" and isinstance(node.ctx, ast.Load):
            res.append({'line': node.lineno, 'value': node.id})
            
        elif isinstance(node.ctx, ast.Load):
            res.append({'line': node.lineno, 'value': node.id})
        
        if isinstance(node.ctx, ast.Store):
            res.append({'line': node.lineno, 'target': node.id})
         
        self.generic_visit(node)

    def visit_Load(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Store(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Del(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Starred(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Expr(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_UAdd(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_USub(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Not(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Invert(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_BinOp(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Add(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Sub(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Mult(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Div(self, node):
        print(node)
        self.generic_visit(node)

    def visit_FloorDiv(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Mod(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Pow(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_LShift(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_RShift(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_BitOr(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_BitXor(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_BitAnd(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_MatMult(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_And(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Or(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Compare(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Eq(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_NotEq(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Lt(self, node):
        print(node)
        self.generic_visit(node)

    def visit_LtE(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Gt(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_GtE(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Is(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_IsNot(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_In(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_NotIn(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Call(self, node):
        node.parent = self.parent
        self.parent = "func"
        print(node._fields)
        print("callllllllllllllllllllll")
        
        self.generic_visit(node)
        

    def visit_keyword(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_IfExp(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Attribute(self, node):
        try:
            print(node.attr+"."+node.value.id)
            res.append({'line': node.lineno, 'operation': node.value.id+"."+node.attr})
            self.parent = ""
        except AttributeError:
            self.generic_visit(node)
        print(node)
        
        #self.generic_visit(node)

    def visit_Subscript(self, node):
        self.parent = "subscript"
        print(node)
        
        self.generic_visit(node)

    def visit_Index(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Slice(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_ExtSlice(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_ListComp(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_SetComp(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_DictComp(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_comprehension(self, node):
        print(node)
        
        self.generic_visit(node)

    '''def visit_Assign(self, node):
        print(node)
        print(node.lineno)
        
        self.generic_visit(node)
    '''
    def visit_AnnAssign(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Print(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Raise(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Assert(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Delete(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Pass(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Import(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_alias(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_If(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_For(self, node):
        print("forrrrrrrrrrrrrrrrrr")
        print(node)
        
        self.generic_visit(node)

    def visit_While(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Break(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Continue(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Try(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_TryFinally(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_TryExcept(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_With(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_withitem(self, node):
        print(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Lambda(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_arguments(self, node):
        print("arguments")
        print(node)
        self.generic_visit(node)

    def visit_arg(self, node):
        print("arguments")
        print(node)
        
        self.generic_visit(node)

    def visit_Return(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Yield(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_YieldFrom(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Global(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_Nonlocal(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        print("function")
        print(node)
        
        self.generic_visit(node)

    def visit_Await(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        print(node)
        
        self.generic_visit(node)

    def visit_AsyncWith(self, node):
        print(node)
        
        self.generic_visit(node)
        
    def visit_Constant(self, node):
        print(self)
        
        res.append({'line': node.lineno, 'value': node.s})
        self.generic_visit(node)


def combine_parsed_data(parsed_code):
    print(parsed_code)
    updated_result = {}
    for line in parsed_code:
        line_no = line['line']
        if line_no not in updated_result:
            updated_result[line['line']] = {}
            p = []
        for key in line.keys():
            if key == 'value':
                p.append(line[key])
            if key != 'line':
                if key == 'value':
                    updated_result[line_no].update({key: p})
                else:
                    updated_result[line_no].update({key: line[key]})
    print(p)
    return updated_result
                
code = """
def measuretime(f, n, *args):
    t = [0]*n
    res = f(*args)
    for n in range(n):
        t0 = time.time()
        f(*args)
        t[n] = time.time() - t0
    return(1000*np.array(t), res)
def fun_rqa(v,metric):
    # Attempt sparse RQA if metric is euclidean
    metric_sup = (metric is "supremum")
    rp = RecurrencePlot(v, metric=metric, sparse_rqa=metric_sup,
    threshold=1.2, dim=3, tau=6)
    rqa = rp.rqa_summary()
    rqa["Lmax"] = rp.max_diaglength()
    rqa["ENT"] = rp.diag_entropy()
    rqa["TT"] = rp.trapping_time()
    return(rqa)
    
def benchmark(metric):
    m = np.loadtxt("rossler.txt")
    for r in range(12):
        x = m[:250*(r+1), 2*r]
        (tt, res) = measuretime(fun_rqa, 5, x, metric)
        t = median(tt)
        with open("benchmark_rqa_python_%s.txt"%metric, "a") as f:
            f.write("%d\t%f\t"%(r,t))
            for k in ["RR","DET","L","Lmax","ENT","LAM","TT"]:
                f.write("%s\t"%(res[k]))
            f.write("\\n")
"""   
root = ast.parse(code)
print(ast.dump(root, indent=4))
visitor = Visitor()
visitor.visit(root)
combine_parsed_data(res)