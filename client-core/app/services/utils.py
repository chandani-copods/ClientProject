from datetime import datetime, timezone
from fastapi import HTTPException
from app.schemas.common import (
    APIError,
)
from starlette.status import HTTP_400_BAD_REQUEST
from sqlmodel import SQLModel, select
from sqlalchemy import func, or_, text
from fastapi import Query
from typing import (
    Optional,
    List,
    Type,
    Any,
    Dict,
    Union,
    get_args,
    get_origin,
    Annotated,
    Tuple,
)
from enum import Enum
import inspect
from pydantic import ValidationError


def raise_api_error(
    code: str | None = "ERROR",
    message: str | None = "Something went wrong",
    status_code: int = HTTP_400_BAD_REQUEST,
    details: dict | None = None,
):
    error = APIError(code=code, message=message, details=details)
    raise HTTPException(status_code=status_code, detail=error.model_dump())


common_error_responses = {
    422: {"description": "Validation error", "model": APIError},
    404: {"description": "Not found", "model": APIError},
    500: {"description": "Internal server error", "model": APIError},
}


# def build_filtered_query(model, filters: FilterModelWithFields):
#     """
#     Build a filtered query for a given model and filter model.
#     """
#     query = select(model)

#     if filters.search and filters.searchable_fields:
#         search_clauses = [
#             getattr(model, field).ilike(f"%{filters.search}%")
#             for field in filters.searchable_fields
#         ]
#         query = query.where(or_(*search_clauses))

#     for field in filters.filterable_fields:
#         value = getattr(filters, field, None)
#         if value is not None:
#             column = getattr(model, field)

#             # Check if value is an iterable
#             if hasattr(value, "__iter__") and not isinstance(value, (str, bytes)):
#                 query = query.where(column.in_(value))
#             else:
#                 query = query.where(column == value)

#     # Handle date range filters - simple datetime comparison
#     for field, date_range in filters.date_range_filter_fields.items():
#         column = getattr(model, field)

#         if date_range.from_date is not None:
#             query = query.where(column >= date_range.from_date)
#         if date_range.to_date is not None:
#             query = query.where(column <= date_range.to_date)

#     if filters.sort_by and filters.sort_by in filters.valid_sort_fields:
#         column = getattr(model, filters.sort_by)
#         order = (
#             column.desc()
#             if filters.sort_direction == SortDirection.DESC
#             else column.asc()
#         )
#         query = query.order_by(order)

#     return query


# def build_paginated_and_filtered_query(
#     model,
#     filters: FilterModelWithFields,
#     custom_where: Optional[List[Any]] = None,
#     join_options: Optional[List[Any]] = None,
# ) -> Tuple[Any, Any]:
#     """
#     Build a paginated query for a given model and filter model. Return filtered and paginated query.
#     """
#     base_query = build_filtered_query(model, filters)

#     if custom_where:
#         base_query = base_query.where(*custom_where)

#     if join_options:
#         base_query = base_query.options(*join_options)

#     paginated_query = base_query.offset(filters.skip).limit(filters.limit)

#     # Use a subquery to count only the filtered rows
#     total_count_query = select(func.count()).select_from(base_query.subquery())
#     return paginated_query, total_count_query


# def get_filter_metadata(
#     session, model: Type[SQLModel], filter_model_class: Type[FilterModelWithFields]
# ) -> List[FilterOption]:
#     meta = {}
#     sql_fields = []

#     # Instantiate to access property
#     filter_model = filter_model_class()

#     # Handle regular filter fields
#     for field in filter_model.filterable_fields:
#         source = filter_model_class.filter_sources.get(field, "sql")

#         if isinstance(source, list):
#             meta[field] = source
#         elif isinstance(source, type) and issubclass(source, Enum):
#             meta[field] = [e.value for e in source]
#         elif source == "sql":
#             sql_fields.append(field)

