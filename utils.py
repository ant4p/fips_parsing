import json
import pandas as pd


# функция в которую передаём датафрейм pandas и название файла для сохранения информации,
# в этой функции мы создаём иерархическую структуру файла и записываем json по конкретному МПК
def save_to_json_with_hierarchy(df, output_file):
    # создаем корневую структуру
    tree = []

    # стек для отслеживания текущих уровней
    stack = []

    for _, row in df.iterrows():
        code = row["Код"].strip()
        description = row["Описание"].strip()

        # определяем уровень вложенности по количеству точек в начале описания
        desc_cleaned = description.lstrip(".")
        dots_count = len(description) - len(desc_cleaned)
        description = desc_cleaned.strip()

        item = {"группа": code, "расшифровка": description, "подгруппы": []}

        # удаляем из стека все уровни глубже текущего
        while len(stack) > dots_count:
            stack.pop()

        if dots_count == 0:
            # основная группа - добавляем в корень
            tree.append(item)
            stack = [item]
        else:
            # добавляем как дочерний элемент к последнему элементу текущего уровня
            if stack:
                parent = stack[-1]
                parent["подгруппы"].append(item)
                # если стек был короче текущего уровня, добавляем новый уровень
                if len(stack) <= dots_count:
                    stack.append(item)

    # сохраняем в JSON файл
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)

    return tree


# функция, которая читает подклассы МПК из .xlsx файла и возвращает список этих подклассов,
# по которым будет произведен парсинг
def get_mpk_list_from_file(filename):
    df = pd.read_excel(filename, header=None)
    list_mpk_from_file = df.stack().dropna().tolist()
    return list_mpk_from_file
