from string import Template

airlines_content = {
    1: 'Volaris',
    2: 'Aeromar',
    3: 'Interjet',
    4: 'Aeromexico'
}

airports_content = {
    1: 'Benito Juarez',
    2: 'Guanajuato',
    3: 'La paz',
    4: 'Oaxaca'
}

movements_content = {
    1: 'Salida',
    2: 'Llegada'
}

flights_content = (
    [1, 1, 1, '2021-05-02'],
    [2, 1, 1, '2021-05-02'],
    [3, 2, 2, '2021-05-02'],
    [4, 3, 2, '2021-05-02'],
    [1, 3, 2, '2021-05-02'],
    [2, 1, 1, '2021-05-02'],
    [2, 3, 1, '2021-05-04'],
    [3, 4, 1, '2021-05-04'],
    [3, 4, 1, '2021-05-04'],

)

creation_queries = (
            """
            CREATE TABLE IF NOT EXISTS airlines (
                airline_id INTEGER PRIMARY KEY,
                airline_name VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS airports (
                airport_id INTEGER PRIMARY KEY,
                airport_name VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS movements (
                movement_id INTEGER PRIMARY KEY,
                description VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS flights (
                airline_id INTEGER references airlines (airline_id),
                airport_id INTEGER references airports (airport_id),
                movement_id INTEGER references movements (movement_id),
                flight_day VARCHAR(255) NOT NULL
            )
            """
        )
drop_queries = (
    """DROP TABLE airlines CASCADE """,
    """DROP TABLE airports CASCADE """,
    """DROP TABLE movements CASCADE """,
    """DROP TABLE flights CASCADE """
)

populate_airlines: Template = Template(
    """
    INSERT INTO airlines (airline_id, airline_name)
    VALUES (${id}, '${name}');
    """,
)

populate_airports:Template = Template(
    """
    INSERT INTO airports (airport_id, airport_name)
    VALUES (${id}, '${name}')
    """,
)

populate_movements:Template = Template(
    """
    INSERT INTO movements (movement_id, description)
    VALUES (${id}, '${desc}')
    """
)

populate_flights:Template = Template(
    """
    INSERT INTO flights (airline_id, airport_id, movement_id, flight_day)
    VALUES (${id_airline}, ${id_airport}, ${id_movement}, '${daily}')
    """
)

bigger_mov_airport_query ="""
                    SELECT airport_name, COUNT(movement_id)
                    FROM flights INNER JOIN airports ON flights.airport_id = airports.airport_id GROUP BY airports.airport_id
                    HAVING COUNT (movement_id)=(
                        SELECT MAX(mycount)
                        FROM (
                            SELECT airport_id, COUNT(movement_id) mycount
                            FROM flights
                            GROUP BY airport_id) as x);

                """

more_flights_airline_query="""
                    SELECT airline_name, COUNT(airport_id)
                    FROM flights INNER JOIN airlines ON flights.airport_id = airlines.airline_id GROUP BY airlines.airline_id
                    HAVING COUNT (airport_id)=(
                        SELECT MAX(mycount)
                        FROM (
                            SELECT airport_id, COUNT(airport_id) mycount
                            FROM flights
                            GROUP BY airport_id) as x);"""

more_flights_date_query="""
                    SELECT flight_day, COUNT(movement_id)
                    FROM flights GROUP BY flight_day
                    HAVING COUNT(movement_id)=(
                        SELECT MAX(mycount)
                        FROM (
                            SELECT flight_day, COUNT(movement_id) mycount
                            FROM flights
                            GROUP BY flight_day) as x)"""

more_than_2_flights_airline_query="""
                    SELECT airlines.airline_name, flight_day, COUNT(movement_id)
                    FROM (flights INNER JOIN airlines ON flights.airline_id = airlines.airline_id )
                    GROUP BY airlines.airline_name, flight_day
                    HAVING COUNT(movement_id) > 2;"""
