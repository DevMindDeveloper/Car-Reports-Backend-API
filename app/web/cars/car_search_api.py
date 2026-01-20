from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError


from app.web import *

@app.route("/search_cars", methods=["POST"])
@token_required
def search_cars(id):
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

    ## check that all fields are avaliable using schema validation
    car = schema.load({
        'date': date,
        'make' : make,
        'model' : model,
        'year' : year,
    })

    car_record = schema.dump(car)

    try:

        results = session.query(Car.make, Car.model, Car.year).filter(Car.date == car_record['date'], Car.make == car_record['make'],
                                                                      Car.model == car_record['model'], Car.year == car_record['year']).all()

        for res in results:
            car_dict['make'].append(res.make)
            car_dict['model'].append(res.model)
            car_dict['year'].append(res.year)

        return jsonify({"success":car_dict}), 200 # success
    
    except SQLAlchemyError as er:
        session.rollback()
        return jsonify({"error": f"Error {er}"}), 400  # bad request
    
    finally:
        session.close()
