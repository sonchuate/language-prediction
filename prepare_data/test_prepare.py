with open('output.txt','r',encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
with open('log.txt', 'w', encoding='utf-8') as f:
    for line in lines:
        if len(line) < 3: continue
        x, y = line.split('\t')
        x = x.split(' ')
        y = y.split(' ')
        for w, l in zip(x,y):
            # print(w, l)
            f.write(f'{w}\t{l}\n')