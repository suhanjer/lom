str = 'ShipmentDate>=strftime("%Y-%m-%d", "20{year}-01-01") AND ShipmentDate<=strftime("%Y-%m-%d", "20{year}-12-31")'

lst = [(str.format(year=i)) for i in range(18, 22)]

for i in lst:
    print(i)