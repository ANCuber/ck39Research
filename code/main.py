import process as worker

s = input("輸入你想生成的數學算式:")
signs = ["大於等於","小於等於","等於","大於","小於"]
k = 5
for i in range(0,5):
    if(s.find(signs[i])>=0):
        k = i
        break
st = worker.processed(s,k)
st = worker.retrived(st)
result = worker.generate(st,k)
print(result)

print(worker.rev(result,s))



