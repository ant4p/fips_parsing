import json
import pandas as pd


# функция, принимающая json файл, преобразует вложенную структуру словарей
# с подгруппами в плоскую таблицу с сохранением иерархии.
def flat_tree_v1(node, parent_group=None, level=0, rows=None):
    if rows is None:
        rows = []

    rows.append(
        {
            "Группа": node["группа"],
            "Родительская группа": parent_group,
            "Уровень": level,
            "Расшифровка": node["расшифровка"],
        }
    )

    for child in node.get("подгруппы", []):
        flat_tree_v1(child, parent_group=node["группа"], level=level + 1, rows=rows)

    return rows

# функция, принимающая json файл, преобразует вложенную структуру словарей
# с подгруппами в плоскую таблицу с сохранением иерархии и визуальными отступами.
def flat_tree_with_indent_v2(node, rows=None, indent=0):
    if rows is None:
        rows = []

    rows.append(
        {
            "Группа": " -- -- " * indent + node["группа"],
            "Расшифровка": " -- -- " * indent + node["расшифровка"],
        }
    )

    for child in node.get("подгруппы", []):
        flat_tree_with_indent_v2(child, rows, indent + 1)

    return rows

# функция, принимающая json файл, преобразует вложенную структуру словарей
# с подгруппами в плоскую таблицу с сохранением иерархии и показом path к каждой группе.
def flat_tree_with_path_v3(node, path=None, rows=None):
    if path is None:
        path = []
    if rows is None:
        rows = []

    current_path = path + [node["группа"]]
    rows.append(
        {
            "Полный путь": " → ".join(current_path),
            "Группа": node["группа"],
            "Уровень": len(current_path) - 1,
            "Расшифровка": node["расшифровка"],            
        }
    )

    for child in node.get("подгруппы", []):
        flat_tree_with_path_v3(child, current_path, rows)

    return rows

# функция, принимающая json файл, преобразует его в файл xlsx
def convert_json_to_xlsx(output_json_file, folder_path_xlsx):
    with open(output_json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_rows = []
    all_rows_v2 = []
    all_rows_v3 = []

    for item in data:
        all_rows.extend(flat_tree_v1(item))
        all_rows_v2.extend(flat_tree_with_indent_v2(item))
        all_rows_v3.extend(flat_tree_with_path_v3(item))

    df = pd.DataFrame(all_rows)
    df_v2 = pd.DataFrame(all_rows_v2)
    df_v3 = pd.DataFrame(all_rows_v3)

    excel_file = df.to_excel(f"{folder_path_xlsx}union_v1.xlsx", index=False, engine="openpyxl")
    excel_file_v2 = df_v2.to_excel(f"{folder_path_xlsx}union_v2.xlsx", index=False, engine="openpyxl")
    excel_file_v3 = df_v3.to_excel(f"{folder_path_xlsx}union_v3.xlsx", index=False, engine="openpyxl")
    return excel_file, excel_file_v2, excel_file_v3
