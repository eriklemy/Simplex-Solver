"""
    TDE - Otimizaçao de Sistemas Lineares
    NOME: Erick Lemmy dos Santos Oliveira
    PROF: Guilherme

    Construção de programa que resolve problemas de programação linear por SIMPLEX
"""
import copy
from fractions import Fraction


class SimplexOutput:
    UniqueOptimal = 0
    MultipleOptimal = 1
    Infeasibe = 2
    Unbounded = 3
    Degeneracy = 4


class SimplexSolver:
    def __init__(self, A, b, ineq):
        self.A = A
        self.b = b
        self.C = []
        self.ineq = ineq
        self.is_minimize = None
        self.tableau = None  # Instância de SimplexTableau

    def initialize_tableau(self):
        self.tableau = SimplexTableau(self.ineq, self.is_minimize)
        self.tableau.initialize(self.A, self.b, self.C)

    def minimize(self, C):
        self.is_minimize = True
        self.C = [-1 * value for value in C]
        self.initialize_tableau()

    def maximize(self, C):
        self.is_minimize = False
        self.C = C
        self.initialize_tableau()

    def solve(self):
        max_iterations = 2 * len(self.A[0])

        input("Press enter to continue...")
        while not self.is_optimal():
            pivot = self.tableau.find_pivot()
            if pivot[1] < 0:
                return None, SimplexOutput.Unbounded

            print(f"Iteração: {self.tableau.iteration_count}")
            print(f"Pivo: {pivot[1]}")
            print(f"Variavel entrando: {self.tableau.entering[pivot[0]]}")
            print(f"Variavel saindo: {self.tableau.departing[pivot[1]]}")
            self.tableau._print_tableau()
            print(f"Soluçao atual: \n{self.get_current_solution()}")
            input("Press enter to continue...")
            self.tableau.step(pivot)

        solution = self.get_current_solution()
        if self.tableau.iteration_count >= max_iterations:
            print("O problema pode estar degenerado.")
            return solution, SimplexOutput.Degeneracy

        var = "x" if not self.is_minimize else "y"
        has_zero_x_value = any(
            value == 0 for key, value in solution.items() if key.startswith(var)
        )
        if has_zero_x_value:
            return solution, SimplexOutput.MultipleOptimal

        return solution, SimplexOutput.UniqueOptimal

    def is_optimal(self):
        return all(x >= 0 for x in self.tableau.tableau[-1][:-1])

    def get_current_solution(self):
        solution = {}
        for x in self.tableau.entering:
            if x != "b":
                departing_index = (
                    self.tableau.departing.index(x)
                    if x in self.tableau.departing
                    else -1
                )
                if departing_index >= 0:
                    solution[x] = self.tableau.tableau[departing_index][-1]
                else:
                    solution[x] = 0
        solution["z"] = self.tableau.tableau[-1][-1]

        if self.is_minimize:
            bottom_row = self.tableau.tableau[-1]
            for v in self.tableau.entering:
                if "s" in v:
                    solution[v.replace("s", "x")] = bottom_row[
                        self.tableau.entering.index(v)
                    ]
        return solution


