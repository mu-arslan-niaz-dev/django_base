from django_base.validation.exceptions import APIValidationError


class UserCreateValidator:
    """
    Validates payload for creating a user (DRF-style: single responsibility, reusable).
    """

    def validate(self, data):
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""
        email = (data.get("email") or "").strip()

        if not username or not password:
            raise APIValidationError(
                "username and password are required",
                status_code=400,
            )

        return {
            "username": username,
            "password": password,
            "email": email,
        }


class UserListValidator:
    """
    Validates query params for listing users.

    Supported:
    - page: int (default 1)
    - page_size: int (default 50, max 200)
    """

    def validate(self, query_params):
        page_raw = (query_params.get("page") or "").strip()
        page_size_raw = (query_params.get("page_size") or "").strip()

        page = 1
        page_size = 50

        if page_raw:
            if not page_raw.isdigit():
                raise APIValidationError(
                    "page must be a positive integer", status_code=400
                )
            page = int(page_raw)

        if page_size_raw:
            if not page_size_raw.isdigit():
                raise APIValidationError(
                    "page_size must be a positive integer", status_code=400
                )
            page_size = int(page_size_raw)

        if page < 1:
            raise APIValidationError("page must be >= 1", status_code=400)
        if page_size < 1:
            raise APIValidationError("page_size must be >= 1", status_code=400)
        if page_size > 200:
            raise APIValidationError("page_size must be <= 200", status_code=400)

        return {"page": page, "page_size": page_size}
