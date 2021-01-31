import requests, sys, uuid

auth_params = {
    'key':"KEY",
    'token':"TOKEN",
}

base_url = "https://api.trello.com/1/{}"
board_id = "board_id"

def get_column_data():
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    return column_data

def read():
    for column in get_column_data():
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print("Название колонки:", column['name'], f"\nКол-во задач: {len(task_data)}")
        if not task_data:
            print('\t' + 'Нет задач')
            continue
        for task in task_data:
            print('\t' + task['name'])

def create(name, column_name):
    for column in get_column_data():
        if column['name'] == column_name:
            requests.post(base_url.format('cards'), data={'name':name, 'idList':column['id'], **auth_params})
            break

def delete(name, column_name):
    for column in get_column_data():
        if column['name'] == column_name:
            arr = []
            task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
            for task in task_data:
                if task['name'] == name:
                    arr.append(task)
            if len(arr) > 1:
                i = 0
                for task in arr:
                    i += 1
                    print(f"Номер: {i} Имя: {task['name']} Ссылка: {task['url']}")
                requests.delete(base_url.format('cards') + '/' + arr[int(input('Найдены несколько задач с одинаковыми именами!\nВведите номер задачи: ')) - 1]['id'], data={**auth_params})
            else:
                requests.delete(base_url.format('cards') + '/' + arr[0]['id'], data={**auth_params})

def create_column(name):
    list_id = str(uuid.uuid1())
    requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name':name,'id':list_id, **auth_params})

def move(name, column_name):
    task_id = None
    arr = {}
    for column in get_column_data():
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                arr[column['name']] = task
    if len(arr) > 1:
        i = 0
        arr2 = []
        for key in arr:
            i += 1
            print(f"Номер: {i} Имя: {arr[key]['name']} Ссылка: {arr[key]['url']} Колонка: {key}")
            arr2.append(arr[key])
        task_id = arr2[int(input('Найдены несколько задач с одинаковыми именами!\nВведите номер задачи: ')) - 1]['id']
    elif len(arr) == 1:
        task_id = arr[0]['id']
    elif len(arr) == 0:
        print('Нет задачи с таким именем!')
        return

    for column in get_column_data():
        if column['name'] == column_name:
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value':column['id'], **auth_params})
            break

def helper():
    print('Создать колонку - python test.py create_column "имя колонки"\nСоздать задачу - python test.py create "имя задачи" "имя колонки"\nУдалить задачу - python test.py delete "имя задачи" "имя колонки"\nПереместить задачу - python test.py move "имя задачи" "имя колонки"')

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == 'help':
        helper()
    elif len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])
    elif sys.argv[1] == 'delete':
        delete(sys.argv[2], sys.argv[3])
