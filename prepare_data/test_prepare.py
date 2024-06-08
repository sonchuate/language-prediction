with open('output.txt','r',encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
max_len = 0
with open('log.txt', 'w', encoding='utf-8') as f:
    for line in lines:
        if len(line) < 3: continue
        x, y = line.split('\t')
        max_len = max(max_len, len(x))
        x = x.split(' ')
        y = y.split(' ')
        for w, l in zip(x,y):
            # print(w, l)
            f.write(f'{w}\t{l}\n')
print(max_len)