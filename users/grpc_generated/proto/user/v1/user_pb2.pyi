import datetime

from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from proto.common.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER_STATUS_UNSPECIFIED: _ClassVar[UserStatus]
    USER_STATUS_ACTIVE: _ClassVar[UserStatus]
    USER_STATUS_PENDING_VERIFICATION: _ClassVar[UserStatus]
    USER_STATUS_DEACTIVATED: _ClassVar[UserStatus]
    USER_STATUS_SUSPENDED: _ClassVar[UserStatus]
    USER_STATUS_BANNED: _ClassVar[UserStatus]

class UserRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER_ROLE_UNSPECIFIED: _ClassVar[UserRole]
    USER_ROLE_CUSTOMER: _ClassVar[UserRole]
    USER_ROLE_SELLER: _ClassVar[UserRole]
    USER_ROLE_ADMIN: _ClassVar[UserRole]
    USER_ROLE_SUPPORT: _ClassVar[UserRole]

class AddressType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ADDRESS_TYPE_UNSPECIFIED: _ClassVar[AddressType]
    ADDRESS_TYPE_SHIPPING: _ClassVar[AddressType]
    ADDRESS_TYPE_BILLING: _ClassVar[AddressType]
    ADDRESS_TYPE_BOTH: _ClassVar[AddressType]
USER_STATUS_UNSPECIFIED: UserStatus
USER_STATUS_ACTIVE: UserStatus
USER_STATUS_PENDING_VERIFICATION: UserStatus
USER_STATUS_DEACTIVATED: UserStatus
USER_STATUS_SUSPENDED: UserStatus
USER_STATUS_BANNED: UserStatus
USER_ROLE_UNSPECIFIED: UserRole
USER_ROLE_CUSTOMER: UserRole
USER_ROLE_SELLER: UserRole
USER_ROLE_ADMIN: UserRole
USER_ROLE_SUPPORT: UserRole
ADDRESS_TYPE_UNSPECIFIED: AddressType
ADDRESS_TYPE_SHIPPING: AddressType
ADDRESS_TYPE_BILLING: AddressType
ADDRESS_TYPE_BOTH: AddressType

class User(_message.Message):
    __slots__ = ("id", "email", "display_name", "first_name", "last_name", "phone", "avatar_url", "status", "roles", "email_verified", "phone_verified", "profile", "audit", "last_login_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    EMAIL_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    PHONE_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    AUDIT_FIELD_NUMBER: _ClassVar[int]
    LAST_LOGIN_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    display_name: str
    first_name: str
    last_name: str
    phone: _common_pb2.PhoneNumber
    avatar_url: str
    status: UserStatus
    roles: _containers.RepeatedScalarFieldContainer[UserRole]
    email_verified: bool
    phone_verified: bool
    profile: UserProfile
    audit: _common_pb2.AuditInfo
    last_login_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., display_name: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., phone: _Optional[_Union[_common_pb2.PhoneNumber, _Mapping]] = ..., avatar_url: _Optional[str] = ..., status: _Optional[_Union[UserStatus, str]] = ..., roles: _Optional[_Iterable[_Union[UserRole, str]]] = ..., email_verified: bool = ..., phone_verified: bool = ..., profile: _Optional[_Union[UserProfile, _Mapping]] = ..., audit: _Optional[_Union[_common_pb2.AuditInfo, _Mapping]] = ..., last_login_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UserProfile(_message.Message):
    __slots__ = ("bio", "date_of_birth", "gender", "language", "currency", "timezone", "company", "website", "social_links")
    class SocialLinksEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BIO_FIELD_NUMBER: _ClassVar[int]
    DATE_OF_BIRTH_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    COMPANY_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_FIELD_NUMBER: _ClassVar[int]
    SOCIAL_LINKS_FIELD_NUMBER: _ClassVar[int]
    bio: str
    date_of_birth: _common_pb2.Date
    gender: str
    language: str
    currency: str
    timezone: str
    company: str
    website: str
    social_links: _containers.ScalarMap[str, str]
    def __init__(self, bio: _Optional[str] = ..., date_of_birth: _Optional[_Union[_common_pb2.Date, _Mapping]] = ..., gender: _Optional[str] = ..., language: _Optional[str] = ..., currency: _Optional[str] = ..., timezone: _Optional[str] = ..., company: _Optional[str] = ..., website: _Optional[str] = ..., social_links: _Optional[_Mapping[str, str]] = ...) -> None: ...

class UserAddress(_message.Message):
    __slots__ = ("id", "user_id", "label", "full_name", "phone", "address", "type", "is_default_shipping", "is_default_billing", "delivery_instructions", "audit")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_SHIPPING_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_BILLING_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_INSTRUCTIONS_FIELD_NUMBER: _ClassVar[int]
    AUDIT_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    label: str
    full_name: str
    phone: _common_pb2.PhoneNumber
    address: _common_pb2.Address
    type: AddressType
    is_default_shipping: bool
    is_default_billing: bool
    delivery_instructions: str
    audit: _common_pb2.AuditInfo
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., label: _Optional[str] = ..., full_name: _Optional[str] = ..., phone: _Optional[_Union[_common_pb2.PhoneNumber, _Mapping]] = ..., address: _Optional[_Union[_common_pb2.Address, _Mapping]] = ..., type: _Optional[_Union[AddressType, str]] = ..., is_default_shipping: bool = ..., is_default_billing: bool = ..., delivery_instructions: _Optional[str] = ..., audit: _Optional[_Union[_common_pb2.AuditInfo, _Mapping]] = ...) -> None: ...

