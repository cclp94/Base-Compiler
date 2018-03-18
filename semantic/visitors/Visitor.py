from syntactic.SyntaxTree import *
from functools import singledispatch, update_wrapper

#support overloading for class methods
def methdispatch(func):
    dispatcher = singledispatch(func)
    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper

class Visitor:
    @methdispatch
    def visit(self, node): pass

    @visit.register(ProgNode)
    def _(self, node): pass

    @visit.register(ClassDeclNode)
    def _(self, node): pass

    @visit.register(ClassSourceNode)
    def _(self, node): pass

    @visit.register(ProgramNode)
    def _(self, node): pass

    @visit.register(IdNode)
    def _(self, node): pass

    @visit.register(TypeNode)
    def _(self, node): pass

    @visit.register(InheritanceNode)
    def _(self, node): pass

    @visit.register(ClassMemberDeclNode)
    def _(self, node): pass

    @visit.register(ClassMethodNode)
    def _(self, node): pass

    @visit.register(ClassAttributeNode)
    def _(self, node): pass

    @visit.register(ArrayDimenssionNode)
    def _(self, node): pass

    @visit.register(FuncParamsNode)
    def _(self, node): pass

    @visit.register(FuncParamNode)
    def _(self, node): pass

    @visit.register(FuncBodyNode)
    def _(self, node): pass

    @visit.register(IntegerNode)
    def _(self, node): pass

    @visit.register(FloatNode)
    def _(self, node): pass

    @visit.register(AssignNode)
    def _(self, node): pass

    @visit.register(VariableNode)
    def _(self, node): pass

    @visit.register(VariableDeclNode)
    def _(self, node): pass

    @visit.register(IfStatementNode)
    def _(self, node): pass

    @visit.register(ForLoopNode)
    def _(self, node): pass

    @visit.register(ReturnNode)
    def _(self, node): pass

    @visit.register(PutNode)
    def _(self, node): pass

    @visit.register(GetNode)
    def _(self, node): pass

    @visit.register(AddOpNode)
    def _(self, node): pass

    @visit.register(MultOpNode)
    def _(self, node): pass

    @visit.register(RelOpNode)
    def _(self, node): pass

    @visit.register(IndicesNode)
    def _(self, node): pass

    @visit.register(ScopeBlockNode)
    def _(self, node): pass

    @visit.register(ArithmExprNode)
    def _(self, node): pass

    @visit.register(ExprNode)
    def _(self, node): pass

    @visit.register(TermNode)
    def _(self, node): pass

    @visit.register(FactorNode)
    def _(self, node): pass

    @visit.register(AParamsNode)
    def _(self, node): pass