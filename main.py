import os
import time


from dotenv import load_dotenv
from parser_mpk import get_mpk_data
from script import get_json_files, union_json_files
from transformation_to_xlsx import convert_json_to_xlsx
from utils import get_mpk_list_from_file, save_to_json_with_hierarchy

load_dotenv()


# основная функция, точка входа
def main():
    filename = os.getenv("INPUT_MPK_FILENAME")

    # достаём список МПК для парсинга из .xlsx файла
    list_mpk_from_file = get_mpk_list_from_file(filename)

    edition = os.getenv("EDITION")
    folder_path_json = os.getenv("FOLDER_WITH_JSON_PATH")

    # проходимся по списку МПК
    for subclass in list_mpk_from_file:
        # указываем место хранения и имя нового создаваемого json файла
        output_file = f"{folder_path_json}{subclass}.json"
        # используем парсер для получения данных по конкретному МПК
        mpk_data = get_mpk_data(subclass, edition)
        # сохраняем данные согласно иерархии в json формате
        save_to_json_with_hierarchy(mpk_data, output_file)
        # делаем таймаут, чтобы не перегружать сервер
        time.sleep(1)

    output_json_file = os.getenv("OUTPUT_JSON_FILE")

    # получаем список всех сохранённых json файлов
    json_file_list = get_json_files(folder_path_json)
    # объединяем в один общий json файл при необходимости
    union_json_files(json_file_list, output_json_file, folder_path_json)

    folder_path_xlsx = os.getenv("FOLDER_WITH_XLSX_PATH")

    # преобразуем общий json файл в файлы xlsx - 3 варианта
    convert_json_to_xlsx(output_json_file, folder_path_xlsx)


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execute = end_time - start_time
    print(f'{execute} seconds.')
