# Equipe:
# Jona Ferreira de Sousa - 539700
# Rebeca Albino Ferreira Silva - 541789
# Bezalel Silva Barbosa - 540377

from parser import PropositionalFormula, TOKEN_AND, TOKEN_IMPL, TOKEN_NEG, TOKEN_OR
import sys


class Tableux:
    def __init__(self, formulas):
        self.formulas = formulas
        self.branch = []
        self.betas = []
        self.stack_branches = []

        for formula in self.formulas[:-1]: # Passa por todos menos pelo último
            formula_marcada = (formula, True) # Marca como True

            self.branch.append(formula_marcada) # Adiciona os fórmulas marcadas como True ao ramo
            self.betas.append(self.is_beta(formula_marcada)) # Adiciona True ou False ao betas a partir das fórmulas marcadas

        formula_marcada = (self.formulas[-1], False) # Marca o último como False

        self.branch.append(formula_marcada) # Adiciona a última fórmula marcada como 
        self.betas.append(self.is_beta(formula_marcada)) # Marca a última como True ou False
        
        self.expand_alpha() # Expande logo todas as fórmulas alfa

    def is_valid(self): # Verifica se as fórmulas são válidas
        i = 0
        while i < len(self.branch):
            conective, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(self.branch[i][0])
            if conective == None and subformulas == None: # caso retorne None None é falso
                return False
            return True # por padrão é verdadeiro

    # O is_beta vai valorar True pra as fórmulas que forem betas e false para os alfas
    def is_beta(self, formula):
        conective, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula[0])

        if conective == TOKEN_AND and formula[1] == False:
            return True

        elif conective == TOKEN_OR and formula[1] == True:
            return True

        elif conective == TOKEN_IMPL and formula[1] == True:
            return True
        
        return False

    # Função para verificar se uma fórmula é um átomo, se for retorna True. Se não, retorna false
    def is_atomo(self, formula):
        conective, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula[0])
        if conective == 'atom':
            return True
        return False
        

    def expand_alpha(self):
        i = 0
        while i < len(self.branch): # Percorre todo o ramo
            conective, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(self.branch[i][0])

            if conective == TOKEN_AND and self.branch[i][1] == True:  # TA^B
                self.branch.extend([(subformulas[0], True), (subformulas[1], True)]) # Adiciono as subfórmulas no ramo
                self.betas.extend([self.is_beta((subformulas[0], True)), self.is_beta((subformulas[1], True))])
                # Adiciona a lista de betas, marcando os betas como True e os alfas como False

                self.branch.pop(i) # Depois de expandir, eu removo o alfa que foi expandido
                self.betas.pop(i)  # Depois de remover para ramo tem que remover para betas


            elif conective == TOKEN_OR and self.branch[i][1] == False: # FAvB
                self.branch.extend([(subformulas[0], False), (subformulas[1], False)]) # Adiciono as subfórmulas no ramo
                self.betas.extend([self.is_beta((subformulas[0], False)), self.is_beta((subformulas[1], False))]) # adiciona True ou False em betas considerando is_beta com a tupla
                # Adiciona a lista de betas, marcando os betas como True e os alfas como False

                self.branch.pop(i) # Depois de expandir, eu removo o alfa que foi expandido
                self.betas.pop(i) # Depois de remover para ramo tem que remover para betas

            elif conective == TOKEN_IMPL and self.branch[i][1] == False: # FA->B
                self.branch.extend([(subformulas[0], True), (subformulas[1], False)]) # Adiciono as subfórmulas no ramo
                self.betas.extend([self.is_beta((subformulas[0], True)), self.is_beta((subformulas[1], False))]) # adiciona True ou False em betas considerando is_beta com a tupla
                # Adiciona a lista de betas, marcando os betas como True e os alfas como False
                
                self.branch.pop(i) # Depois de expandir, eu removo o alfa que foi expandido
                self.betas.pop(i) # Depois de remover para ramo tem que remover para betas

            elif conective == TOKEN_NEG and self.branch[i][1] == True: # T~A
                self.branch.append((subformulas[0], False)) # Adiciono a subfórmula no ramo
                self.betas.append(self.is_beta((subformulas[0], False))) # adiciona True ou False em betas considerando is_beta com a tupla 
                # Adiciona a lista de betas, marcando os betas como True e os alfas como False
                
                self.branch.pop(i) # Depois de expandir, eu removo o alfa que foi expandido
                self.betas.pop(i) # Depois de remover para ramo tem que remover para betas

            elif conective == TOKEN_NEG and self.branch[i][1] == False: # F~A
                self.branch.append((subformulas[0], True)) # Adiciono a subfórmula no ramo
                self.betas.append(self.is_beta((subformulas[0], True))) # adiciona True ou False em betas considerando is_beta com a tupla
                # Adiciona a lista de betas, marcando os betas como True e os alfas como False
                
                self.branch.pop(i) # Depois de expandir, eu removo o alfa que foi expandido
                self.betas.pop(i) # Depois de remover para ramo tem que remover para betas
            
            else: # só incremente caso não haja expansão do alfa
                i += 1  # Avançar para a próxima fórmula
                

    def expand_beta(self):
        i = 0
        for i in range(len(self.branch)): # Percorre todo o ramo 
            if self.betas[i]: # condição para que só expanda betas que ainda não foram expandidos (marcados como True)
                conective, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(self.branch[i][0])
            
                if conective == TOKEN_AND and self.branch[i][1] == False: # FA^B
                    self.branch.append((subformulas[0], False)) # Adicionar a ramificação a esquerda (Beta1)
                    self.betas.append(self.is_beta((subformulas[0], False)))  # Adiciona a lista de betas, marcando os betas como True e os alfas como False
                    self.betas[i] = False # Marca o beta expandido como falso
                    self.stack_branches.append([(subformulas[1], False), len(self.branch), self.betas[:]]) # Adiciona a pilha uma lista contendo a ramificação direita (Beta2), o tamanho atual de ramo e a lista de beta atual

                elif conective == TOKEN_OR and self.branch[i][1] == True: # TAvB
                    self.branch.append((subformulas[0], True)) # Adicionar a ramificação a esquerda (Beta1)
                    self.betas.append(self.is_beta((subformulas[0], True)))  # Adiciona a lista de betas, marcando os betas como True e os alfas como False
                    self.betas[i] = False  # Marca o beta expandido como falso
                    self.stack_branches.append([(subformulas[1], True), len(self.branch), self.betas[:]]) # Adiciona a pilha uma lista contendo a ramificação direita (Beta2), o tamanho atual de ramo e a lista de beta atual

                elif conective == TOKEN_IMPL and self.branch[i][1] == True: # TA->B
                    self.branch.append((subformulas[0], False)) # Adicionar a ramificação a esquerda (Beta1)
                    self.betas.append(self.is_beta((subformulas[0], False)))  # Adiciona a lista de betas, marcando os betas como True e os alfas como False
                    self.betas[i] = False  # Marca o beta expandido como falso
                    self.stack_branches.append([(subformulas[1], True), len(self.branch), self.betas[:]]) # Adiciona a pilha uma lista contendo a ramificação direita (Beta2), o tamanho atual de ramo e a lista de beta atual

                break # para o loop, para que só execute um beta por vez
    
    def unstack(self):

        if not self.stack_branches: # se a pilha de ramos está vazia, só retorna
            return
        
        # se não está, eu vou pegar o beta2 , o tamanho e a lista de betas
        #  e desempilhar (remover da pilha)
        beta2, tam, betas = self.stack_branches.pop()
        self.branch = self.branch[:tam - 1] # É retirado do ramo o último valor (que seria o valor que causou o fechamento do ramo)
        self.betas = [beta for beta in betas[:-1]] # o beta é atualizado com a mudança do ramo, retirando o booleano que representava o último valor
        self.branch.append(beta2) # O beta dois que estava guardado na pilha é adicionado ao ramo
        self.betas.append(self.is_beta(beta2)) # é definido Alfa ou Beta pra ele na lista de betas

    def is_branch_closed(self):

        literals = {} # armazena os literais para comparação
        for i in range(len(self.branch)): # Vai percorrer todo o ramo
            if self.is_atomo(self.branch[i][0]): # Vai limitar os próximos passos aos átomos
                if self.branch[i][0] in literals: # Verifica se o átomo atual já está no dicionário
                    if literals[self.branch[i][0]] != self.branch[i][1]: # Caso esteja, ele vai comparar se as valorações são diferentes (True, False)
                        return True # Caso sejam diferentes, retorna True
                else:
                    literals[self.branch[i][0]] = self.branch[i][1] # Adiciona o átomo e a valoração 
        return False # Retorna falso se não houver contradição 
    

    # Passa as tuplas para a escrita padrão em string
    def pass_string_default(self, valuations):
        valuations_str = ''
        for atomo, value in valuations:
            if value:
                valuations_str += f"T{atomo} "
            else:
                valuations_str += f"F{atomo} "
        
        return valuations_str.strip() # Remove o espaço do fim

    def prove(self):

        while True:
            if self.is_valid(): # verificar se há retorno de fórmulas como None None
               
                if self.is_branch_closed(): # verifica se há contradição dentro do ramo
                    if self.stack_branches: # varifica se a pilha está vazia
                        self.unstack() # se houver desempilha
                    else:
                        # Se a pilha estiver vazia e o ramo está fechada quer dizer que o loop passou 
                        # por todos os possiveis ramos e todos eram fechados, consequentemente, a fórmula é válida
                        return 'Sequente válido'
                else:
                    if True in self.betas:   # Caso o ramo não feche mas ainda tem betas para expandir
                       
                        # Se houver, o codigo erá expandir o beta 
                        self.expand_beta() # Expande beta uma vez
                        self.expand_alpha() # A cada expasão de beta, o codigo procura expandir os possíveis alfas gerados (caso tenha)  
                    
                    else:
                       

                        valuations = set() # Vai armazenar as valorações, sem repetição
                        
                        # vai percorrer o branch e inserir apenas os átomos em valuation
                        for item in self.branch: 
                            if self.is_atomo(item):
                                valuations.add(item)


                        return self.pass_string_default(valuations)   ## vai retornar usando a função pass_string_default os átomos marcados no padrão conhecido (ex: Tp Fq)
            else: # Se is_valid for falsa, quer dizer que uma das fórmulas passadas retornou None None
                return "Sequente inválido"   

    
def main():
    filename = sys.argv[1]
    with open(filename, 'r', encoding="utf-8") as x:
        num_formulas = int(x.readline())
        formulas = [x.readline().strip() for _ in range(num_formulas)]
        tableux = Tableux(formulas)

        print(tableux.prove())


if __name__ == "__main__":
    main()
