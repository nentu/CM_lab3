from solver.equation import *
from sympy.abc import x

nl = '\n'

tab = '\t'

def r(a, k=3):
    return str(round(a, k))


def newton_cote(formula, a, b, k):
    res, X, Y, _ = generalMethod(formula, a, b, k)
    return f'''Вычислим интеграл на отрезке ({a}, {b}) заданной функции по формуле Ньютона – Котеса при k = {k}.
Для начала разобьём наш отрезок (a, b) на {k} частей и в каждой точке вычислим функцию.{nl}
{nl.join([r(x) + tab + r(y) for x, y in zip(X, Y)])}.{nl} Затем скалярно перемножим вектор значений функций на вектор коэффициентов
Котеса для с^{k}_i. Полученная сумма и будет равна нашему интегралу. {nl}Ответ = {res}'''


def rectangle(formula, a, b, n):
    parts = np.linspace(a, b, n + 1)
    res = solve(formula, center_rectangle, a, b, n)
    X = list()
    Y = list()
    Z = list()
    for i in range(len(parts) - 1):
        X.append((parts[i] + parts[i + 1]) / 2)
        Y.append(formula.subs(x, X[-1]).evalf())
        Z.append(Y[-1] * (b - a) / n)
    return f'''Вычислим интеграл на отрезке ({a}, {b}) заданной функции по методу средних прямоугольников при n = {n}.
    Для начала разобьём наш отрезок (a, b) на {n} частей и в каждой из них вычислим значение функции в середине отрезка.
    Затем умножим на ширину отрезка = {r((b - a) / n)}{nl}
    {nl.join([r(x) + tab + r(y) + tab + r(z) for x, y, z in zip(X, Y, Z)])}.{nl} Затем сложим площади фигур и полученная сумма и будет равна нашему интегралу. {nl}Ответ = {r(res)}'''


def trapecia(formula, a, b, n):
    parts = np.linspace(a, b, n + 1)
    res = solve(formula, trapezoid, a, b, n)
    X = list()
    Y = list()
    Z = list()
    for a, b in zip(parts[:-1], parts[1:]):
        X.append(f'({r(a)}, {r(b)})')
        Y.append(f'({r(formula.subs(x, a).evalf())}, {r(formula.subs(x, b).evalf())})')
        Z.append((formula.subs(x, a).evalf() + formula.subs(x, b).evalf()) * (b - a) / 2)

    return f'''Вычислим интеграл на отрезке ({a}, {b}) заданной функции по методу трапеций при n = {n}.
Для начала разобьём наш отрезок (a, b) на {n} частей и в каждой из них вычислим значение функции на краях отрезка a' и b'.
Затем по формуле площади трапеции найдём площадь и сложим их, получив конечный результат.
{nl.join([x + tab + y + tab + r(z) for x, y, z in zip(X, Y, Z)])}.{nl}
Ответ = {r(res)}'''


def simsonDoc(formula, a, b, n):
    parts = np.linspace(a, b, n + 1)
    resMain = solve(formula, trapezoid, a, b, n)
    X = list()
    Y = list()
    F = list()
    Z = list()
    for a, b in zip(parts[:-1], parts[1:]):
        res, X1, Y1, interpolF = generalMethod(formula, a, b, 3)
        X.append('(' + ', '.join([r(i) for i in X1]) + ')')
        Y.append('(' + ', '.join([r(i) for i in Y1]) + ')')
        F.append(latex(interpolF))
        Z.append(res)

    return f'''Вычислим интеграл на отрезке ({a}, {b}) заданной функции по методу Симпсона при n = {n}.
    Для начала разобьём наш отрезок (a, b) на {n} частей и в каждой из них вычислим значение функции на краях отрезка (a' и b') и в середина'.
    Посчитаем интерполяционный многочлен Лагранжа через 3 точки (у нас получится парабола).
    Затем найдём площадь под параболой, для этого проинтегрируем отдельно каждый многочлен в переделах (a', b'). Сложим полученные площади, получив конечный результат.
    {nl.join([x + tab + y + tab + f + tab + r(z) for x, y, f, z in zip(X, Y, F, Z)])}.{nl}
    Ответ = {r(resMain)}'''


if __name__ == '__main__':
    formula = formulas[1]
    print(f'По заданию предлагается вычислить интеграл ${latex(formula)}$ разными методам и сравнить результаты')
    print(f'''Для начала честно вычислим интеграл по формуле Ньютона-Лейбница. Первообразная F(x)= ${latex(formula.integrate(x))}$. 
    Тогда сам интеграл равен F(b) - F(a) = {integral(formula, 0, 2)}''')
    print(newton_cote(formula, 0, 2, 6))
    print(rectangle(formula, 0, 2, 10))
    print(trapecia(formula, 0, 2, 10))
    print(simsonDoc(formula, 0, 2, 10))
