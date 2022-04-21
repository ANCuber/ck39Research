
import torch
import numpy

n = int(input())
x =[]
ans = []
for i in range(n):
    x.append(int(input()))
    ans.append(2*x[i])
inlayer = torch.tensor(x,dtype=torch.float32);

l1 = torch.randn(n,requires_grad=True)

l2 = torch.randn(n,requires_grad=True)

y =  l1*inlayer

z = l2*y

z.backward(torch.tensor(ans,dtype=torch.float32))

print(z);