# Simplex-solver
Programa de Resolução de Problemas de Programação Linear por Método Simplex

### Versoes
    - Python: completo
    - Rust: em desenvolvimento (aprendizado).

## TDE - Otimização de Sistemas Lineares
- **NOME:** Erick Lemmy dos Santos Oliveira
- **PROF:** Guilherme

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

### Exemplos:

- Minimização e Maximização de casos otimos:

#### Input:
1. Minimize $\to$ $C = 3x_1 + 2x_2$
$ S.t:$
    $2x_1 + 1x_2\leq 18$
    $2x_1 + 3x_2\leq 42$
    $3x_1 + 1x_2\leq 24$
$x_1, x_2, x_3, x_4, x_5 \geq 0$

```python 
C = [3, 2]                   # objetivo
A = [[2, 1], [2, 3], [3, 1]] # vetor base
b = [18, 42, 24]             # restricao
ineq = ["<=", "<=", "<="]
```

#### Output:


---

2. Maximize $\to$ $Z = 1x_1 + 2x_2 -1x_3$
$ S.t:$
    $2x_1 + 1x_2 + 1x_3 \leq 18$
    $4x_1 + 2x_2 + 3x_3 \leq 42$
    $2x_1 + 5x_2 + 5x_3 \leq 24$
$x_1, x_2, x_3, x_4, x_5, x_6 \geq 0$

```python 
A = [[2, 1, 1], [4, 2, 3], [2, 5, 5]]
C = [1, 2, -1]
b = [14, 28, 30]
ineq = ["<=", "<=", "<="]
```

#### Output:

---

#### Input:
- Unbounded e Inviavel

3. Maximize $\to$ $Z = 5x_1 + 4x_2$
$ S.t:$
    $1x_1 + 0x_2\leq 7$
    $1x_1 - 2x_2\leq 8$
$x_1, x_2 \geq 0$

```python 
A = [[1, 0], [1, -1]]
C = [5, 4]
b = [7, 8]
ineq = ["<=", "<=", "<="]
```
