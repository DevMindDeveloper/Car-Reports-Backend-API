from flask import Flask, request, jsonify
import mysql.connector as mc
from dateutil import parser

from app import config as c

app = Flask(__name__)

## db creds
db_configs = {
    'host' : c.host,
    'user' : c.user,
    'password' : c.password,
    'database' : c.database
}


def convert_date_to_desired_format(date):
    try:
        dt = parser.parse(date)
        return dt.strftime("%Y-%m-%d")
    except Exception as e:
        return f"Invlaid date : {e}"

@app.route("/search_cars", methods=["POST"])
def search_cars():
    ## initialization
    car_dict = {
        "make": [],
        "model": [],
        "year": []
    }

    data = request.get_json()
    date = convert_date_to_desired_format(data['date'])
    make = data['make']
    model = data['model']
    year = data['year']

    ## db initialization
    conn = mc.connect(**db_configs)
    cursor = conn.cursor()

    ## check both fields are avaliable
    if not date or not make or not model or not year:
        return jsonify({"error":"all fields are not given"}), 400 # bad request

    try:

        search_sql_query = "select make, model, year from cars_report where date = %s and make = %s and model = %s and year = %s;"
        cursor.execute(search_sql_query, (date, make, model, year))
        results = cursor.fetchall()
        print(results)

        for res in results:
            car_dict['make'].append(res[0])
            car_dict['model'].append(res[1])
            car_dict['year'].append(res[2])

        return jsonify({"success":car_dict}), 200 # success
    
    except mc.Error as er:
        return jsonify({"error": f"Error {er}"}), 400  # bad request

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=2255)