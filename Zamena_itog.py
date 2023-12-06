import tkinter as tk
from tkinter import simpledialog, messagebox


def input_values(message):
    values = []
    while True:
        next_line = simpledialog.askstring("Ввод данных", message + "\nВведите 0 для завершения:")
        if next_line is None or next_line == "0":
            break
        else:
            values.append(int(next_line))
    return values


def print_values(values, label):
    output_text = f"\n\n{label} по периодам:\n"
    for key, value in enumerate(values):
        output_text += f"Период {key}: {value} тыс. руб\n"
    messagebox.showinfo(label, output_text)


def conditional_optimization(Rt, St, P):
    T = len(Rt) - 1
    output_text = f"\nДанные периода 0 считаются базовыми. Всего расчет проводится на {T} следующих периодах"
    output_text += "\n\nУсловная оптимизация:\n\n"

    r0 = Rt[0]

    cond_opt = {}
    c = 0
    F = [[0] * (T) for i in range(T)]

    for k in range(T, 0, -1):
        n = c + 1
        output_text += f"{n}-й шаг, k = {k}\n\n"
        row = {}
        for t in range(1, k + 1):
            if k == T:
                Rtt = Rt[t]
                s = Rtt
                z = (St[t] - P) + r0
                v = max(s, z)

                output_text += f"Период {t}: max({Rtt}; {St[t]} - {P} + {r0}) = {v};"
                if s >= z:
                    output_text += " - Сохраняем\n"
                    row[t] = [v, 0]
                else:
                    output_text += " - Заменяем\n"
                    row[t] = [v, 1]
                F[k - 1][t - 1] = max(s, z)
            else:
                Rtt = Rt[t] + F[k][t]
                s = Rtt
                z = (St[t] - P) + r0 + F[k][0]
                v = max(s, z)
                output_text += f"Период {t}: max({Rt[t]} + {F[k][t]}; {St[t]} - {P} + {r0} + {F[k][0]}) = {v};"
                if s >= z:
                    output_text += " - Сохраняем\n"
                    row[t] = [v, 0]
                else:
                    output_text += " - Заменяем\n"
                    row[t] = [v, 1]
                F[k - 1][t - 1] = max(s, z)
        output_text += "\n\n"
        cond_opt[k] = row
        c += 1
    max_profit = F[0][0]
    messagebox.showinfo("Условная оптимизация", output_text)
    return cond_opt, max_profit


def unconditional_optimization(cond_opt):
    output_text = "\n\nБезусловная оптимизация: \n"
    t = 1

    cond_opt = dict(sorted(cond_opt.items()))
    uncond_opt = []
    for k, s in cond_opt.items():
        output_text += f"k = {k}\n"
        output_text += f"Возраст оборудования {t} лет\n"
        if s[t][1] == 1:
            output_text += "Заменяем\n\n"
            uncond_opt.append(k)
            t = 0
        else:
            output_text += "Сохраняем\n\n"

        t += 1
    output_text += f"Таким образом, замену оборудования нужно провести в начале " + ", ".join(
        map(str, uncond_opt)) + "года\n"
    messagebox.showinfo("Безусловная оптимизация", output_text)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    St = input_values(
        "Пожалуйста, введите значения остаточной стоимости S(t), начиная с базового периода, и разделяя данные по годам с помощью Enter")
    print_values(St, "Остаточная стоимость S(t)")

    Rt = input_values(
        "Пожалуйста, введите значения дохода R(t), начиная с базового периода, и разделяя данные по годам с помощью Enter\nКоличество введенных периодов должно совпадать с предыдущим вводом")
    print_values(Rt, "Доход R(t)")

    if len(Rt) != len(St):
        messagebox.showerror("Ошибка", "Количество периодов не совпадает")
        exit()

    P = simpledialog.askinteger("Ввод данных", "Введите стоимость нового оборудования P")

    cond_optimization_result, max_profit = conditional_optimization(Rt, St, P)
    unconditional_optimization(cond_optimization_result)
    messagebox.showinfo("Максимальная прибыль", f"Максимальная прибыль составит: {max_profit}")
