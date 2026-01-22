import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SortOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SORT_ORDER_UNSPECIFIED: _ClassVar[SortOrder]
    SORT_ORDER_ASC: _ClassVar[SortOrder]
    SORT_ORDER_DESC: _ClassVar[SortOrder]

class EntityStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENTITY_STATUS_UNSPECIFIED: _ClassVar[EntityStatus]
    ENTITY_STATUS_ACTIVE: _ClassVar[EntityStatus]
    ENTITY_STATUS_INACTIVE: _ClassVar[EntityStatus]
    ENTITY_STATUS_PENDING: _ClassVar[EntityStatus]
    ENTITY_STATUS_ARCHIVED: _ClassVar[EntityStatus]
    ENTITY_STATUS_SUSPENDED: _ClassVar[EntityStatus]

class HealthStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HEALTH_STATUS_UNSPECIFIED: _ClassVar[HealthStatus]
    HEALTH_STATUS_HEALTHY: _ClassVar[HealthStatus]
    HEALTH_STATUS_DEGRADED: _ClassVar[HealthStatus]
    HEALTH_STATUS_UNHEALTHY: _ClassVar[HealthStatus]
SORT_ORDER_UNSPECIFIED: SortOrder
SORT_ORDER_ASC: SortOrder
SORT_ORDER_DESC: SortOrder
ENTITY_STATUS_UNSPECIFIED: EntityStatus
ENTITY_STATUS_ACTIVE: EntityStatus
ENTITY_STATUS_INACTIVE: EntityStatus
ENTITY_STATUS_PENDING: EntityStatus
ENTITY_STATUS_ARCHIVED: EntityStatus
ENTITY_STATUS_SUSPENDED: EntityStatus
HEALTH_STATUS_UNSPECIFIED: HealthStatus
HEALTH_STATUS_HEALTHY: HealthStatus
HEALTH_STATUS_DEGRADED: HealthStatus
HEALTH_STATUS_UNHEALTHY: HealthStatus

class PaginationRequest(_message.Message):
    __slots__ = ("page_size", "page_token")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: str
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class PaginationResponse(_message.Message):
    __slots__ = ("next_page_token", "total_count", "has_more")
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    total_count: int
    has_more: bool
    def __init__(self, next_page_token: _Optional[str] = ..., total_count: _Optional[int] = ..., has_more: bool = ...) -> None: ...

class Money(_message.Message):
    __slots__ = ("currency_code", "amount", "decimal_places")
    CURRENCY_CODE_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    DECIMAL_PLACES_FIELD_NUMBER: _ClassVar[int]
    currency_code: str
    amount: int
    decimal_places: int
    def __init__(self, currency_code: _Optional[str] = ..., amount: _Optional[int] = ..., decimal_places: _Optional[int] = ...) -> None: ...

class Price(_message.Message):
    __slots__ = ("current", "original", "discount_percent")
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_FIELD_NUMBER: _ClassVar[int]
    DISCOUNT_PERCENT_FIELD_NUMBER: _ClassVar[int]
    current: Money
    original: Money
    discount_percent: int
    def __init__(self, current: _Optional[_Union[Money, _Mapping]] = ..., original: _Optional[_Union[Money, _Mapping]] = ..., discount_percent: _Optional[int] = ...) -> None: ...

class Address(_message.Message):
    __slots__ = ("line1", "line2", "city", "state", "postal_code", "country_code")
    LINE1_FIELD_NUMBER: _ClassVar[int]
    LINE2_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    POSTAL_CODE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    line1: str
    line2: str
    city: str
    state: str
    postal_code: str
    country_code: str
    def __init__(self, line1: _Optional[str] = ..., line2: _Optional[str] = ..., city: _Optional[str] = ..., state: _Optional[str] = ..., postal_code: _Optional[str] = ..., country_code: _Optional[str] = ...) -> None: ...

class GeoLocation(_message.Message):
    __slots__ = ("latitude", "longitude")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    latitude: float
    longitude: float
    def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...

class Date(_message.Message):
    __slots__ = ("year", "month", "day")
    YEAR_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    year: int
    month: int
    day: int
    def __init__(self, year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ...) -> None: ...

class TimeRange(_message.Message):
    __slots__ = ("start_time", "end_time")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(self, start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AuditInfo(_message.Message):
    __slots__ = ("created_at", "updated_at", "created_by", "updated_by", "version")
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    created_by: str
    updated_by: str
    version: int
    def __init__(self, created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_by: _Optional[str] = ..., updated_by: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...

class SortSpec(_message.Message):
    __slots__ = ("field", "order")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    field: str
    order: SortOrder
    def __init__(self, field: _Optional[str] = ..., order: _Optional[_Union[SortOrder, str]] = ...) -> None: ...

class ErrorDetail(_message.Message):
    __slots__ = ("code", "message", "field", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    field: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ..., field: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ValidationError(_message.Message):
    __slots__ = ("errors",)
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    errors: _containers.RepeatedCompositeFieldContainer[FieldError]
    def __init__(self, errors: _Optional[_Iterable[_Union[FieldError, _Mapping]]] = ...) -> None: ...

class FieldError(_message.Message):
    __slots__ = ("field", "message", "rule")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RULE_FIELD_NUMBER: _ClassVar[int]
    field: str
    message: str
    rule: str
    def __init__(self, field: _Optional[str] = ..., message: _Optional[str] = ..., rule: _Optional[str] = ...) -> None: ...

class ResourceId(_message.Message):
    __slots__ = ("type", "id")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    type: str
    id: str
    def __init__(self, type: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class Attribute(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class Image(_message.Message):
    __slots__ = ("url", "alt_text", "width", "height", "format", "size_bytes")
    URL_FIELD_NUMBER: _ClassVar[int]
    ALT_TEXT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    url: str
    alt_text: str
    width: int
    height: int
    format: str
    size_bytes: int
    def __init__(self, url: _Optional[str] = ..., alt_text: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., format: _Optional[str] = ..., size_bytes: _Optional[int] = ...) -> None: ...

class Attachment(_message.Message):
    __slots__ = ("id", "filename", "content_type", "size_bytes", "url", "uploaded_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    UPLOADED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    filename: str
    content_type: str
    size_bytes: int
    url: str
    uploaded_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., filename: _Optional[str] = ..., content_type: _Optional[str] = ..., size_bytes: _Optional[int] = ..., url: _Optional[str] = ..., uploaded_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class PhoneNumber(_message.Message):
    __slots__ = ("country_code", "national_number", "e164")
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    NATIONAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    E164_FIELD_NUMBER: _ClassVar[int]
    country_code: str
    national_number: str
    e164: str
    def __init__(self, country_code: _Optional[str] = ..., national_number: _Optional[str] = ..., e164: _Optional[str] = ...) -> None: ...

class HealthCheckResponse(_message.Message):
    __slots__ = ("status", "components", "version", "checked_at")
    class ComponentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: HealthStatus
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[HealthStatus, str]] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CHECKED_AT_FIELD_NUMBER: _ClassVar[int]
    status: HealthStatus
    components: _containers.ScalarMap[str, HealthStatus]
    version: str
    checked_at: _timestamp_pb2.Timestamp
    def __init__(self, status: _Optional[_Union[HealthStatus, str]] = ..., components: _Optional[_Mapping[str, HealthStatus]] = ..., version: _Optional[str] = ..., checked_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
