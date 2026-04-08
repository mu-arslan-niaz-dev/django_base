import json

from django.http import HttpResponse


def json_response(payload, status=200):
    """Single place for JSON HTTP responses (no JsonResponse in controllers)."""
    return HttpResponse(
        json.dumps(payload, ensure_ascii=False, default=str),
        content_type="application/json; charset=utf-8",
        status=status,
    )


def success_response(data, status=200):
    """Standard success envelope."""
    return json_response({"data": data}, status=status)


def error_response(message, status=400, code=None):
    """Standard error envelope."""
    err = {"message": message}
    if code is not None:
        err["code"] = code
    return json_response({"error": err}, status=status)
