import pandas as pd
import os
import sqlite3

if os.path.exists('lom.db'):
    os.remove('lom.db')
else:
    print('db file does not exist')

con = sqlite3.connect('lom.db')
cur = con.cursor()
cur.execute(
    """
    CREATE TABLE entries (
        Region TEXT,
        Client TEXT,
        Mass REAL,
        Price REAL,
        Total REAL,
        ShipmentDate TEXT,
        Payment REAL,
        PaymentDate TEXT
    );
    """
)
print('table created')

fname = "lom.csv"

data = pd.read_csv(fname, delimiter = ";")
print(data)
df = pd.DataFrame(data, columns = ['Регион', 'Клиент', 'Вес', 'Цена', 'Сумма', 'Дата поставки', 'Оплачено', 'Дата оплаты'])
df_db = [(i['Регион'], i['Клиент'], i['Вес'], i['Цена'], i['Сумма'], i['Дата поставки'], i['Оплачено'], i['Дата оплаты']) for index, i in df.iterrows()]
#print(df_db)

cur.executemany(f"INSERT INTO entries (Region, Client, Mass, Price, Total, ShipmentDate, Payment, PaymentDate) values (?, ?, ?, ?, ?, ?, ?, ?)", df_db)
con.commit()
con.close()
print("closed")