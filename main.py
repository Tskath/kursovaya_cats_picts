import json
from urllib.parse import quote
import requests

group_name = "AIEPYAPI-162"
text = input("Введите текст для картинки: ").strip()
token = input("Введите токен Яндекс.Диска: ").strip()

headers = {"Authorization": "OAuth " + token}

print("1. Создаем папку на Яндекс.Диске...")
requests.put(
    "https://" + "cloud-api.yandex.net" + "/v1/disk/resources",
    headers=headers,
    params={"path": group_name},
    timeout=15
)

print("2. Скачиваем картинку кота (ждем до 60 сек)...")
url_cat = "https://" + "cataas.com" + "/cat" + "/says/" + quote(text) + "?type=small"
image_data = requests.get(url_cat, timeout=60).content

print("3. Загружаем картинку на Яндекс.Диск...")
file_name = text + ".jpg"
upload_res = requests.get(
    "https://" + "cloud-api.yandex.net" + "/v1/disk/resources/upload",
    headers=headers,
    params={"path": group_name + "/" + file_name, "overwrite": "true"},
    timeout=15
)
upload_url = upload_res.json()["href"]
requests.put(upload_url, files={"file": image_data}, timeout=30)

print("4. Сохраняем отчет в result.json...")
info = [{"file_name": file_name, "size": len(image_data)}]
with open("result.json", "w", encoding="utf-8") as file:
    json.dump(info, file, ensure_ascii=False, indent=4)

print("Готово! Проверяйте Яндекс.Диск и файл result.json")