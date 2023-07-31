from pprint import pprint
import re
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
p = re.compile(r"(\+7|8) ?\(?(\d{3})\)?[ -]?(\d{3})[ -]?(\d{2})[ -]?(\d{2})(:? ?\(?(?:доб\.?) (\d{4}))?")
# компилирую регулярное выражение

for i in contacts_list:
    for j, k in enumerate(i):
        a = k.split(" ", 1)
        if ((j < 3 and j >= 0) and len(a) > 1):
        # если фамилия имя или отчество состоит больше, чем из одного слова
            i[j] = a[0] # в текущем поле оставляем только первое слово
            i[j + 1] = a[1] # оставшиеся слова переносим в следующее поле (например из фамилии в имя или из имени в отчество)
        elif (j == 5):

            # приводим телефоны к нужному формату
            res = p.findall(k)
            if (len(res) == 0): continue # если телефона в этой строке нет
            res = res[0] # избавляемся от вложенности кортежа в массив
            i[j] = f"+7({res[1]}){res[2]}-{res[3]}-{res[4]}{(' доб.' + res[6]) if res[6] != '' else ''}"
            # помещаем в ячейку телефона значение в нужном формате

contacts_list.sort() # сортируем элементы для того,
# чтобы одинаковые фио были друг за другом
# (так просто легче проверять)

to_remove = [] # тут будут храниться строки,
# которые после цикла будут не нужны (дубликаты)

for i, j in enumerate(contacts_list):
    if not (i != len(contacts_list) - 1 and j[0] == contacts_list[i + 1][0]
    and j[1] == contacts_list[i + 1][1]): continue
    # если текущий элемент массива не является последним
    # и текущее ИО не совпадает со следующим
    # то ничего не делаем

    for k, l in enumerate(j):
        if not (k != len(j) - 1 and l == "" and contacts_list[i + 1][k] != ""): continue
        # если текущая клетка таблицы
        # пустая, а под ней (на следующей строке) не пустая

        contacts_list[i][k] = contacts_list[i + 1][k]
        # то в текущую клетку записываем значение из следующей строки

    to_remove.append(i + 1) # и отмечаем следующую строку как дубликат

for i, j in enumerate(to_remove):
    contacts_list.pop(j - i) # избавляемся от дубликатов
    # j - i потому что при удалении элемента, индексы смещаются на 1
    # а i показывает, сколько удалений мы произвели
    # значит, отнимая от изначального индекса количество удалений
    # получим новый индекс искомого элемента

# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
    csv.writer(f, delimiter=',').writerows(contacts_list)
    # Вместо contacts_list подставьте свой список