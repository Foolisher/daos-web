import datetime
from filecmp import cmp
import json


obj = json.loads('{"name":"wg", "age":[23,24,25]}', encoding='utf-8')
print(obj['age'])


print(json.loads('[{"error":"hello"}]', encoding='utf-8'))

print("1  2 3 4".split(" "))

l=list()
l.append({"id": 1})
l.append({"id": 2})
l.sort(key=lambda o:o['id'], reverse=True)


print(l)

# print("hello %s", (greed))