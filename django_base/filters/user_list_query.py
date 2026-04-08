from django_base.filters.common import map_ordering, parse_optional_bool


def apply_user_list_query_params(queryset, query_params):
    """
    Reusable mapping layer for list-users query params:
    - sort_by: id | username | date_joined
    - order_by: asc | desc
    - is_active: true/false/1/0/yes/no
    - is_staff: true/false/1/0/yes/no
    - search: username icontains
    """
    is_active_value = parse_optional_bool(query_params.get("is_active"))
    is_staff_value = parse_optional_bool(query_params.get("is_staff"))
    search = (query_params.get("search") or "").strip()

    if is_active_value is not None:
        queryset = queryset.filter(is_active=is_active_value)
    if is_staff_value is not None:
        queryset = queryset.filter(is_staff=is_staff_value)
    if search:
        queryset = queryset.filter(username__icontains=search)

    ordering = map_ordering(
        query_params=query_params,
        allowed_fields={"id", "username", "date_joined"},
        default_field="id",
    )
    return queryset.order_by(ordering)
