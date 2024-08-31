from lark import Lark, Transformer

TOKEN_OR   = "|"
TOKEN_AND  = "&"
TOKEN_IMPL = "->"
TOKEN_NEG  = "¬"

grammar = """
    start: expr

    ?expr: "("expr "{TOKEN_OR}" expr ")"  -> or_
          | "("expr "{TOKEN_AND}" expr ")"  -> and_
          | "("expr "{TOKEN_IMPL}" expr ")"  -> impl_
          | "{TOKEN_NEG}" expr  -> not_
          | VAR

    VAR: /[a-z]+[_0-9]*/

""".format(TOKEN_OR=TOKEN_OR, TOKEN_AND=TOKEN_AND, TOKEN_IMPL=TOKEN_IMPL, TOKEN_NEG=TOKEN_NEG)

parser = Lark(grammar, start='start')

class SubformulaExtractor(Transformer):
    def __init__(self):
        self.main_conective = None
        self.immediate_subformulas = None

    def or_(self, args):
        self.main_conective = TOKEN_OR
        self.immediate_subformulas = [args[0], args[1]]
        return f"({args[0]}{TOKEN_OR}{args[1]})"

    def and_(self, args):
        self.main_conective = TOKEN_AND
        self.immediate_subformulas = [args[0], args[1]]
        return f"({args[0]}{TOKEN_AND}{args[1]})"

    def impl_(self, args):
        self.main_conective = TOKEN_IMPL
        self.immediate_subformulas = [args[0], args[1]]
        return f"({args[0]}{TOKEN_IMPL}{args[1]})"

    def not_(self, args):
        self.main_conective = TOKEN_NEG
        self.immediate_subformulas = [args[0]]
        return f"{TOKEN_NEG}{args[0]}"

    def VAR(self, token):
        self.main_conective = "atom"
        self.immediate_subformulas = [token.value]
        return token.value

    def start(self, args):
        return args[0]

class PropositionalFormula:
    @staticmethod
    def _get_parsed_formula(formula):
        try:
          parse_tree = parser.parse(formula)
        except:
          return
        return parse_tree

    @staticmethod
    def get_main_conective_and_immediate_subformulas(formula):
      parse_tree = PropositionalFormula._get_parsed_formula(formula)
      if parse_tree is None:
        return None, None
      extractor = SubformulaExtractor()
      extractor.transform(parse_tree)
      return extractor.main_conective, extractor.immediate_subformulas


# EXEMPLO DE USO
# conective, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas("(((p->q)->q)->q)")
# if conective is not None:
#   print("valida")
#   print(conective, subformulas)
# else:
#   print("malformulada")