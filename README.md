# Simplex-solver
Programa de Resolução de Problemas de Programação Linear por Método Simplex

### Versoes
    - Python: completo
    - Rust: em desenvolvimento (Estudo).

## TDE - Otimização de Sistemas Lineares
- **NOME:** Erick Lemmy dos Santos Oliveira
- **PROF:** Guilherme Nunes Nogueira Neto

Este é um programa em Python que resolve problemas de programação linear utilizando o método Simplex. Ele foi desenvolvido como parte de uma tarefa (TDE) para consolidar conhecimentos sobre o funcionamento do método Simplex, incluindo casos de maximização e minimização. O programa também é capaz de lidar com problemas de programação linear com diferentes tipos de restrições (≤, ≥, =).

### Requisitos e Funcionalidades
O programa atende aos seguintes requisitos:

1. **Implementação de Maximização e Minimização:** O programa permite a resolução de problemas de maximização e minimização, conforme especificado pelo usuário.

2. **Interface com o Usuário:** O programa possui uma interface simples que permite ao usuário inserir a matriz de coeficientes, os vetores de coeficientes da função objetivo e das restrições. O tipo de problema (maximização ou minimização) também é informado pelo usuário.

3. **Número de Iterações:** O programa fornece informações sobre o número de iterações realizadas durante a solução do problema.

4. **Identificação do "Z" ou "C" Ótimo e Valores das Variáveis Básicas:** O software apresenta a solução ótima do problema, indicando os valores de Z ou C, bem como os valores das variáveis básicas.

5. **Apontar Problemas de Degeneração:** O programa é capaz de identificar se o problema de programação linear sofre de degeneração, um desafio comum nesse tipo de problema.

6. **Indicação de Problemas Inviáveis:** O software verifica se o problema de programação linear é inviável, ou seja, não possui solução factível.

7. **Indicação de Problemas Sem Fronteira:** O programa identifica se o problema de programação linear não possui fronteira em alguma dimensão, o que resulta em soluções ilimitadas.

### Utilização
Para utilizar o programa, siga as instruções apresentadas na interface do usuário. 

O programa solicitará informações sobre a matriz de coeficientes, os vetores de coeficientes da função objetivo e das restrições, bem como o tipo de problema (maximização ou minimização). Após a execução, o programa apresentará a solução do problema e informações adicionais, como o número de iterações e a presença de soluções múltiplas, degeneração, inviabilidade ou soluções ilimitadas.

O programa foi projetado para atender a requisitos educacionais, fornecendo uma ferramenta de aprendizado prática para o método Simplex. 

Portanto, é adequado para estudantes e entusiastas de programação linear que desejam compreender e aplicar o método Simplex na resolução de problemas do mundo real.

**Observação:** O programa foi desenvolvido para fins educacionais e de aprendizado ativo. Portanto, os exemplos e dados iniciais podem ser substituídos pelos seus próprios problemas de programação linear.

---
### Como executar:

No windows execute:
- python simplex.py

No linux:
- python3 simplex.py

Ou rode diretamente pelo repl.it:
- https://replit.com/join/dboqhxqhuy-ericklemmy

### Exemplos:

#### Input exemplo:
![Exemplo](/imgs/exemplo_1.png)

- Minimização e Maximização:

#### 1. Input:

Maximize $\to$ $C = 3x_1 + 2x_2$ <br>
$S.t:$ <br>
    $2x_1 + 1x_2\leq 18$ <br>
    $2x_1 + 3x_2\leq 42$ <br>
    $3x_1 + 1x_2\leq 24$ <br>
$x_1, x_2, x_3, x_4, x_5 \geq 0$ <br>

```python 
C = [3, 2]                   # objetivo
A = [[2, 1], [2, 3], [3, 1]] # vetor base
b = [18, 42, 24]             # restricao
ineq = ["<=", "<=", "<="]
```