class UserPreferences(_message.Message):
    __slots__ = ("email", "push", "sms", "privacy")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PUSH_FIELD_NUMBER: _ClassVar[int]
    SMS_FIELD_NUMBER: _ClassVar[int]
    PRIVACY_FIELD_NUMBER: _ClassVar[int]
    email: EmailPreferences
    push: PushPreferences
    sms: SmsPreferences
    privacy: PrivacyPreferences
    def __init__(self, email: _Optional[_Union[EmailPreferences, _Mapping]] = ..., push: _Optional[_Union[PushPreferences, _Mapping]] = ..., sms: _Optional[_Union[SmsPreferences, _Mapping]] = ..., privacy: _Optional[_Union[PrivacyPreferences, _Mapping]] = ...) -> None: ...

class EmailPreferences(_message.Message):
    __slots__ = ("order_updates", "promotions", "newsletter", "seller_updates", "security_alerts")
    ORDER_UPDATES_FIELD_NUMBER: _ClassVar[int]
    PROMOTIONS_FIELD_NUMBER: _ClassVar[int]
    NEWSLETTER_FIELD_NUMBER: _ClassVar[int]
    SELLER_UPDATES_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ALERTS_FIELD_NUMBER: _ClassVar[int]
    order_updates: bool
    promotions: bool
    newsletter: bool
    seller_updates: bool
    security_alerts: bool
    def __init__(self, order_updates: bool = ..., promotions: bool = ..., newsletter: bool = ..., seller_updates: bool = ..., security_alerts: bool = ...) -> None: ...

class PushPreferences(_message.Message):
    __slots__ = ("enabled", "order_updates", "price_alerts", "messages")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ORDER_UPDATES_FIELD_NUMBER: _ClassVar[int]
    PRICE_ALERTS_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    order_updates: bool
    price_alerts: bool
    messages: bool
    def __init__(self, enabled: bool = ..., order_updates: bool = ..., price_alerts: bool = ..., messages: bool = ...) -> None: ...

class SmsPreferences(_message.Message):
    __slots__ = ("enabled", "delivery_updates", "two_factor_auth")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_UPDATES_FIELD_NUMBER: _ClassVar[int]
    TWO_FACTOR_AUTH_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    delivery_updates: bool
    two_factor_auth: bool
    def __init__(self, enabled: bool = ..., delivery_updates: bool = ..., two_factor_auth: bool = ...) -> None: ...

