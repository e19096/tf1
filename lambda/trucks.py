import json
import os
import psycopg2

def create_conn():
    conn = None
    try:
        conn = psycopg2.connect(dbname=os.environ.get("DB_NAME"),
                                user=os.environ.get("DB_USER"),
                                host=os.environ.get("DB_HOST"),
                                port=os.environ.get("DB_PORT"),
                                password=os.environ.get("DB_PASSWORD"))
        # conn = psycopg2.connect(dbname='constituents_development',
        #                         user='postgres',
        #                         host="localhost",
        #                         port=5432,
        #                         password='postgres')
    except:
        print("Cannot connect.")
    return conn

def fetch(conn, query, vars):
    result = []
    print("Now executing: {}".format(query))
    cursor = conn.cursor()
    cursor.execute(query, vars)

    raw = cursor.fetchall()
    for line in raw:
        result.append(line)

    return result

def write(conn, query, vars, error_msg):
    print("Now executing: {}".format(query))
    cursor = conn.cursor()
    try:
        # TODO row-level locks
        cursor.execute(query, vars)
        conn.commit()
    except Exception as e:
        print('write error')
        print(e)
        conn.rollback()
        return error_msg

# TODO handle error case
def handler(event, context):
    print(event)
    print(context)

    conn = create_conn()

    resource = event.get("resource")
    if resource == "/trucks":
        data = handle_trucks(event, conn)
    elif resource == "/reservations":
        data = handle_reservations(event, conn)
    # else error TODO

    conn.close()

    return {"statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"data": data}, default=str)}

def handle_trucks(event, conn):
    params = event.get("queryStringParameters")
    if params is None: # TODO what if empty or missing or bad params
        return {"error": "Bad request"} # TODO use exception for bad req 400

    return get_available_trucks(conn=conn,
                                start_dt=params.get("start_dt"),
                                end_dt=params.get("end_dt"))

def handle_reservations(event, conn):
    httpMethod = event.get("httpMethod")
    params = event.get("queryStringParameters")
    if params is None: # TODO what if empty or missing or bad params
        return {"error": "Bad request"} # TODO use exception; return 400

    if httpMethod == "GET":
        return get_user_reservations(conn=conn,
                                     user_id=params.get("user_id"))
    elif httpMethod == "POST":
        return create_reservation(conn=conn,
                                  user_id=params.get("user_id"),
                                  truck_id=params.get("truck_id"),
                                  start_dt=params.get("start_dt"),
                                  end_dt=params.get("end_dt"))
        pass

# TODO upsert with additional identifier.. move_id?
# TODO let client pass truck name instead of truck id

# TODO validate: res starts in future, end dt > start dt, truck id, user_id; decorator?
# TODO verify logged in user is requesting own or is admin user
def create_reservation(conn, user_id, truck_id, start_dt, end_dt):
    query = """
    insert into reservations (user_id, truck_id, start_dt_utc, end_dt_utc)
    values (%s, %s, %s, %s)
    """
    error_msg = "truck unavailable! please select a different truck or daterange and try again"
    return write(conn, query, (int(user_id), int(truck_id), start_dt, end_dt), error_msg)

# TODO timezones! require utc params?
# TODO add 15? min buffer between reservations
# TODO look up overlapping by truck name instead

# TODO validate params
def get_available_trucks(conn, start_dt, end_dt):
    query = """
    with overlapping_reservations as (
      select trucks.id as truck_id
           , reservations.id as reservation_id
      from trucks
      join reservations
        on trucks.id = reservations.truck_id
       and tsrange(%s, %s) && tsrange(reservations.start_dt_utc, reservations.end_dt_utc)
    )
    select * from trucks
    left join overlapping_reservations
           on trucks.id = overlapping_reservations.truck_id
    where overlapping_reservations.reservation_id is null
    """
    return fetch(conn, query, (start_dt, end_dt))

# TODO option/param to fetch past reservations

# TODO verify logged in user is requesting own or is admin user
def get_user_reservations(conn, user_id):
    query = """
    select * from reservation
    where end_dt_utc > (now() at time zone 'utc')
      and user_id = %s
    order by start_dt_utc asc
    limit 100",
    """
    return fetch(conn, query, (int(user_id),))

# TODO signup/login
# TODO factor fns out into other files eg trucks, reservations
