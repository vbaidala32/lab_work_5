import numpy as np
import sympy as sp
import tkinter as tk
from tkinter import messagebox


# Функція для отримання математичної функції
def get_user_function(function_str):
    try:
        x = sp.symbols('x')
        function_sympy = sp.sympify(function_str)
        if x not in function_sympy.free_symbols:
            raise ValueError("Функція повинна містити змінну 'x'.")
        return function_sympy, sp.lambdify(x, function_sympy, "numpy")
    except (sp.SympifyError, ValueError) as error:
        messagebox.showerror("Помилка введення", f"Помилка введення: {error}")
        return None, None


# Метод бісекції
def bisection_method(function, interval_start, interval_end, tolerance):
    if function(interval_start) * function(interval_end) >= 0:
        return "Метод бісекції не підходить для даного інтервалу"

    while (interval_end - interval_start) > tolerance * 2:
        midpoint = (interval_start + interval_end) / 2
        if function(midpoint) == 0.0:
            return midpoint
        elif function(interval_start) * function(midpoint) < 0:
            interval_end = midpoint
        else:
            interval_start = midpoint

    return (interval_start + interval_end) / 2


# Метод Ньютона
def newton_method(function, derivative_function, initial_guess, tolerance):
    current_x = initial_guess
    while True:
        function_value = function(current_x)
        derivative_value = derivative_function(current_x)
        if derivative_value == 0:
            return "Похідна дорівнює нулю. Метод Ньютона не може бути застосований."
        next_x = current_x - function_value / derivative_value
        if abs(next_x - current_x) < tolerance:
            return next_x
        current_x = next_x


# Виконання обчислень
def calculate_roots():
    function_str = entry_function.get()
    method = method_var.get()
    tolerance = float(entry_tolerance.get())

    user_function_sympy, user_function = get_user_function(function_str)
    if user_function is None:
        return

    x = sp.symbols('x')
    user_function_derivative_sympy = sp.diff(user_function_sympy, x)
    user_function_derivative = sp.lambdify(x, user_function_derivative_sympy, "numpy")

    x_values = [i * 0.5 for i in range(-100, 100)]
    sign_change_intervals = [
        (x_values[i], x_values[i + 1])
        for i in range(len(x_values) - 1)
        if user_function(x_values[i]) * user_function(x_values[i + 1]) < 0
    ]

    results_text.delete("1.0", tk.END)
    results_text.insert(tk.END, f"Обчислена похідна функції f(x): f'(x) = {user_function_derivative_sympy}\n\n")

    integer_roots = [
        int(root) for root in sp.solveset(user_function_sympy, x, domain=sp.S.Reals) if root.is_integer
    ]
    if integer_roots:
        results_text.insert(tk.END, f"Цілі корені функції f(x): {integer_roots}\n\n")
    else:
        results_text.insert(tk.END, "Цілих коренів функції f(x) немає.\n\n")

    for idx, (interval_start, interval_end) in enumerate(sign_change_intervals):
        if method == "Метод бісекції":
            root = bisection_method(user_function, interval_start, interval_end, tolerance)
            if isinstance(root, str):
                results_text.insert(tk.END, f"Корінь {idx + 1} (Метод бісекції): {root}\n")
            else:
                results_text.insert(tk.END, f"Корінь {idx + 1} (Метод бісекції): {root:.4f}\n")
        elif method == "Метод Ньютона":
            midpoint = (interval_start + interval_end) / 2
            root = newton_method(user_function, user_function_derivative, midpoint, tolerance)
            if isinstance(root, str):
                results_text.insert(tk.END, f"Корінь {idx + 1} (Метод Ньютона): {root}\n")
            else:
                results_text.insert(tk.END, f"Корінь {idx + 1} (Метод Ньютона): {root:.4f}\n")


if __name__ == "__main__":
    # Інтерфейс Tkinter
    root = tk.Tk()
    root.title("Пошук коренів функції")

    # Поле для введення функції
    tk.Label(root, text="Введіть функцію f(x):").grid(row=0, column=0)
    entry_function = tk.Entry(root, width=30)
    entry_function.grid(row=0, column=1)

    # Поле для введення точності
    tk.Label(root, text="Введіть точність (наприклад, 0.0001):").grid(row=1, column=0)
    entry_tolerance = tk.Entry(root, width=10)
    entry_tolerance.grid(row=1, column=1)

    # Вибір методу
    method_var = tk.StringVar(value="Метод бісекції")
    tk.Label(root, text="Оберіть метод:").grid(row=2, column=0)
    tk.Radiobutton(root, text="Метод бісекції", variable=method_var, value="Метод бісекції").grid(row=2, column=1, sticky="w")
    tk.Radiobutton(root, text="Метод Ньютона", variable=method_var, value="Метод Ньютона").grid(row=3, column=1, sticky="w")

    # Кнопка для запуску обчислень
    button_calculate = tk.Button(root, text="Обчислити корені", command=calculate_roots)
    button_calculate.grid(row=4, column=0, columnspan=2)

    # Поле для виведення результатів
    results_text = tk.Text(root, height=15, width=50)
    results_text.grid(row=5, column=0, columnspan=2)

    root.mainloop()