#     if sql_fields:
#         table_name = model.__tablename__
#         schema_name = model.__table__.schema or "public"
#         full_table_name = f"{schema_name}.{table_name}"
#         sql_parts = [
#             f"'{field}', (SELECT ARRAY(SELECT DISTINCT {field} FROM {full_table_name} WHERE {field} IS NOT NULL))"
#             for field in sql_fields
#         ]
#         sql = f"SELECT json_build_object({', '.join(sql_parts)});"
#         try:
#             result = session.exec(text(sql)).scalar_one()
#             if result:
#                 meta.update(result)
#         except Exception as e:
#             print(f"Error getting filter metadata: {str(e)}")
#             for field in sql_fields:
#                 meta[field] = []

#     # Create regular filter options with appropriate filter types
#     filter_options = []
#     for k, v in meta.items():
#         # Determine filter type based on field configuration
#         field_type = filter_model_class.model_fields.get(k)
#         filter_type = FilterType.SINGLE_SELECT  # Default

#         if field_type and field_type.annotation:
#             # Check if it's a List type (multi-select)
#             origin = get_origin(field_type.annotation)
#             args = get_args(field_type.annotation)

#             # Handle Optional[List[...]] or List[...]
#             if origin is list or (
#                 origin is Union and any(get_origin(arg) is list for arg in args)
#             ):
#                 filter_type = FilterType.MULTI_SELECT

#         filter_options.append(
#             FilterOption(
#                 key=k,
#                 label=k.replace("_", " ").title(),
#                 options=v,
#                 filter_type=filter_type,
#             )
#         )

#     # Add date range filter options automatically
#     date_range_fields = getattr(filter_model_class, "date_range_fields", [])
#     for field in date_range_fields:
#         filter_options.append(
#             FilterOption(
#                 key=field,
#                 label=field.replace("_", " ").title(),
#                 options=[],  # Empty for date ranges
#                 filter_type=FilterType.DATE_RANGE,
#             )
#         )

#     return filter_options


# def extract_query_params_from_filter_model(
#     model_class: Type[FilterModelWithFields],
# ) -> Dict[str, Any]:
#     """
#     Extract query parameters from a filter model to Annotated[T, Query()] in query params.
#     """
#     query_params = {}

#     for field_name, field_info in model_class.model_fields.items():
#         outer_type_ = field_info.annotation
#         origin = get_origin(outer_type_)
#         args = get_args(outer_type_)

#         if origin is list or (
#             origin is Union and any(get_origin(arg) is list for arg in args)
#         ):
#             # Handle Optional[List[Enum]] or List[str]
#             inner = (
#                 get_args(outer_type_)[0]
#                 if origin is list
#                 else next(
#                     (get_args(arg)[0] for arg in args if get_origin(arg) is list), str
#                 )
#             )
#             query_params[field_name] = Annotated[Optional[List[inner]], Query()]
#         elif origin is Union and type(None) in args:
#             base_type = next(arg for arg in args if arg is not type(None))
#             query_params[field_name] = Annotated[Optional[base_type], Query()]
#         else:
#             query_params[field_name] = Annotated[outer_type_, Query()]

#     return query_params


# def create_filter_deps(model_class: Type[FilterModelWithFields]):
#     query_param_defs = extract_query_params_from_filter_model(model_class)
#     model_fields = model_class.model_fields

#     def _filter_dep(**query_params):
#         return model_class(**{k: v for k, v in query_params.items() if v is not None})

#     parameters = []
#     for key, value in query_param_defs.items():
#         default_val = model_fields[key].default if key in model_fields else None

#         parameters.append(
#             inspect.Parameter(
#                 name=key,
#                 kind=inspect.Parameter.KEYWORD_ONLY,
#                 default=default_val if default_val is not None else None,
#                 annotation=value,
#             )
#         )

#     _filter_dep.__signature__ = inspect.Signature(parameters=parameters)
#     return _filter_dep


def utc_now():
    return datetime.now(tz=timezone.utc)


def beautify_validation_error(error: ValidationError) -> List[Dict[str, str]]:
    return [
        {"field": ".".join(map(str, error["loc"])), "message": error["msg"]}
        for error in error.errors()
    ]
