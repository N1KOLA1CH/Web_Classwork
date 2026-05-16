import requests

url = 'http://localhost:8080/api/v2/jobs'

print('Получение списка всех работ (get)')
response = requests.get(url)
print(response.json())

print('Корректное добавление новой работы (post)')
new_job = {
    'team_leader': 1,
    'job': 'Rabotq',
    'work_size': 48,
    'collaborators': '2, 3, 4',
    'is_finished': False
}
response = requests.post(url, json=new_job)
print(response.json())
created_job_id = response.json().get('id')

print(f'Получение одной работы по id {created_job_id} (get)')
if created_job_id:
    response = requests.get(f'{url}/{created_job_id}')
    print(response.json())
else:
    print('Работы не существует')

print('Получение несуществующей работы (get)')
response = requests.get(f'{url}/999')
print(response.json())

print('Добавление работы с пустым полем (post)')
invalid_job = {
    'team_leader': 2,
    'work_size': 12,
    'collaborators': '5',
    'is_finished': True
}
response = requests.post(url, json=invalid_job)
print(response.json())

print(f'Удаление созданной работы по id {created_job_id} (delete)')
if created_job_id:
    response = requests.delete(f'{url}/{created_job_id}')
    print(response.json())
else:
    print('Нечешо удалять')