class PrivacyPreferences(_message.Message):
    __slots__ = ("public_profile", "show_online_status", "searchable", "share_activity")
    PUBLIC_PROFILE_FIELD_NUMBER: _ClassVar[int]
    SHOW_ONLINE_STATUS_FIELD_NUMBER: _ClassVar[int]
    SEARCHABLE_FIELD_NUMBER: _ClassVar[int]
    SHARE_ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    public_profile: bool
    show_online_status: bool
    searchable: bool
    share_activity: bool
    def __init__(self, public_profile: bool = ..., show_online_status: bool = ..., searchable: bool = ..., share_activity: bool = ...) -> None: ...

class CreateUserRequest(_message.Message):
    __slots__ = ("email", "password", "first_name", "last_name", "display_name", "phone", "roles")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    first_name: str
    last_name: str
    display_name: str
    phone: _common_pb2.PhoneNumber
    roles: _containers.RepeatedScalarFieldContainer[UserRole]
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., display_name: _Optional[str] = ..., phone: _Optional[_Union[_common_pb2.PhoneNumber, _Mapping]] = ..., roles: _Optional[_Iterable[_Union[UserRole, str]]] = ...) -> None: ...

class CreateUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class GetUserByEmailRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class GetUserByEmailResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class UpdateUserRequest(_message.Message):
    __slots__ = ("user_id", "user", "update_mask")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    user: User
    update_mask: _field_mask_pb2.FieldMask
    def __init__(self, user_id: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class UpdateUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class DeleteUserRequest(_message.Message):
    __slots__ = ("user_id", "reason")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    reason: str
    def __init__(self, user_id: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class DeactivateUserRequest(_message.Message):
    __slots__ = ("user_id", "reason")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    reason: str
    def __init__(self, user_id: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class DeactivateUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class ReactivateUserRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class ReactivateUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class ListUsersRequest(_message.Message):
    __slots__ = ("pagination", "statuses", "roles", "sort")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    pagination: _common_pb2.PaginationRequest
    statuses: _containers.RepeatedScalarFieldContainer[UserStatus]
    roles: _containers.RepeatedScalarFieldContainer[UserRole]
    sort: _common_pb2.SortSpec
    def __init__(self, pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ..., statuses: _Optional[_Iterable[_Union[UserStatus, str]]] = ..., roles: _Optional[_Iterable[_Union[UserRole, str]]] = ..., sort: _Optional[_Union[_common_pb2.SortSpec, _Mapping]] = ...) -> None: ...

class ListUsersResponse(_message.Message):
    __slots__ = ("users", "pagination")
    USERS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[User]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, users: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...

class SearchUsersRequest(_message.Message):
    __slots__ = ("query", "pagination", "statuses", "roles", "created_at")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    query: str
    pagination: _common_pb2.PaginationRequest
    statuses: _containers.RepeatedScalarFieldContainer[UserStatus]
    roles: _containers.RepeatedScalarFieldContainer[UserRole]
    created_at: _common_pb2.TimeRange
    def __init__(self, query: _Optional[str] = ..., pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ..., statuses: _Optional[_Iterable[_Union[UserStatus, str]]] = ..., roles: _Optional[_Iterable[_Union[UserRole, str]]] = ..., created_at: _Optional[_Union[_common_pb2.TimeRange, _Mapping]] = ...) -> None: ...

class SearchUsersResponse(_message.Message):
    __slots__ = ("users", "pagination")
    USERS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[User]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, users: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...

class UpdateUserProfileRequest(_message.Message):
    __slots__ = ("user_id", "profile", "update_mask")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    profile: UserProfile
    update_mask: _field_mask_pb2.FieldMask
    def __init__(self, user_id: _Optional[str] = ..., profile: _Optional[_Union[UserProfile, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class UpdateUserProfileResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class AddUserAddressRequest(_message.Message):
    __slots__ = ("user_id", "address")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    address: UserAddress
    def __init__(self, user_id: _Optional[str] = ..., address: _Optional[_Union[UserAddress, _Mapping]] = ...) -> None: ...

class AddUserAddressResponse(_message.Message):
    __slots__ = ("address",)
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: UserAddress
    def __init__(self, address: _Optional[_Union[UserAddress, _Mapping]] = ...) -> None: ...

class UpdateUserAddressRequest(_message.Message):
    __slots__ = ("user_id", "address_id", "address", "update_mask")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_ID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    address_id: str
    address: UserAddress
    update_mask: _field_mask_pb2.FieldMask
    def __init__(self, user_id: _Optional[str] = ..., address_id: _Optional[str] = ..., address: _Optional[_Union[UserAddress, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class UpdateUserAddressResponse(_message.Message):
    __slots__ = ("address",)
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: UserAddress
    def __init__(self, address: _Optional[_Union[UserAddress, _Mapping]] = ...) -> None: ...

class DeleteUserAddressRequest(_message.Message):
    __slots__ = ("user_id", "address_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    address_id: str
    def __init__(self, user_id: _Optional[str] = ..., address_id: _Optional[str] = ...) -> None: ...

class ListUserAddressesRequest(_message.Message):
    __slots__ = ("user_id", "type")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    type: AddressType
    def __init__(self, user_id: _Optional[str] = ..., type: _Optional[_Union[AddressType, str]] = ...) -> None: ...

class ListUserAddressesResponse(_message.Message):
    __slots__ = ("addresses",)
    ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    addresses: _containers.RepeatedCompositeFieldContainer[UserAddress]
    def __init__(self, addresses: _Optional[_Iterable[_Union[UserAddress, _Mapping]]] = ...) -> None: ...

class SetDefaultAddressRequest(_message.Message):
    __slots__ = ("user_id", "address_id", "type")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    address_id: str
    type: AddressType
    def __init__(self, user_id: _Optional[str] = ..., address_id: _Optional[str] = ..., type: _Optional[_Union[AddressType, str]] = ...) -> None: ...

class SetDefaultAddressResponse(_message.Message):
    __slots__ = ("address",)
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: UserAddress
    def __init__(self, address: _Optional[_Union[UserAddress, _Mapping]] = ...) -> None: ...

class VerifyEmailRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class VerifyEmailResponse(_message.Message):
    __slots__ = ("sent", "message")
    SENT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    sent: bool
    message: str
    def __init__(self, sent: bool = ..., message: _Optional[str] = ...) -> None: ...

class ConfirmEmailVerificationRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class ConfirmEmailVerificationResponse(_message.Message):
    __slots__ = ("verified", "user_id")
    VERIFIED_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    verified: bool
    user_id: str
    def __init__(self, verified: bool = ..., user_id: _Optional[str] = ...) -> None: ...

class ChangePasswordRequest(_message.Message):
    __slots__ = ("user_id", "current_password", "new_password")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    NEW_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    current_password: str
    new_password: str
    def __init__(self, user_id: _Optional[str] = ..., current_password: _Optional[str] = ..., new_password: _Optional[str] = ...) -> None: ...

class RequestPasswordResetRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class RequestPasswordResetResponse(_message.Message):
    __slots__ = ("sent", "message")
    SENT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    sent: bool
    message: str
    def __init__(self, sent: bool = ..., message: _Optional[str] = ...) -> None: ...

class ResetPasswordRequest(_message.Message):
    __slots__ = ("token", "new_password")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    NEW_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    token: str
    new_password: str
    def __init__(self, token: _Optional[str] = ..., new_password: _Optional[str] = ...) -> None: ...

class GetUserPreferencesRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class GetUserPreferencesResponse(_message.Message):
    __slots__ = ("preferences",)
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    preferences: UserPreferences
    def __init__(self, preferences: _Optional[_Union[UserPreferences, _Mapping]] = ...) -> None: ...

class UpdateUserPreferencesRequest(_message.Message):
    __slots__ = ("user_id", "preferences", "update_mask")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    preferences: UserPreferences
    update_mask: _field_mask_pb2.FieldMask
    def __init__(self, user_id: _Optional[str] = ..., preferences: _Optional[_Union[UserPreferences, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class UpdateUserPreferencesResponse(_message.Message):
    __slots__ = ("preferences",)
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    preferences: UserPreferences
    def __init__(self, preferences: _Optional[_Union[UserPreferences, _Mapping]] = ...) -> None: ...