#### 1. Output:
```python
Press enter to continue...
Iteração: 0
Pivo: 3
Variavel entrando: x1
Variavel saindo: s3

Tabela Atual:
┏━━━━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━┓
┃ x1 ┃ x2 ┃ s1 ┃ s2 ┃ s3 ┃ b  ┃
┡━━━━╇━━━━╇━━━━╇━━━━╇━━━━╇━━━━┩
│ 2  │ 1  │ 1  │ 0  │ 0  │ 18 │
│ 2  │ 3  │ 0  │ 1  │ 0  │ 42 │
│ 3  │ 1  │ 0  │ 0  │ 1  │ 24 │
│ -3 │ -2 │ 0  │ 0  │ 0  │ 0  │
└────┴────┴────┴────┴────┴────┘
Soluçao atual:
x1: 0; x2: 0; s1: 18; s2: 42; s3: 24; z: 0;

Press enter to continue...
Iteração: 1
Pivo: 1/3
Variavel entrando: x2
Variavel saindo: s1

Tabela Atual:
┏━━━━┳━━━━━┳━━━━┳━━━━┳━━━━━━┳━━━━┓
┃ x1 ┃ x2  ┃ s1 ┃ s2 ┃ s3   ┃ b  ┃
┡━━━━╇━━━━━╇━━━━╇━━━━╇━━━━━━╇━━━━┩
│ 0  │ 1/3 │ 1  │ 0  │ -2/3 │ 2  │
│ 0  │ 7/3 │ 0  │ 1  │ -2/3 │ 26 │
│ 1  │ 1/3 │ 0  │ 0  │ 1/3  │ 8  │
│ 0  │ -1  │ 0  │ 0  │ 1    │ 24 │
└────┴─────┴────┴────┴──────┴────┘
Soluçao atual:
x1: 8; x2: 0; s1: 2; s2: 26; s3: 0; z: 24;

Press enter to continue...
Iteração: 2
Pivo: 4
Variavel entrando: s3
Variavel saindo: s2

Tabela Atual:
┏━━━━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━┓
┃ x1 ┃ x2 ┃ s1 ┃ s2 ┃ s3 ┃ b  ┃
┡━━━━╇━━━━╇━━━━╇━━━━╇━━━━╇━━━━┩
│ 0  │ 1  │ 3  │ 0  │ -2 │ 6  │
│ 0  │ 0  │ -7 │ 1  │ 4  │ 12 │
│ 1  │ 0  │ -1 │ 0  │ 1  │ 6  │
│ 0  │ 0  │ 3  │ 0  │ -1 │ 30 │
└────┴────┴────┴────┴────┴────┘
Soluçao atual:
x1: 6; x2: 6; s1: 0; s2: 12; s3: 0; z: 30;

Press enter to continue...

Solução:
┏━━━━━━┳━━━━┳━━━━┳━━━━━━┳━━━━━━┳━━━━┳━━━━┓
┃ Base ┃ x1 ┃ x2 ┃   s1 ┃   s2 ┃ s3 ┃  b ┃
┡━━━━━━╇━━━━╇━━━━╇━━━━━━╇━━━━━━╇━━━━╇━━━━┩
│   x2 │  0 │  1 │ -1/2 │  1/2 │  0 │ 12 │
│   s3 │  0 │  0 │ -7/4 │  1/4 │  1 │  3 │
│   x1 │  1 │  0 │  3/4 │ -1/4 │  0 │  3 │
│    z │  0 │  0 │  5/4 │  1/4 │  0 │ 33 │
└──────┴────┴────┴──────┴──────┴────┴────┘
Existem múltiplas soluções ótimas.

Solução Encontrada:
x1: 3
x2: 12
s1: 0
s2: 0
s3: 3
z: 33
```

---

#### 2. Input:

- Solucao Unica
  
Maximize $\to$ $Z = 1x_1 + 1x_2$ <br>
$S.t:$ <br>
    $1x_1 + 2x_2 \leq 4$ <br>
    $4x_1 + 2x_2 \leq 12$ <br>
$x_1, x_2 \geq 0$ <br>

```python 
A = [[1, 2], [4, 2]]
C = [1, 1]
b = [4, 12]
ineq = ["<=", "<="]
```

#### 2. Output:
```python
Tabela Atual:
┏━━━━┳━━━━┳━━━━┳━━━━┳━━━━┓
┃ x1 ┃ x2 ┃ s1 ┃ s2 ┃ b  ┃
┡━━━━╇━━━━╇━━━━╇━━━━╇━━━━┩
│ 1  │ 2  │ 1  │ 0  │ 4  │
│ 4  │ 2  │ 0  │ 1  │ 12 │
│ -1 │ -1 │ 0  │ 0  │ 0  │
└────┴────┴────┴────┴────┘
Soluçao atual:
x1: 0; x2: 0; s1: 4; s2: 12; z: 0;

Press enter to continue...
Iteração: 1
Pivo: 3/2
Variavel entrando: x2
Variavel saindo: s1

Tabela Atual:
┏━━━━┳━━━━━━┳━━━━┳━━━━━━┳━━━┓
┃ x1 ┃ x2   ┃ s1 ┃ s2   ┃ b ┃
┡━━━━╇━━━━━━╇━━━━╇━━━━━━╇━━━┩
│ 0  │ 3/2  │ 1  │ -1/4 │ 1 │
│ 1  │ 1/2  │ 0  │ 1/4  │ 3 │
│ 0  │ -1/2 │ 0  │ 1/4  │ 3 │
└────┴──────┴────┴──────┴───┘
Soluçao atual:
x1: 3; x2: 0; s1: 1; s2: 0; z: 3;

Press enter to continue...

Solução:
┏━━━━━━┳━━━━┳━━━━┳━━━━━━┳━━━━━━┳━━━━━━┓
┃ Base ┃ x1 ┃ x2 ┃   s1 ┃   s2 ┃    b ┃
┡━━━━━━╇━━━━╇━━━━╇━━━━━━╇━━━━━━╇━━━━━━┩
│   x2 │  0 │  1 │  2/3 │ -1/6 │  2/3 │
│   x1 │  1 │  0 │ -1/3 │  1/3 │  8/3 │
│    z │  0 │  0 │  1/3 │  1/6 │ 10/3 │
└──────┴────┴────┴──────┴──────┴──────┘
A solução é única e ótima.

Solução Encontrada:
x1: 8/3
x2: 2/3
s1: 0
s2: 0
z: 10/3
```

