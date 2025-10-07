from flask import request,jsonify
from functools import wraps

def validate_request(supported_types, *field_names):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = None
            data = (
                request.form.to_dict()
                if request.form
                else (request.args.to_dict() or request.json  )
            )

            # Field requirement check
            missing_fields = set(field_names) - set(data)
            if missing_fields:
                return (
                    jsonify(
                        {
                            "error": f"Missing required fields: {', '.join(missing_fields)}"
                        }
                    ),
                    400,
                )

            # Empty field check
            if request.is_json and not empty_field_check(
                request.get_json(), list(field_names)
            ):
                return jsonify(message="Fields cannot be empty"), 400

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def empty_field_check(dictionary, keys):
    try:
        for key in keys:
            if key in dictionary and not dictionary.get(key):
                return False
        return True
    except Exception as exc:
        logging.error(f"error occured in fucntion empty_field_check:{exc}")
        return False