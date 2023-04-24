import sqlite3

#dictionary with strings for SQL queries for each year, edit to add another year
YEARS_DICT = {
    '2018': 'ShipmentDate>=strftime("%Y-%m-%d", "2018-01-01") AND ShipmentDate<=strftime("%Y-%m-%d", "2018-12-31")',
    '2019': 'ShipmentDate>=strftime("%Y-%m-%d", "2019-01-01") AND ShipmentDate<=strftime("%Y-%m-%d", "2019-12-31")',
    '2020': 'ShipmentDate>=strftime("%Y-%m-%d", "2020-01-01") AND ShipmentDate<=strftime("%Y-%m-%d", "2020-12-31")',
    '2021': 'ShipmentDate>=strftime("%Y-%m-%d", "2021-01-01") AND ShipmentDate<=strftime("%Y-%m-%d", "2021-12-31")',
}

#function to connect to db
def connect_to_db(db_file):
    conn = 0
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

#gets all values from Mass column by year, prints them out, and returns in dictionary form where keys are years
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

#returns list of regions
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

#returns list of clients
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

#prints out sum of of Mass column for each region and returns sorted dictionary where keys are regions
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
        if data == None:
            print(f"    0")
        else:
            print(f"    {region} {round(values[region], 2)}")

    values_sorted = dict(sorted(values.items(), key=lambda item: item[1], reverse=True))
    #for i in values_sorted:
        #print(f"    {i} - {round(values_sorted[i], 2)} ({round(values_sorted[i]/total*100, 1)}%)")

    print("\n")
    return values_sorted

#prints out sum of Mass column of regions by year and returns dictionary where in form "year": {"region": value}
def by_year_region(conn, regions, years, year_values_total):
    cur = conn.cursor()
    
    year_values = {}
    for year in years:
        region_values = {}
        for region in regions:
            cur.execute(f"SELECT SUM(Mass) FROM entries WHERE Region = '{region}' AND {years[year]}")
            data = cur.fetchall()[0][0]
            region_values[region] = data

        year_values[year] = region_values
    
    for year in year_values:
        print(f"{year}: {round(year_values_total[year], 2)}")

        for region in year_values[year]:
            if year_values[year][region] == None:
                print(f"    {region} 0")
            else:
                print(f"    {region} {round(year_values[year][region], 2)} ({round(year_values[year][region]/year_values_total[year]*100, 1)}%)")
            
        print("\n")
        
#prints out sum by clients and returns them in '"client": value' form
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
        print(f"    {client} {round(values[client], 2)} ({round(values[client]/total*100, 1)}%)")

    values_sorted = dict(sorted(values.items(), key=lambda item: item[1], reverse=True))
    #for i in values_sorted :
        #print(f"{i} {round(values_sorted[i], 2)} ({round(values_sorted[i]/total*100, 1)}%)")

    print("\n")

    return values_sorted

#prints sum of mass column of every client by year
def by_year_client(conn, clients, years, year_values_total):
    cur = conn.cursor()

    year_values = {}
    for year in years:
        client_values = {}
        for client in clients:
            cur.execute(f"SELECT SUM(Mass) FROM entries WHERE Client = '{client}' AND {years[year]}")
            data = cur.fetchall()[0][0]
            client_values[client] = data 

        year_values[year] = client_values

    for year in years:
        print(f"{year}: {round(year_values_total[year], 2)}")

        for client in year_values[year]:
            if year_values[year][client] == None:
                print(f"    {client} 0")
            else:
                print(f"    {client} {round(year_values[year][client], 2)} ({round(year_values[year][client]/year_values_total[year]*100, 1)}%)")
        
        print("\n")

#year-month Mass column total
def year_month(conn):
    #period = 'ShipmentDate>=strftime("%Y-%m-%d", "20{year}-{month}-01") AND ShipmentDate<=strftime("%Y-%m-%d", "20{year}-{nextmonth}-31")'
    cur = conn.cursor()

    year_values = {}
    for i in range(18, 22):
        month_values = {}
        for j in range(1, 13):
            cur.execute('SELECT SUM(Mass) FROM entries WHERE ShipmentDate>=strftime("%Y-%m-%d", "20{year}-{month}-01") AND ShipmentDate<=strftime("%Y-%m-%d", "20{year}-{month}-31")'.format(year=i, month=str(j).zfill(2)))
            data = cur.fetchall()[0][0]
            month_values[j] = data
        year_values[i] = month_values

    for year in year_values:
        print(f"{year}", end="")
        for month in year_values[year]:
            if year_values[year][month] == None:
                pass
            else:
                print(f" {str(round(year_values[year][month], 2)).zfill(7)}", end="")

        print("\n")

#prints sum of Mass column of each client in region and returns them in '"region": {"client": value}' form
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
                print(f"    {client} {round(region_clients_dict[region][client], 2)} ({round(region_clients_dict[region][client]/region_values[region]*100, 1)}%)")

    return region_clients_dict

#main function
def main():

    database = "lom.db"
    conn = connect_to_db(database)

    with conn:
        regions = get_all_regions(conn)
        clients = get_all_clients(conn)

        year_values_total = get_all_by_year(conn, YEARS_DICT)

        region_values_total = by_region(conn, regions)
        by_year_region(conn, regions, YEARS_DICT, year_values_total)

        by_client(conn, clients)
        by_year_client(conn, clients, YEARS_DICT, year_values_total)

        year_month(conn)

        by_region_client(conn, region_values_total, clients)
    
if __name__ == '__main__':
    main()