class SimplexTableau:
    def __init__(self, ineq, prob):
        self.A = []
        self.C = []
        self.b = []
        self.ineq = ineq
        self.tableau = []
        self.entering = []
        self.departing = []
        self.is_minimize = prob
        self.iteration_count = 0

    def initialize(self, A, b, C):
        # Multiplica linha por -1 se ineq >= para transformar em <=
        for i, ineq in enumerate(self.ineq):
            if ineq == ">=":
                for j in range(len(A[i])):
                    A[i][j] *= -1 if self.is_minimize else 1
                b[i] *= -1 if self.is_minimize else 1

        self.A = [[Fraction(x) for x in a] for a in A]
        self.b = [Fraction(x) for x in b]
        self.C = [-Fraction(x) if self.is_minimize else -Fraction(x) for x in C]

        self.update_enter_depart(self.get_matrixAb())
        self.create_tableau()
        self.ineq = ["="] * len(self.b)
        self.update_enter_depart(self.tableau)

    def create_tableau(self):
        self.tableau = copy.deepcopy(self.A)
        self.add_slack_and_artificial_variables()
        self.tableau.append(self.C + [0] * (len(self.b) + 1))

    def add_slack_and_artificial_variables(self):
        """Add slack & artificial variables to matrix A to transform all inequalities to equalities."""
        slack_vars = self._generate_identity(len(self.tableau))
        for i in range(len(slack_vars)):
            self.tableau[i] += slack_vars[i]
            if self.ineq[i] == ">=":
                self.tableau[i].append(-1)
            elif ">=" in self.ineq:
                self.tableau[i].append(0)
            self.tableau[i] += [self.b[i]]

    def find_pivot(self):
        enter_index = self.get_entering_var()
        depart_index = self.get_departing_var(enter_index)
        return [enter_index, depart_index]

    def step(self, pivot_index):
        j, i = pivot_index

        pivot = self.tableau[i][j]
        self.tableau[i] = [element / pivot for element in self.tableau[i]]
        for index, row in enumerate(self.tableau):
            if index != i:
                row_scale = [y * self.tableau[index][j] for y in self.tableau[i]]
                self.tableau[index] = [
                    x - y for x, y in zip(self.tableau[index], row_scale)
                ]

        self.departing[i] = self.entering[j]
        self.iteration_count += 1

    def update_enter_depart(self, matrix):
        self.entering = []
        self.departing = []

        for i in range(len(matrix[0])):
            if i < len(self.A[0]):
                prefix = "x" if not self.is_minimize else "y"
                self.entering.append(f"{prefix}{i+1}")
            elif i < len(matrix[0]) - 1:
                self.entering.append(f"s{i + 1 - len(self.A[0])}")
                self.departing.append(f"s{i + 1 - len(self.A[0])}")
            else:
                self.entering.append("b")

    def get_matrixAb(self):
        matrix = [row + [bi] for row, bi in zip(self.A, self.b)]
        return matrix

    def get_entering_var(self):
        """Get the 'most negative' element of the bottom row."""
        bottom_row = self.tableau[-1]
        most_neg_ind = bottom_row.index(min(bottom_row))
        return most_neg_ind

    def get_departing_var(self, entering_index):
        min_ratio = float("inf")
        min_ratio_index = -1
        for index, row in enumerate(self.tableau):
            if row[entering_index] > 0:
                ratio = row[-1] / row[entering_index]
                if 0 < ratio < min_ratio:
                    min_ratio = ratio
                    min_ratio_index = index
        return min_ratio_index

    def _generate_identity(self, n):
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    def _print_tableau(self):
        print(f"\n┌───{self.entering[0]}───", end="")
        for val in self.entering[1:]:
            if val == "b":
                print(f"┬────{val}──", end="")
            else:
                print(f"┬───{val}───", end="")
        print("─┬────────┐")
        for num, row in enumerate(self.tableau):
            print("│", end=" ")
            for index, val in enumerate(row):
                print(" {:^5} │".format(str(val)), end=" ")
            if num < (len(self.tableau) - 1):
                print(f"  {self.departing[num]}   │")
            elif num == len(self.tableau) - 1:
                print("   z   │")
            else:
                print("       │")

        print("└────────", end="")
        for _ in self.entering:
            print("┴────────", end="")
        print("┘")


