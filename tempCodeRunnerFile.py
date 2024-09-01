# beta
# criar dois novos ramo pra cada formula (OR, IMP)
def expand_beta(self):
        i = 0
        while i < self.tamAtual:
            conective, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(
                self.ramo[i][0])
            if conective == TOKEN_OR and self.ramo[i][1] == True:
                # Criar dois novos ramos
                ramo1 = self.ramo.copy()
                ramo1.append((subformulas[0], True))
                ramo2 = self.ramo.copy()
                ramo2.append((subformulas[1], True))
                self.pilhaDeRamos.append(ramo1)
                self.pilhaDeRamos.append(ramo2)
            elif conective == TOKEN_IMPL and self.ramo[i][1] == True:
                # Criar dois novos ramos
                ramo1 = self.ramo.copy()
                ramo1.append((subformulas[0], False))
                ramo2 = self.ramo.copy()
                ramo2.append((subformulas[1], True))
                self.pilhaDeRamos.append(ramo1)
                self.pilhaDeRamos.append(ramo2)
            i += 1
          
