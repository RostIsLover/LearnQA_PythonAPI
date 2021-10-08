import requests
import json
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"
ready_status = "Job is ready"
not_ready_status = "Job is NOT ready"

# 1. Создаём задачу
response = requests.get(url)
obj_start = json.loads(response.text)
token = obj_start["token"]
seconds = obj_start["seconds"]
print(f"Задача создана: {response.text}")

# 2. Отправляем запрос с token ДО того, как задача готова, убеждался в правильности поля status
response = requests.get(url, params={"token": token})
obj_mid = json.loads(response.text)
if obj_mid["status"] == not_ready_status:
    print(f"Статус до выполнения задачи отображается верно: {obj_mid['status']}")

# 3. Ждём нужное количество секунд с помощью функции time.sleep()
print(f"Ждём выполенения {seconds} сек")
time.sleep(seconds)

# 4. Отправляем запрос c token ПОСЛЕ того, как задача готова, убеждался в правильности поля status и наличии поля result
response = requests.get(url, params={"token": token})
obj_end = json.loads(response.text)

if "result" in obj_end and obj_end["status"] == ready_status:
    print(f"Статус после выполнения задачи отображается верно: {obj_end['status']}")

