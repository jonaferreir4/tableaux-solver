from parser import PropositionalFormula, TOKEN_AND, TOKEN_IMPL, TOKEN_NEG, TOKEN_OR
import sys


class Tableux:
    def __init__(self, formulas):
        self.formulas = formulas
        self.ramo = []
        self.tamAtual = 0
        self.betas = []
        self.pilhaDeRamos = []

        self.initial_markings = [(formula, True)
                                 for formula in self.formulas[:-1]]
        self.initial_markings.append((self.formulas[-1], False))
        self.ramo.extend(self.initial_markings)
        self.tamAtual += len(self.ramo)
        self.betas = [False] * self.tamAtual

    def add_formula_to_branch(self):
        pass

    def expand_alpha(self):
        i = 0
        while i < self.tamAtual:
            conective, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(
                self.ramo[i][0])
            if conective == TOKEN_AND and self.ramo[i][1] == True:
                self.ramo.extend(
                    [(subformulas[0], True), (subformulas[1], True)])
                self.tamAtual += 1
                self.betas.extend([False, False])
                self.ramo.pop(i)
                continue

            elif conective == TOKEN_OR and self.ramo[i][1] == False:
                self.ramo.extend(
                    [(subformulas[0], False), (subformulas[1], False)])
                self.tamAtual += 1
                self.betas.extend([False, False])
                self.ramo.pop(i)
                continue

            elif conective == TOKEN_IMPL and self.ramo[i][1] == False:
                self.ramo.extend(
                    [(subformulas[0], True), (subformulas[1], False)])
                self.tamAtual += 1
                self.betas.extend([False, False])
                self.ramo.pop(i)
                continue

            elif conective == TOKEN_NEG and self.ramo[i][1] == True:
                self.ramo.append((subformulas[0], False))
                self.betas.extend([False])
                self.ramo.pop(i)
                continue

            elif conective == TOKEN_NEG and self.ramo[i][1] == False:
                self.ramo.append((subformulas[0], True))
                self.betas.extend([False])
                self.ramo.pop(i)
                continue

            if self.is_branch_closed():
                break

            i += 1  # Avançar para a próxima fórmula

    def expand_beta(self):
        for i in range(self.tamAtual):
            if not self.betas[i]:
                conective, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(
                    self.ramo[i][0])
                if conective == TOKEN_AND and self.ramo[i][1] == False:
                    self.ramo.append((subformulas[0], False))
                    self.tamAtual += 1
                    self.pilhaDeRamos.extend(
                        [self.ramo[self.tamAtual - 1], self.tamAtual, self.betas])
                    self.betas[i] = True

                elif conective == TOKEN_OR and self.ramo[i][1] == True:
                    self.betas[i] = True
                    self.pilhaDeRamos.extend(
                        [self.ramo[self.tamAtual - 1], self.tamAtual, self.betas])
                    self.ramo.append((subformulas[0], True))
                    self.tamAtual += 1

                elif conective == TOKEN_IMPL and self.ramo[i][1] == True:
                    self.ramo.append((subformulas[0], False))
                    self.tamAtual += 1
                    self.pilhaDeRamos.extend(
                        [self.ramo[self.tamAtual - 1], self.tamAtual, self.betas])
                    self.betas[i] = True

            if self.is_branch_closed()[0]:
                self.ramo.pop(self.is_branch_closed()[1])
                self.betas.pop()
                self.tamAtual -=1

                break

            self.expand_alpha()

    def is_branch_closed(self):
        literals = {}

        for i in range(self.tamAtual):
            if len(self.ramo[i][0]) == 1:
                if self.ramo[i][0] in literals:
                    if literals[self.ramo[i][0]] != self.ramo[i][1]:
                        return (True, i)
                else:
                    literals[self.ramo[i][0]] = self.ramo[i][1]
        return (False, None)


def main():
    filename = sys.argv[1]
    with open(filename, 'r', encoding="utf-8") as x:
        num_formulas = int(x.readline())
        formulas = [x.readline().strip() for _ in range(num_formulas)]
        tableux = Tableux(formulas)
        tableux.expand_alpha()
        tableux.expand_beta()
        print(f"RAMO - {tableux.ramo}")
        print(f"BETAS - {tableux.betas}")
        print(f"TAMANHO DO RAMO - {tableux.tamAtual}")
        print(f"PILHA - {tableux.pilhaDeRamos}")


if __name__ == "__main__":
    main()
