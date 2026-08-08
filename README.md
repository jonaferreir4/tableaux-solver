# Provador de Teoremas por Tableaux Semânticos 🧩

Um provador automático de teoremas para **Lógica Proposicional** baseado no método dos **Tableaux Semânticos** (Semantic Tableaux), desenvolvido em Python. O sistema analisa sequentes lógicos informados via arquivos de entrada (`.tab`), determinando se o sequente é **Válido** ou **Inválido** (fornecendo uma valoração de contramodelo no caso de invalidez).

---

## 👨‍💻 Equipe e Créditos

Projeto desenvolvido para a disciplina de **Lógica para Computação** no curso de **Ciência da Computação** — *Universidade Federal do Ceará (UFC)*.

* **Jona Ferreira de Sousa**
* **Rebeca Albino Ferreira Silva**

---

## 🚀 Funcionalidades

- **Análise Sintática Avançada:** Parser construído com a biblioteca [Lark](https://github.com/lark-parser/lark) para validação e extração de conectivos principais e subfórmulas imediatas.
- **Validação de Malformação:** Identifica sequentes malformados e retorna a mensagem `"Sequente inválido"`.
- **Expansão Regrada de Tableaux:**
  - **Regras $\alpha$ (não ramificadas):** Expansão imediata de conjunções verdadeiras, disjunções falsas, implicações falsas e negações.
  - **Regras $\beta$ (ramificadas):** Gerenciamento de ramificações (disjunções verdadeiras, conjunções falsas, implicações verdadeiras).
- **Backtracking Eficiente:** Utilização de pilha de ramos (`stack_branches`) para alternar entre ramos e explorar a árvore de tableaux.
- **Detecção Automatizada de Fechamento:** Identificação imediata de contradições atômicas ($T p$ e $F p$) no mesmo ramo.
- **Geração de Contramodelo (Valoração):** Quando um ramo não pode ser fechado e não há mais regras para aplicar, o algoritmo extrai as atribuições de verdade que tornam as premissas verdadeiras e a conclusão falsa (ex: `Tp Fq`).

---

## 📐 Sintaxe e Gramática

O provador suporta as seguintes convenções sintáticas para fórmulas proposicionais:

### Operadores Lógicos
| Conectivo | Símbolo | Exemplo Sintático |
| :--- | :---: | :--- |
| **Negação** | `¬` | `¬p` |
| **Conjunção** | `&` | `(p&q)` |
| **Disjunção** | `|` | `(p\|q)` |
| **Implicação** | `->` | `(p->q)` |

### Regras de Formatação
1. **Variáveis Proposicionais (Átomos):** Identificadores em letras minúsculas, podendo conter números e sublinhados (ex: `p`, `q`, `a_1`, `var2`).
2. **Parentetização Obrigatória:** Operações binárias (`&`, `|`, `->`) devem estar obrigatoriamente delimitadas por parênteses `( A op B )`.
3. **Negação:** O operador `¬` antecede diretamente a fórmula afetada sem necessidade de espaço (ex: `¬(p->q)` ou `¬p`).

---

## 📂 Formato do Arquivo de Entrada (`.tab`)

Os testes são fornecidos através de arquivos com extensão `.tab`. A estrutura do arquivo deve seguir o padrão:

```text
<N>
<Premissa_1>
<Premissa_2>
...
<Premissa_N-1>
<Conclusão>
```

- **Linha 1:** Um número inteiro $N$ ($N \ge 1$) indicando o total de fórmulas presentes no arquivo.
- **Linhas 2 a $N$:** As $N-1$ primeiras fórmulas são consideradas **Premissas** (valoradas inicialmente como `True` / $T$).
- **Linha $N+1$:** A última fórmula é a **Conclusão** do sequente (valorada inicialmente como `False` / $F$).

### Exemplo de Entrada (`exemplo5.tab`)
```text
2
(p&q)
(p|q)
```
*(Representa o sequente $p \land q \vdash p \lor q$)*

---

## 🛠️ Arquitetura do Projeto

O código-fonte está organizado em dois módulos principais em Python:

```text
Trab-logica-Tableaux/
├── parser.py           # Parser sintático e extrator de subfórmulas usando Lark
├── solver.py           # Algoritmo dos Tableaux Semânticos e execução principal
├── requirements.txt    # Dependências do projeto (lark)
├── exemplo.tab         # Arquivo de teste de exemplo
├── exemplo2.tab        # Arquivo de teste de exemplo 2
├── ...
└── README.md           # Documentação do projeto
```

### 1. `parser.py`
- Define a gramática EBNF com a biblioteca `Lark`.
- Implementa a classe `SubformulaExtractor(Transformer)` que percorre a árvore sintática gerada e extrai o conectivo principal e as subfórmulas imediatas.
- Fornece a classe estática `PropositionalFormula` com o método `get_main_conective_and_immediate_subformulas(formula)`.

### 2. `solver.py`
- Implementa a classe `Tableaux`:
  - `__init__`: Inicializa o ramo principal, marcando premissas com `True` e conclusão com `False`, e dispara a expansão $\alpha$ inicial.
  - `expand_alpha()`: Expande iterativamente todas as fórmulas do tipo $\alpha$ presentes no ramo.
  - `expand_beta()`: Aplica a primeira regra $\beta$ pendente, adicionando o ramo esquerdo e salvando o ramo direito na pilha (`stack_branches`).
  - `unstack()`: Restaura o estado para explorar a ramificação direita guardada na pilha quando um ramo fecha.
  - `is_branch_closed()`: Verifica contradições de valoração atômica ($T p$ e $F p$) no mesmo ramo.
  - `prove()`: Loop principal de prova. Retorna `"Sequente válido"` se todos os ramos fecharem, a valoração de contramodelo se algum ramo aberto terminar sem regras pendentes, ou `"Sequente inválido"` se houver fórmula malformada.

---

## ⚙️ Pré-requisitos e Instalação

### Pré-requisitos
- **Python 3.8** ou superior instalado na máquina.

### Instalação

1. Clone o repositório ou navegue até a pasta do projeto:
   ```bash
   cd Trab-logica-Tableaux
   ```

2. (Opcional, mas recomendado) Crie e ative um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # ou no Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Como Executar

Para rodar o solver, execute o arquivo `solver.py` passando o caminho do arquivo `.tab` como argumento de linha de comando:

```bash
python solver.py <caminho_do_arquivo.tab>
```

### Exemplos de Execução

#### Teste 1: Sequente Válido
```bash
python solver.py exemplo2.tab
```
**Saída Esperada:**
```text
Sequente válido
```

#### Teste 2: Sequente Inválido (Com Contramodelo)
```bash
python solver.py exemplo.tab
```
**Saída Esperada:**
```text
Tq Tp
```
*(Indica que a valoração $v(q) = \text{True}$ e $v(p) = \text{True}$ é um contramodelo que refuta o sequente).*

---

## 📋 Regras de Expansão do Tableaux Implementadas

| Tipo | Fórmula Marcada | Subfórmulas Adicionadas ao Ramo | Ação no Ramo |
| :---: | :---: | :---: | :---: |
| **$\alpha$** | $T (A \land B)$ | $T A$, $T B$ | Adiciona no mesmo ramo |
| **$\alpha$** | $F (A \lor B)$ | $F A$, $F B$ | Adiciona no mesmo ramo |
| **$\alpha$** | $F (A \to B)$ | $T A$, $F B$ | Adiciona no mesmo ramo |
| **$\alpha$** | $T (\neg A)$ | $F A$ | Adiciona no mesmo ramo |
| **$\alpha$** | $F (\neg A)$ | $T A$ | Adiciona no mesmo ramo |
| **$\beta$** | $F (A \land B)$ | $F A$ $\mid$ $F B$ | Ramifica em dois caminhos |
| **$\beta$** | $T (A \lor B)$ | $T A$ $\mid$ $T B$ | Ramifica em dois caminhos |
| **$\beta$** | $T (A \to B)$ | $F A$ $\mid$ $T B$ | Ramifica em dois caminhos |
