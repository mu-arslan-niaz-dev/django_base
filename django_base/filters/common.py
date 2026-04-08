def parse_optional_bool(value):
    if value is None:
        return None
    val = value.strip().lower()
    if val in {"true", "1", "yes"}:
        return True
    if val in {"false", "0", "no"}:
        return False
    return None


def map_ordering(query_params, allowed_fields, default_field="id"):
    sort_by = (query_params.get("sort_by") or default_field).strip().lower()
    order_by = (query_params.get("order_by") or "asc").strip().lower()

    if sort_by not in allowed_fields:
        sort_by = default_field

    prefix = "-" if order_by == "desc" else ""
    return f"{prefix}{sort_by}"