class UserInterface:
    def input_matrix(self):
        print("Insira a matriz de coeficientes (A):")
        print("Insira o número de equações (linhas):")
        num_equations = int(input())
        print("Insira o número de variáveis (colunas):")
        num_variables = int(input())
        A = []
        for i in range(num_equations):
            print(f"Insira os coeficientes da equação {i + 1} separados por espaço:")
            coefficients = list(map(float, input().split()))
            A.append(coefficients)

        # Leitura do vetor de coeficientes da função objetivo (C)
        print("Insira os coeficientes da função objetivo (C) separados por espaço:")
        C = list(map(float, input().split()))

        # Leitura do vetor de constantes (b)
        print("Insira os valores do vetor de constantes (b) separados por espaço:")
        b = list(map(float, input().split()))

        print("Insira os valores as inequacoes (>=, <=, =) separados por espaço:")
        ineq = list(map(str, input().split()))
        return A, C, b, ineq

    def print_solution(self, solution):
        print("Solução encontrada:")
        for var, value in solution.items():
            print(f"{var}: {value}")
        print("\n")

    def print_iteration(self, tableau):
        print("Número de iterações:", tableau.iteration_count)
        print("Status da tabela do Simplex:")
        tableau._print_tableau()

    def print_uniqueOptimal(self):
        print("A soluçao é otima")

    def print_multipleOptimal(self):
        print("A soluçao encontrada é otima pois (Zj - Cj >= 0)")
        print("Porem como há uma variavel basica nula.")
        print("Exitem infinitas solucoes possiveis para x_n")

    def print_degeneracy(self):
        print("Problema sofre de degeneração.")

    def print_infeasibility(self):
        print("Problema é inviável.")

    def print_unbounded(self):
        print("Soluçao ilimitada (Unbounded). O Problema não possui fronteira")
        print("Todos os elementos da coluna que entra na base sao")
        print("menores que ZERO ou NULOS.")

    def simplex_show(self, tableau, is_minimize, ineq=None):
        objective = "Maximize -> Z: " if not is_minimize else "Minimize -> C:"
        print(objective, end="")

        for i, value in enumerate(tableau.tableau[-1]):
            # if is_minimize:
            value *= -1
            sign = "+" if value >= 0 and i > 0 else "\b"
            if i < len(tableau.tableau[-1]) - 1:
                print(f"{sign} {value}x{i+1} ", end="")

        print("\nSubject to:")
        for i, values in enumerate(tableau.tableau[0:-1]):
            for j, value in enumerate(values[0:-1]):
                sign = "+" if value >= 0 and j > 0 else "\b"
                print(f" {sign} {value}x{j+1}", end="")

            ineq = tableau.ineq if ineq is None else ineq
            b = -tableau.b[i] if tableau.b[i] < 0 else tableau.b[i]
            print(f" {ineq[i]} {b}")

        for i in range(len(tableau.tableau[0]) - 1):
            comma = "," if i <= len(tableau.tableau) - 1 else ""
            print(f"  x{i+1}{comma}", end="")
        print(" >= 0\n\n")


def main():
    # Dados de exemplo para a matriz A, vetor C e vetor b
    A = [[2, 1], [2, 3], [3, 1]]
    C = [3, 2]
    b = [18, 42, 24]
    # A = [[2, 1, 1], [4, 2, 3], [2, 5, 5]]
    # C = [1, 2, -1]
    # b = [14, 28, 30]
    ineq = ["<=", "<=", "<="]

    ui = UserInterface()
    # A, C, b, ineq = ui.input_matrix()
    solver = SimplexSolver(A, b, ineq)

    result = None
    prob = input("Deseja minimizar ou maximizar o problema (Min/Max): ").upper()
    is_minimize = True if prob in "MINIMIZE" else False
    if is_minimize:
        solver.minimize(C)
        ui.simplex_show(solver.tableau, is_minimize, ineq)
        ui.simplex_show(solver.tableau, not is_minimize)
        solution, result = solver.solve()
    else:
        solver.maximize(C)
        ui.simplex_show(solver.tableau, is_minimize, ineq)
        ui.simplex_show(solver.tableau, is_minimize)
        solution, result = solver.solve()

    if result == SimplexOutput.Infeasibe:
        ui.print_infeasibility()
    elif result == SimplexOutput.UniqueOptimal:
        ui.print_iteration(solver.tableau)
        ui.print_uniqueOptimal()
        ui.print_solution(solution)
    elif result == SimplexOutput.MultipleOptimal:
        ui.print_iteration(solver.tableau)
        ui.print_multipleOptimal()
        ui.print_solution(solution)
    elif result == SimplexOutput.Unbounded:
        ui.print_unbounded()
    elif result == SimplexOutput.Degeneracy:
        ui.print_degeneracy()


if __name__ == "__main__":
    main()
