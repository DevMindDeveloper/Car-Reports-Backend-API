from dateutil import parser

## date formating
def convert_date_to_desired_format(date):
    try:
        dt = parser.parse(date)
        return dt.strftime("%Y-%m-%d")
    except Exception as e:
        return f"Invlaid date : {e}"
    