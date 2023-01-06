import psycopg2

from queries import creation_queries, airlines_content, populate_airlines, airports_content, populate_airports, \
    movements_content, populate_movements, flights_content, populate_flights, drop_queries, \
    bigger_mov_airport_query, more_flights_airline_query, more_flights_date_query, more_than_2_flights_airline_query


class TableManager:

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="xaldigital_local",
            user="debug",
            password="debug",
            port=9090)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        print("""
    ------------------------RETO 02------------------------------
        """)

    def main(self) -> None:

        self.create_tables()
        try:
            self.populate_tables()
        except Exception:
            self.drop_tables()
            self.create_tables()
            self.populate_tables()

        self.bigger_mov_airport()
        self.more_flights_airline()
        self.more_flights_date()
        self.more_than_2_flights_airlines()

    def create_tables(self) -> None:
        for query in creation_queries:
            self.cursor.execute(query)

    def drop_tables(self) -> None:
        for query in drop_queries:
            self.cursor.execute(query)

    def populate_tables(self) -> None:

        for key, value in airlines_content.items():
            query = populate_airlines.substitute({
                'id': key,
                'name': value
            })
            self.cursor.execute(query)

        for key, value in airports_content.items():
            query = populate_airports.substitute({
                'id': key,
                'name': value
            })
            self.cursor.execute(query)

        for key, value in movements_content.items():
            query = populate_movements.substitute({
                'id': key,
                'desc': value
            })
            self.cursor.execute(query)

        for row in flights_content:
            query = populate_flights.substitute({
                'id_airline': row[0],
                'id_airport': row[1],
                'id_movement': row[2],
                'daily': row[3]
            })
            self.cursor.execute(query)

    def bigger_mov_airport(self):
        self.cursor.execute(bigger_mov_airport_query)
        print('''
            AEROPUERTO(s) CON MAYOR MOVIMIENTO EN EL AÑO
        ''')
        for row in self.cursor:
            print(f'Nombre:{row[0]}\n'
                  f'Movimientos:{row[1]}\n')

    def more_flights_airline(self):
        self.cursor.execute(more_flights_airline_query)
        print('''
                AEROLINEA(s) CON MAS VUELOS EN EL AÑO
                ''')
        for row in self.cursor:
            print(f'Nombre:{row[0]}\n'
                  f'Vuelos:{row[1]}\n')

    def more_flights_date(self):
        self.cursor.execute(more_flights_date_query)
        print('''
                DIA CON MAYOR NUMERO DE VUELOS
                ''')
        for row in self.cursor:
            print(f'Dia:{row[0]}\n'
                  f'Vuelos:{row[1]}\n')

    def more_than_2_flights_airlines(self):
        self.cursor.execute(more_than_2_flights_airline_query)
        print('''
                AEROLINEAS(s) CON MAS DE 2 VUELOS AL AÑO
                ''')
        if len(self.cursor.fetchall()):
            for row in self.cursor:
                print(f'Nombre:{row[0]}\n'
                      f'Vuelos:{row[1]}\n')
        else:
            print("NO hay aerolineas")


creator = TableManager()
creator.main()