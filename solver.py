from parser import PropositionalFormula, TOKEN_AND, TOKEN_IMPL, TOKEN_NEG, TOKEN_OR
import sys


class Tableux:
    def __init__(self, formulas):
        self.formulas = formulas
        self.ramo = []
        self.betas = []
        self.pilhaDeRamos = []

        for formula in self.formulas[:-1]: # Passa por todos menos pelo último
            formula_marcada = (formula, True) # Marca como True

            self.ramo.append(formula_marcada) # Adiciona os fórmulas marcadas como True ao ramo
            self.betas.append(self.is_beta(formula_marcada)) # Adiciona True ou False ao betas a partir das fórmulas marcadas

        formula_marcada = (self.formulas[-1], False) # Marca o último como False

        self.ramo.append(formula_marcada) # Adiciona a última fórmula marcada como 
        self.betas.append(self.is_beta(formula_marcada))

        self.expand_alpha()

    # Função que vai preencher a lista de betas com True se a fórmula for Beta
    def is_beta(self, formula):
        conective, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula[0])

        if conective == TOKEN_AND and formula[1] == False:
            return True

        elif conective == TOKEN_OR and formula[1] == True:
            return True

        elif conective == TOKEN_IMPL and formula[1] == True:
            return True
        
        return False

    # Função para verificar se uma fórmula é um átomo
    def is_atomo(self, formula):
        conective, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula[0])

        if conective == 'atom':
            return True
        
        return False

    def expand_alpha(self):
        i = 0
        while i < len(self.ramo):
            conective, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(self.ramo[i][0])

            if conective == TOKEN_AND and self.ramo[i][1] == True:  # TA^B
                self.ramo.extend([(subformulas[0], True), (subformulas[1], True)]) # Adiciono as subfórmulas no ramo
                self.betas.extend([self.is_beta((subformulas[0], True)), self.is_beta((subformulas[1], True))])
                # Adiciona a lista de betas, marcando os betas como True e os alfas como False

                self.ramo.pop(i) # Depois de expandir, eu removo o alfa que foi expandido
                self.betas.pop(i)

            elif conective == TOKEN_OR and self.ramo[i][1] == False: # FAvB
                self.ramo.extend([(subformulas[0], False), (subformulas[1], False)]) # Adiciono as subfórmulas no ramo
                self.betas.extend([self.is_beta((subformulas[0], False)), self.is_beta((subformulas[1], False))])
                # Adiciona a lista de betas, marcando os betas como True e os alfas como False

                self.ramo.pop(i) # Depois de expandir, eu removo o alfa que foi expandido
                self.betas.pop(i) # Depois de remover para ramo tem que remover para betas

            elif conective == TOKEN_IMPL and self.ramo[i][1] == False: # FA->B
                self.ramo.extend([(subformulas[0], True), (subformulas[1], False)]) # Adiciono as subfórmulas no ramo
                self.betas.extend([self.is_beta((subformulas[0], True)), self.is_beta((subformulas[1], False))])
                # Adiciona a lista de betas, marcando os betas como True e os alfas como False
                
                self.ramo.pop(i) # Depois de expandir, eu removo o alfa que foi expandido
                self.betas.pop(i) # Depois de remover para ramo tem que remover para betas

            elif conective == TOKEN_NEG and self.ramo[i][1] == True: # T~A
                self.ramo.append((subformulas[0], False)) # Adiciono as subfórmulas no ramo
                self.betas.append(self.is_beta((subformulas[0], False)))
                # Adiciona a lista de betas, marcando os betas como True e os alfas como False
                
                self.ramo.pop(i) # Depois de expandir, eu removo o alfa que foi expandido
                self.betas.pop(i) # Depois de remover para ramo tem que remover para betas

            elif conective == TOKEN_NEG and self.ramo[i][1] == False: # F~A
                self.ramo.append((subformulas[0], True)) # Adiciono as subfórmulas no ramo
                self.betas.append(self.is_beta((subformulas[0], True)))
                # Adiciona a lista de betas, marcando os betas como True e os alfas como False
                
                self.ramo.pop(i) # Depois de expandir, eu removo o alfa que foi expandido
                self.betas.pop(i) # Depois de remover para ramo tem que remover para betas
            
            i += 1  # Avançar para a próxima fórmula
            
            if self.is_branch_closed(): # se o ramo fechar, não precisa terminar de expandir
                break

    def expand_beta(self):
        for i in range(len(self.ramo)):
            if self.betas[i]:
                conective, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(self.ramo[i][0])

                if conective == TOKEN_AND and self.ramo[i][1] == False:
                    self.ramo.append((subformulas[0], False))
                    self.betas.append(self.is_beta((subformulas[0], False)))
                    self.betas[i] = False
                    self.pilhaDeRamos.append([(subformulas[1], False), len(self.ramo), self.betas.copy()])

                elif conective == TOKEN_OR and self.ramo[i][1] == True:
                    self.ramo.append((subformulas[0], True))
                    self.betas.append(self.is_beta((subformulas[0], True)))
                    self.betas[i] = False
                    self.pilhaDeRamos.append([(subformulas[1], True), len(self.ramo), self.betas.copy()])

                elif conective == TOKEN_IMPL and self.ramo[i][1] == True:
                    self.ramo.append((subformulas[0], False))
                    self.betas.append(self.is_beta((subformulas[0], False)))
                    self.betas[i] = False
                    self.pilhaDeRamos.append([(subformulas[1], True), len(self.ramo), self.betas.copy()])

                break           
    
    def unstack(self):
        if not self.pilhaDeRamos:
            return
        
        beta2, tam, betas = self.pilhaDeRamos.pop()
        self.ramo = self.ramo[:tam]
        self.betas = betas
        self.ramo.append(beta2)
        self.betas.append(self.is_beta(beta2))

    def is_branch_closed(self):
        literals = {} # armazena os literais para comparação
        for i in range(len(self.ramo)): # Vai percorrer todo o ramo
            if self.is_atomo(self.ramo[i][0]): # Vai limitar os próximos passos aos átomos
                if self.ramo[i][0] in literals: # Verifica se o átomo atual já está no dicionário
                    if literals[self.ramo[i][0]] != self.ramo[i][1]: # Caso esteja, ele vai comparar se as valorações são diferentes (True, False)
                        return True # Caso sejam diferentes, retorna True
                else:
                    literals[self.ramo[i][0]] = self.ramo[i][1] # Adiciona o átomo e a valoração 
        return False # Retorna falso se não houver contradição 
    
    def prove(self):
        while True:
            print(f"RAMO - {self.ramo}")
            print(f"BETAS - {self.betas}")
            print(f"TAMANHO DO RAMO - {len(self.ramo)}")
            print(f"TAMANHO DO BETA - {len(self.betas)}")
            print(f"PILHA - {self.pilhaDeRamos}")

            if self.is_branch_closed():
                if self.pilhaDeRamos:
                    self.unstack()
                else:
                    return 'Sequente verdadeiro'
            else:
                if True in self.betas:
                    self.expand_beta()
                    self.expand_alpha()  
                else:
                    valoracoes = set()

                    for item in self.ramo: 
                        if self.is_atomo(item):
                            valoracoes.add(item)
                        
                    return valoracoes      

        # while not self.is_branch_closed():
        #     print(f"RAMO - {self.ramo}")
        #     print(f"BETAS - {self.betas}")
        #     print(f"TAMANHO DO RAMO - {len(self.ramo)}")
        #     print(f"TAMANHO DO BETA - {len(self.betas)}")
        #     print(f"PILHA - {self.pilhaDeRamos}")
                            
        #     self.expand_alpha()  # Expandir todas as fórmulas alfa primeiro

        #     if not self.pilhaDeRamos and True not in self.betas:
        #         return 'VALORAÇÃO QUE REFUTA'

        #     self.expand_beta()

        #     print(f"RAMO - {self.ramo}")
        #     print(f"BETAS - {self.betas}")
        #     print(f"TAMANHO DO RAMO - {len(self.ramo)}")
        #     print(f"TAMANHO DO BETA - {len(self.betas)}")
        #     print(f"PILHA - {self.pilhaDeRamos}")

        # return 'PROVADO'

def main():
    filename = sys.argv[1]
    with open(filename, 'r', encoding="utf-8") as x:
        num_formulas = int(x.readline())
        formulas = [x.readline().strip() for _ in range(num_formulas)]
        tableux = Tableux(formulas)
        print(tableux.prove())


if __name__ == "__main__":
    main()
