import process as worker

s = input("輸入你的東西:")

st = worker.processed(s)
print(st)

st = worker.retrived(st)
print(st)
result = worker.generate(st)
result = result[0]
print(result)
result = result.strip("[var50]")

print(worker.rev(result,s))



