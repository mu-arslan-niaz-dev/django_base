import json

from django_base.validation.exceptions import APIValidationError


def parse_json_body(request):
    """
    Require application/json and return a decoded dict.
    Raises APIValidationError on bad Content-Type or invalid JSON.
    """
    if request.content_type != "application/json":
        raise APIValidationError(
            "Content-Type must be application/json",
            status_code=415,
        )
    try:
        raw = request.body.decode("utf-8")
        data = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise APIValidationError("Invalid JSON body", status_code=400)

    if not isinstance(data, dict):
        raise APIValidationError("JSON body must be an object", status_code=400)

    return data
