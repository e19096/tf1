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
    except:
        print("Cannot connect.")
    return conn

# TODO format data better for fe
def fetch(conn, query, vars, error_msg):
    result = []
    print("Now executing: {}".format(query))
    cursor = conn.cursor()
    try:
        cursor.execute(query, vars)
        raw = cursor.fetchall()
        for line in raw:
            result.append(line)
        return result
    except Exception as e:
        print('fetch error')
        print(e)
        raise Exception(error_msg)

def write(conn, query, vars, success_msg, error_msg):
    print("Now executing: {}".format(query))
    cursor = conn.cursor()
    try:
        # TODO row-level locks
        cursor.execute(query, vars)
        conn.commit()
        return success_msg
    except Exception as e: # TODO exclusion exception?
        print('write error')
        print(e)
        conn.rollback()
        raise Exception(error_msg)

def handler(event, context):
    print(event)
    print(context)

    conn = create_conn()

    try:
        resource = event.get("resource")
        if resource == "/trucks":
            data = handle_trucks(event, conn)
        elif resource == "/reservations":
            data = handle_reservations(event, conn)
        else:
            print(f"ERROR: unimplemented route: {resource}")

        conn.close()

        return {"statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"data": data}, default=str)}
    except Exception as e: # TODO exception classes
        print('handler error')
        print(e)
        return {"statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": str(e)}, default=str)}


def handle_trucks(event, conn):
    params = event.get("queryStringParameters")
    if params is None or not all(key in params for key in ["start_dt", "end_dt"]):
        raise Exception("Missing query parameters")

    return get_available_trucks(conn=conn,
                                start_dt=params.get("start_dt"),
                                end_dt=params.get("end_dt"))

def handle_reservations(event, conn):
    try:
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]
    except KeyError as e:
        print(e)
        raise Exception("authorization error")

    httpMethod = event.get("httpMethod")
    if httpMethod == "GET":
        return get_user_reservations(conn=conn,
                                     user_id=user_id)
    elif httpMethod == "POST":
        params = event.get("queryStringParameters")
        if params is None or not all(key in params for key in ["truck_id", "start_dt", "end_dt"]):
            raise Exception("Missing query parameters")

        return create_reservation(conn=conn,
                                  user_id=user_id,
                                  truck_id=params.get("truck_id"),
                                  start_dt=params.get("start_dt"),
                                  end_dt=params.get("end_dt"))

# TODO upsert with additional identifier.. move_id?
# TODO let client pass truck name instead of truck id
# TODO validate dates
def create_reservation(conn, user_id, truck_id, start_dt, end_dt):
    query = """
    insert into reservations (user_id, truck_id, start_dt, end_dt)
    values (%s, %s, %s, %s)
    """
    success_msg = "success! your truck has been reserved."
    error_msg = "truck unavailable! please select a different truck or daterange and try again"
    return write(conn,
                 query,
                 (user_id, int(truck_id), start_dt, end_dt),
                 success_msg,
                 error_msg)

# TODO add 15? min buffer between reservations
# TODO look up overlapping by truck name
def get_available_trucks(conn, start_dt, end_dt):
    query = """
    with overlapping_reservations as (
      select trucks.id as truck_id
           , reservations.id as reservation_id
      from trucks
      join reservations
        on trucks.id = reservations.truck_id
       and tstzrange(%s, %s, '[]') && tstzrange(reservations.start_dt, reservations.end_dt, '[]')
    )
    select trucks.id, trucks.name from trucks
    left join overlapping_reservations
           on trucks.id = overlapping_reservations.truck_id
    where overlapping_reservations.reservation_id is null
      and %s > now()
    """
    return fetch(conn, query, (start_dt, end_dt, start_dt), "error fetching trucks, please check your dates and try again")

# TODO option/param to fetch past reservations
def get_user_reservations(conn, user_id):
    query = """
    select reservations.start_dt
         , reservations.end_dt
         , trucks.name
         , trucks.id
    from reservations, trucks
    where reservations.truck_id = trucks.id
      and end_dt > now()
      and user_id = %s
    order by start_dt asc
    limit 100
    """
    return fetch(conn, query, (user_id,), "error fetching your reservations")

# TODO exception classes
# TODO rename file; move fns into sep files
# TODO admin user support
