import os
import requests
import pandas as pd
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

# функция, которая принимает значение подкласса и год для поиска
# сохраняет в bs4 набор данных, очищает их и возвращает датафрейм pandas
def get_mpk_data(subclass, edition=os.getenv("EDITION")):
    base_url = os.getenv("BASE_URL")

    params = {"view": "search", "edition": edition, "symbol": subclass}

    try:
        response = requests.get(base_url, params=params, timeout=None)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("div", class_="row", attrs={"data-symbol": True})

        data = []

        for row in rows:
            code = row.find("div", class_="mpk_section").get_text(strip=True)
            description = row.find("div", class_="mpk_section_note").get_text(
                strip=True
            )

            # удаляем лишние символы и форматируем код
            code = code.replace("\u00a0", " ").strip()

            data.append(
                {
                    "Код": code,
                    "Описание": description,
                }
            )
        df = pd.DataFrame(data)
        df = df[df["Код"].str.startswith(subclass)]
        dataframe = df.drop_duplicates().sort_values("Код")
        return dataframe

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None
