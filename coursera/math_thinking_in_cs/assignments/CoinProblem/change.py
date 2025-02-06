def change(amount):
  if amount == 12:
     return [5,7]
  if amount % 7 == 0:
     list = []
     for i in range(int(amount/7)):
         list.append(7)
     return list
  if amount % 5 == 0:
     list = []
     for i in range(int(amount/5)):
         list.append(5)
     return list
  if amount == 17:
     return [5,5,7]
  if amount == 19:
     return [7,7,5]
  if amount == 22:
     return [5,5,5,7]
  if amount == 24:
    return [5, 5, 7, 7]
  coins=change(amount-7)
  coins.append(7)
  return coins

for i in range(24,1000):
    print(i)
    print(change(i))
    print("-----------------")
  
