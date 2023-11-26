from collections import defaultdict
somerecords = [dict(), dict(), dict()]

somekeys = ['key1', 'key2', 'key3']
somedict = defaultdict(list)
for somekey in somekeys:
    for row in somerecords:
        row['a'] = somekey
        somedict[somekey].append(row)
        break
print(id(somedict['key1'][0]) == id(somedict['key2'][0])) ### >>> True 
