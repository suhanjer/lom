import sqlite3

YEARS_DICT = {
    '2018': 'ShipmentDate>=strftime("%Y-%m-%d", "2018-01-01") AND ShipmentDate<=strftime("%Y-%m-%d", "2018-12-31")',
    '2019': 'ShipmentDate>=strftime("%Y-%m-%d", "2019-01-01") AND ShipmentDate<=strftime("%Y-%m-%d", "2019-12-31")',
    '2020': 'ShipmentDate>=strftime("%Y-%m-%d", "2020-01-01") AND ShipmentDate<=strftime("%Y-%m-%d", "2020-12-31")',
    '2021': 'ShipmentDate>=strftime("%Y-%m-%d", "2021-01-01") AND ShipmentDate<=strftime("%Y-%m-%d", "2021-12-31")',
}

def connect_to_db(db_file):
    conn = 0
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def get_all_by_year(conn, years):
    cur = conn.cursor()

    cur.execute("SELECT SUM(Mass) FROM entries")
    total = cur.fetchall()[0][0]
    print("==================================================================")
    print(f"Всего: {round(total, 2)}")

    year_values = {}
    for year in years:
        cur.execute(f"SELECT SUM(Mass) FROM entries WHERE {years[year]}")
        data = cur.fetchall()[0][0]
        year_values[year] = data
        print(f"    {year}: {round(data,2)} ({round(data/total*100, 2)}%)")

    return year_values

def get_all_regions(conn):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT Region FROM entries")
    data = cur.fetchall()
    regions = []
    for i in data:
        regions.append(i[0])
    regions.sort()
    print("==================================================================")
    print(regions)

    return regions

def get_all_clients(conn):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT Client FROM entries")
    data = cur.fetchall()
    clients = []
    for i in data:
        clients.append(i[0])
    clients.sort()
    print("==================================================================")
    print(clients)

    return clients

def by_region(conn, regions):
    cur = conn.cursor()

    cur.execute("SELECT SUM(Mass) FROM entries")
    total = cur.fetchall()[0][0]
    print("==================================================================")
    print(f"Всего: {round(total, 2)}")

    values = {}
    for region in regions:
        cur.execute(f"SELECT SUM(Mass) FROM entries WHERE Region = '{region}'")
        data = cur.fetchall()
        values[f'{region}'] = data[0][0]

    values_sorted = dict(sorted(values.items(), key=lambda item: item[1], reverse=True))
    for i in values_sorted:
        print(f"    {i} - {round(values_sorted[i], 2)} ({round(values_sorted[i]/total*100, 1)}%)")

    return values_sorted

def by_client(conn, clients):
    cur = conn.cursor()

    cur.execute("SELECT SUM(Mass) FROM entries")
    total = cur.fetchall()[0][0]
    print("==================================================================")
    print(f"Всего: {round(total, 2)}")

    values = {}
    for client in clients:
        cur.execute(f"SELECT SUM(Mass) FROM entries WHERE Client = '{client}'")
        data = cur.fetchall()
        values[f'{client}'] = data[0][0]

    values_sorted = dict(sorted(values.items(), key=lambda item: item[1], reverse=True))
    for i in values_sorted :
        print(f"    {i} - {round(values_sorted[i], 2)} ({round(values_sorted[i]/total*100, 1)}%)")

    return values_sorted

def by_region_client(conn, region_values, clients):
    cur = conn.cursor()

    region_clients_dict = {}
    for region in region_values:
        clients_dict = {}
        for client in clients:
            cur.execute(f"SELECT SUM(Mass) FROM entries WHERE Region = '{region}' AND Client = '{client}'")
            clients_dict[f'{client}'] = cur.fetchall()[0][0]

        region_clients_dict[f'{region}'] = clients_dict
    
    print("==================================================================")
    for region in region_clients_dict:
        print("\n")
        print(region, round(region_values[region], 2))
        for client in region_clients_dict[region]:
            if region_clients_dict[region][client] is not None:
                print(f"    {client} - {round(region_clients_dict[region][client], 2)} ({round(region_clients_dict[region][client]/region_values[region]*100, 1)}%)")

    return region_clients_dict

def main():

    database = "lom.db"
    conn = connect_to_db(database)

    with conn:
        regions = get_all_regions(conn)
        clients = get_all_clients(conn)

        region_values = by_region(conn, regions)
        by_client(conn, clients)

        by_region_client(conn, region_values, clients)

        get_all_by_year(conn, YEARS_DICT)
    
if __name__ == '__main__':
    main()