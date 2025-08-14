from pathlib import Path
import json


# функция, принимающая путь к папке в которую попали созданные парсером json файлы
# возвращает список json файлов, находящихся в папке
def get_json_files(folder_path):
    folder = Path(folder_path)
    if not folder.is_dir():
        raise ValueError(
            f"Указанный путь '{folder_path}' не является папкой или не существует."
        )
    json_files_list = [file.name for file in folder.glob("*.json")]
    return json_files_list


# функция, принимающая список json файлов, наименование файла для объединения и
# путь к папке - возвращает один объединённый json файл
def union_json_files(json_files_list, output_json_file, folder_path):
    files = json_files_list

    union_json_data = []

    for file in files:
        with open(f"{folder_path}{file}", "r", encoding="utf-8") as f:
            data = json.load(f)
            union_json_data.extend(data)

    # сохраняем объединённый JSON в новый файл
    with open(f"{output_json_file}", "w", encoding="utf-8") as f_out:
        json.dump(union_json_data, f_out, ensure_ascii=False)

    print(f"Файлы успешно объединены в новый json file - {output_json_file}")
    return f"{output_json_file}"
