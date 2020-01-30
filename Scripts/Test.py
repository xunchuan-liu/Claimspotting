import re

l = ["this is a dog", "this is a very fluffy dog", "this is a grey dog"]
for s in l:
    res = len(re.findall(r'\w+', s))
    if res <= 5:
        l.remove(s)

print(l)