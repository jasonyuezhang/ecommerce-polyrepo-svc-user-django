"""
gRPC servicer implementation for UserService.

This module implements all RPC methods defined in user.proto using Django models.
"""
import logging
from datetime import datetime
from typing import Optional

import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.empty_pb2 import Empty
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.db import models
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from users.models import User
from users.grpc_generated.proto.user.v1 import user_pb2, user_pb2_grpc
from users.grpc_generated.proto.common.v1 import common_pb2

logger = logging.getLogger(__name__)


class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    """Implementation of UserService gRPC service."""

    def _user_to_proto(self, user: User) -> user_pb2.User:
        """Convert Django User model to protobuf User message."""
        proto_user = user_pb2.User(
            id=str(user.id),
            email=user.email,
            display_name=user.username or user.get_full_name(),
            first_name=user.first_name,
            last_name=user.last_name,
            email_verified=user.is_verified,
            phone_verified=False,  # Add phone verification field to model if needed
        )

        # Set phone number
        if user.phone_number:
            # For now, just set e164 format
            proto_user.phone.e164 = user.phone_number

        # Set status
        if not user.is_active:
            proto_user.status = user_pb2.USER_STATUS_DEACTIVATED
        elif not user.is_verified:
            proto_user.status = user_pb2.USER_STATUS_PENDING_VERIFICATION
        else:
            proto_user.status = user_pb2.USER_STATUS_ACTIVE

        # Set roles
        if user.is_superuser:
            proto_user.roles.append(user_pb2.USER_ROLE_ADMIN)
        else:
            proto_user.roles.append(user_pb2.USER_ROLE_CUSTOMER)

        # Set audit info
        if user.date_joined:
            created_ts = Timestamp()
            created_ts.FromDatetime(user.date_joined)
            proto_user.audit.created_at.CopyFrom(created_ts)

        if user.updated_at:
            updated_ts = Timestamp()
            updated_ts.FromDatetime(user.updated_at)
            proto_user.audit.updated_at.CopyFrom(updated_ts)

        if user.last_login:
            last_login_ts = Timestamp()
            last_login_ts.FromDatetime(user.last_login)
            proto_user.last_login_at.CopyFrom(last_login_ts)

        return proto_user

    def CreateUser(self, request: user_pb2.CreateUserRequest, context) -> user_pb2.CreateUserResponse:
        """Create a new user account."""
        try:
            # Validate email
            if not request.email:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details('Email is required')
                return user_pb2.CreateUserResponse()

            # Check if user already exists
            if User.objects.filter(email=request.email.lower()).exists():
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details(f'User with email {request.email} already exists')
                return user_pb2.CreateUserResponse()

            # Create user
            with transaction.atomic():
                user = User.objects.create_user(
                    email=request.email.lower(),
                    password=request.password,
                    first_name=request.first_name,
                    last_name=request.last_name,
                    username=request.display_name or request.email.split('@')[0],
                )

                if request.phone and request.phone.e164:
                    user.phone_number = request.phone.e164

                user.save()

                logger.info(f'Created user: {user.email} (ID: {user.id})')

            return user_pb2.CreateUserResponse(user=self._user_to_proto(user))

        except Exception as e:
            logger.error(f'Error creating user: {e}', exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.CreateUserResponse()

    def GetUser(self, request: user_pb2.GetUserRequest, context) -> user_pb2.GetUserResponse:
        """Get user by ID."""
        try:
            user = User.objects.get(id=request.user_id)
            return user_pb2.GetUserResponse(user=self._user_to_proto(user))
        except User.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'User not found: {request.user_id}')
            return user_pb2.GetUserResponse()
        except Exception as e:
            logger.error(f'Error getting user: {e}', exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.GetUserResponse()

    def GetUserByEmail(self, request: user_pb2.GetUserByEmailRequest, context) -> user_pb2.GetUserByEmailResponse:
        """Get user by email address."""
        try:
            user = User.objects.get(email=request.email.lower())
            return user_pb2.GetUserByEmailResponse(user=self._user_to_proto(user))
        except User.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'User not found: {request.email}')
            return user_pb2.GetUserByEmailResponse()
        except Exception as e:
            logger.error(f'Error getting user by email: {e}', exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.GetUserByEmailResponse()

    def UpdateUser(self, request: user_pb2.UpdateUserRequest, context) -> user_pb2.UpdateUserResponse:
        """Update user information."""
        try:
            user = User.objects.get(id=request.user_id)

            # Update fields based on field mask
            if request.update_mask and request.update_mask.paths:
                for path in request.update_mask.paths:
                    if path == 'first_name':
                        user.first_name = request.user.first_name
                    elif path == 'last_name':
                        user.last_name = request.user.last_name
                    elif path == 'display_name':
                        user.username = request.user.display_name
                    elif path == 'phone':
                        user.phone_number = request.user.phone.e164 if request.user.phone else ''
            else:
                # Update all fields if no mask provided
                user.first_name = request.user.first_name
                user.last_name = request.user.last_name
                user.username = request.user.display_name
                if request.user.phone and request.user.phone.e164:
                    user.phone_number = request.user.phone.e164

            user.save()
            logger.info(f'Updated user: {user.email} (ID: {user.id})')

            return user_pb2.UpdateUserResponse(user=self._user_to_proto(user))

        except User.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'User not found: {request.user_id}')
            return user_pb2.UpdateUserResponse()
        except Exception as e:
            logger.error(f'Error updating user: {e}', exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.UpdateUserResponse()

    def DeleteUser(self, request: user_pb2.DeleteUserRequest, context) -> Empty:
        """Permanently delete a user account."""
        try:
            user = User.objects.get(id=request.user_id)
            email = user.email
            user.delete()
            logger.warning(f'Deleted user: {email} (ID: {request.user_id}), reason: {request.reason}')
            return Empty()
        except User.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'User not found: {request.user_id}')
            return Empty()
        except Exception as e:
            logger.error(f'Error deleting user: {e}', exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return Empty()

    def DeactivateUser(self, request: user_pb2.DeactivateUserRequest, context) -> user_pb2.DeactivateUserResponse:
        """Deactivate a user account (soft delete)."""
        try:
            user = User.objects.get(id=request.user_id)
            user.is_active = False
            user.save()
            logger.info(f'Deactivated user: {user.email} (ID: {user.id}), reason: {request.reason}')
            return user_pb2.DeactivateUserResponse(user=self._user_to_proto(user))
        except User.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'User not found: {request.user_id}')
            return user_pb2.DeactivateUserResponse()
        except Exception as e:
            logger.error(f'Error deactivating user: {e}', exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.DeactivateUserResponse()

    def ReactivateUser(self, request: user_pb2.ReactivateUserRequest, context) -> user_pb2.ReactivateUserResponse:
        """Reactivate a previously deactivated account."""
        try:
            user = User.objects.get(id=request.user_id)
            user.is_active = True
            user.save()
            logger.info(f'Reactivated user: {user.email} (ID: {user.id})')
            return user_pb2.ReactivateUserResponse(user=self._user_to_proto(user))
        except User.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'User not found: {request.user_id}')
            return user_pb2.ReactivateUserResponse()
        except Exception as e:
            logger.error(f'Error reactivating user: {e}', exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.ReactivateUserResponse()

    def ListUsers(self, request: user_pb2.ListUsersRequest, context) -> user_pb2.ListUsersResponse:
        """List users with pagination and filtering."""
        try:
            # Get pagination parameters
            page_size = min(request.pagination.page_size or 20, 100)

            # Start with base queryset
            queryset = User.objects.all()

            # Apply status filters
            if request.statuses:
                status_filters = []
                for status in request.statuses:
                    if status == user_pb2.USER_STATUS_ACTIVE:
                        status_filters.append(models.Q(is_active=True, is_verified=True))
                    elif status == user_pb2.USER_STATUS_PENDING_VERIFICATION:
                        status_filters.append(models.Q(is_verified=False))
                    elif status == user_pb2.USER_STATUS_DEACTIVATED:
                        status_filters.append(models.Q(is_active=False))

                if status_filters:
                    from django.db.models import Q
                    combined_filter = status_filters[0]
                    for f in status_filters[1:]:
                        combined_filter |= f
                    queryset = queryset.filter(combined_filter)

            # Apply sorting
            if request.sort and request.sort.field:
                field = request.sort.field
                if request.sort.order == common_pb2.SORT_ORDER_DESC:
                    field = f'-{field}'
                queryset = queryset.order_by(field)
            else:
                queryset = queryset.order_by('-date_joined')

            # Get total count
            total_count = queryset.count()

            # Apply pagination
            users = list(queryset[:page_size])

            # Build response
            proto_users = [self._user_to_proto(user) for user in users]

            pagination = common_pb2.PaginationResponse(
                total_count=total_count,
                has_more=len(users) == page_size and total_count > page_size
            )

            return user_pb2.ListUsersResponse(
                users=proto_users,
                pagination=pagination
            )

        except Exception as e:
            logger.error(f'Error listing users: {e}', exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.ListUsersResponse()

    def SearchUsers(self, request: user_pb2.SearchUsersRequest, context) -> user_pb2.SearchUsersResponse:
        """Search for users by criteria."""
        try:
            from django.db.models import Q

            # Get pagination parameters
            page_size = min(request.pagination.page_size or 20, 100)

            # Build search query
            queryset = User.objects.all()

            if request.query:
                queryset = queryset.filter(
                    Q(email__icontains=request.query) |
                    Q(first_name__icontains=request.query) |
                    Q(last_name__icontains=request.query) |
                    Q(username__icontains=request.query)
                )

            # Apply status filters (same as ListUsers)
            if request.statuses:
                # Similar filtering logic as ListUsers
                pass

            # Get total count
            total_count = queryset.count()

            # Apply pagination
            users = list(queryset[:page_size])

            # Build response
            proto_users = [self._user_to_proto(user) for user in users]

            pagination = common_pb2.PaginationResponse(
                total_count=total_count,
                has_more=len(users) == page_size and total_count > page_size
            )

            return user_pb2.SearchUsersResponse(
                users=proto_users,
                pagination=pagination
            )

        except Exception as e:
            logger.error(f'Error searching users: {e}', exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.SearchUsersResponse()

    def HealthCheck(self, request: Empty, context) -> common_pb2.HealthCheckResponse:
        """Return service health status."""
        try:
            # Check database connectivity
            User.objects.count()

            response = common_pb2.HealthCheckResponse(
                status=common_pb2.HEALTH_STATUS_HEALTHY,
                version='1.0.0'
            )

            # Add component health
            response.components['database'] = common_pb2.HEALTH_STATUS_HEALTHY

            # Set checked_at timestamp
            now = Timestamp()
            now.FromDatetime(datetime.utcnow())
            response.checked_at.CopyFrom(now)

            return response

        except Exception as e:
            logger.error(f'Health check failed: {e}', exc_info=True)
            response = common_pb2.HealthCheckResponse(
                status=common_pb2.HEALTH_STATUS_UNHEALTHY,
                version='1.0.0'
            )
            response.components['database'] = common_pb2.HEALTH_STATUS_UNHEALTHY
            return response

    # Stub implementations for other methods (to be fully implemented later)
    def UpdateUserProfile(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not yet implemented')
        return user_pb2.UpdateUserProfileResponse()

    def AddUserAddress(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not yet implemented')
        return user_pb2.AddUserAddressResponse()

    def UpdateUserAddress(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not yet implemented')
        return user_pb2.UpdateUserAddressResponse()

    def DeleteUserAddress(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not yet implemented')
        return Empty()

    def ListUserAddresses(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not yet implemented')
        return user_pb2.ListUserAddressesResponse()

    def SetDefaultAddress(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not yet implemented')
        return user_pb2.SetDefaultAddressResponse()

    def VerifyEmail(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not yet implemented')
        return user_pb2.VerifyEmailResponse()

    def ConfirmEmailVerification(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not yet implemented')
        return user_pb2.ConfirmEmailVerificationResponse()

    def ChangePassword(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not yet implemented')
        return Empty()

    def RequestPasswordReset(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not yet implemented')
        return user_pb2.RequestPasswordResetResponse()

    def ResetPassword(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not yet implemented')
        return Empty()

    def GetUserPreferences(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not yet implemented')
        return user_pb2.GetUserPreferencesResponse()

    def UpdateUserPreferences(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not yet implemented')
        return user_pb2.UpdateUserPreferencesResponse()