---

#### 3. Input:

- Multiplas Soluções

![exemplo_3](/imgs/exemplo_3.png)

Minimize $\to$ $Z = 1x_1 + 2x_2 -1x_3$ <br>
$S.t:$ <br>
    $2x_1 + 1x_2 + 1x_3 \leq 14$ <br>
    $4x_1 + 2x_2 + 3x_3 \leq 28$ <br>
    $2x_1 + 5x_2 + 5x_3 \leq 30$ <br>
$x_1, x_2, x_3, x_4, x_5, x_6 \geq 0$ <br>

```python 
A = [[2, 1, 1], [4, 2, 3], [2, 5, 5]]
C = [1, 2, -1]
b = [14, 28, 30]
ineq = ["<=", "<=", "<="]
```

#### 3. Output:
```python
Press enter to continue...
Iteração: 0
Pivo: 5
Variavel entrando: y3
Variavel saindo: s3

Tabela Atual:
┏━━━━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━┓
┃ y1 ┃ y2 ┃ y3 ┃ s1 ┃ s2 ┃ s3 ┃ b  ┃
┡━━━━╇━━━━╇━━━━╇━━━━╇━━━━╇━━━━╇━━━━┩
│ 2  │ 1  │ 1  │ 1  │ 0  │ 0  │ 14 │
│ 4  │ 2  │ 3  │ 0  │ 1  │ 0  │ 28 │
│ 2  │ 5  │ 5  │ 0  │ 0  │ 1  │ 30 │
│ 1  │ 2  │ -1 │ 0  │ 0  │ 0  │ 0  │
└────┴────┴────┴────┴────┴────┴────┘
Soluçao atual:
y1: 0; y2: 0; y3: 0; s1: 14; s2: 28; s3: 30; z: 0;

Press enter to continue...

Solução:
┏━━━━━━┳━━━━━━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━━━┳━━━━┓
┃ Base ┃   y1 ┃ y2 ┃ y3 ┃ s1 ┃ s2 ┃   s3 ┃  b ┃
┡━━━━━━╇━━━━━━╇━━━━╇━━━━╇━━━━╇━━━━╇━━━━━━╇━━━━┩
│   s1 │  8/5 │  0 │  0 │  1 │  0 │ -1/5 │  8 │
│   s2 │ 14/5 │ -1 │  0 │  0 │  1 │ -3/5 │ 10 │
│   y3 │  2/5 │  1 │  1 │  0 │  0 │  1/5 │  6 │
│    z │  7/5 │  3 │  0 │  0 │  0 │  1/5 │  6 │
└──────┴──────┴────┴────┴────┴────┴──────┴────┘
Existem múltiplas soluções ótimas.

Solução Encontrada:
y1: 0
y2: 0
y3: 6
s1: 8
s2: 10
s3: 0
z: 6
```

---

#### 4. Input:
- Unbounded

Maximize $\to$ $Z = 5x_1 + 4x_2$ <br>
$S.t:$ <br>
    $1x_1 + 0x_2\leq 7$ <br>
    $1x_1 - 2x_2\leq 8$ <br>
$x_1, x_2 \geq 0$ <br>

```python 
A = [[1, 0], [1, -1]]
C = [5, 4]
b = [7, 8]
ineq = ["<=", "<="]
```

### 4. Output:
```python
Press enter to continue...
Iteração: 0
Pivo: 1
Variavel entrando: x1
Variavel saindo: s1

Tabela Atual:
┏━━━━┳━━━━┳━━━━┳━━━━┳━━━┓
┃ x1 ┃ x2 ┃ s1 ┃ s2 ┃ b ┃
┡━━━━╇━━━━╇━━━━╇━━━━╇━━━┩
│ 1  │ 0  │ 1  │ 0  │ 7 │
│ 1  │ -1 │ 0  │ 1  │ 8 │
│ -5 │ -4 │ 0  │ 0  │ 0 │
└────┴────┴────┴────┴───┘
Soluçao atual:
x1: 0; x2: 0; s1: 7; s2: 8; z: 0;

Press enter to continue...

Solução:
┏━━━━━━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━┓
┃ Base ┃ x1 ┃ x2 ┃ s1 ┃ s2 ┃  b ┃
┡━━━━━━╇━━━━╇━━━━╇━━━━╇━━━━╇━━━━┩
│   x1 │  1 │  0 │  1 │  0 │  7 │
│   s2 │  0 │ -1 │ -1 │  1 │  1 │
│    z │  0 │ -4 │  5 │  0 │ 35 │
└──────┴────┴────┴────┴────┴────┘
A solução é ilimitada (UNBOUNDED).
Nenhuma solução foi encontrada.
```

#### Programa funcionando:
![programa_completo](/imgs/complete_solution.png)
