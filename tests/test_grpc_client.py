"""
Test gRPC client for UserService.

This script demonstrates how to call the gRPC service and can be used for testing.

Usage:
    python tests/test_grpc_client.py
"""
import os
import sys
import grpc
from google.protobuf.empty_pb2 import Empty

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from users.grpc_generated.proto.user.v1 import user_pb2, user_pb2_grpc
from users.grpc_generated.proto.common.v1 import common_pb2


def test_health_check(stub):
    """Test the health check endpoint."""
    print("\n=== Testing HealthCheck ===")
    try:
        response = stub.HealthCheck(Empty())
        print(f"Status: {common_pb2.HealthStatus.Name(response.status)}")
        print(f"Version: {response.version}")
        print(f"Components: {dict(response.components)}")
        print("✓ HealthCheck passed")
        return True
    except grpc.RpcError as e:
        print(f"✗ HealthCheck failed: {e.code()} - {e.details()}")
        return False


def test_create_user(stub):
    """Test creating a user."""
    print("\n=== Testing CreateUser ===")
    try:
        request = user_pb2.CreateUserRequest(
            email="test@example.com",
            password="SecurePassword123!",
            first_name="Test",
            last_name="User",
            display_name="testuser"
        )
        response = stub.CreateUser(request)
        print(f"Created user: {response.user.email} (ID: {response.user.id})")
        print(f"Status: {user_pb2.UserStatus.Name(response.user.status)}")
        print("✓ CreateUser passed")
        return response.user.id
    except grpc.RpcError as e:
        print(f"✗ CreateUser failed: {e.code()} - {e.details()}")
        return None


def test_get_user(stub, user_id):
    """Test getting a user by ID."""
    print("\n=== Testing GetUser ===")
    try:
        request = user_pb2.GetUserRequest(user_id=user_id)
        response = stub.GetUser(request)
        print(f"Found user: {response.user.email}")
        print(f"Name: {response.user.first_name} {response.user.last_name}")
        print(f"Status: {user_pb2.UserStatus.Name(response.user.status)}")
        print("✓ GetUser passed")
        return True
    except grpc.RpcError as e:
        print(f"✗ GetUser failed: {e.code()} - {e.details()}")
        return False


def test_get_user_by_email(stub, email):
    """Test getting a user by email."""
    print("\n=== Testing GetUserByEmail ===")
    try:
        request = user_pb2.GetUserByEmailRequest(email=email)
        response = stub.GetUserByEmail(request)
        print(f"Found user: {response.user.email} (ID: {response.user.id})")
        print("✓ GetUserByEmail passed")
        return True
    except grpc.RpcError as e:
        print(f"✗ GetUserByEmail failed: {e.code()} - {e.details()}")
        return False


def test_list_users(stub):
    """Test listing users."""
    print("\n=== Testing ListUsers ===")
    try:
        request = user_pb2.ListUsersRequest(
            pagination=common_pb2.PaginationRequest(page_size=10)
        )
        response = stub.ListUsers(request)
        print(f"Total users: {response.pagination.total_count}")
        print(f"Returned: {len(response.users)} users")
        for i, user in enumerate(response.users[:3], 1):
            print(f"  {i}. {user.email} - {user.first_name} {user.last_name}")
        print("✓ ListUsers passed")
        return True
    except grpc.RpcError as e:
        print(f"✗ ListUsers failed: {e.code()} - {e.details()}")
        return False


def test_search_users(stub, query):
    """Test searching users."""
    print("\n=== Testing SearchUsers ===")
    try:
        request = user_pb2.SearchUsersRequest(
            query=query,
            pagination=common_pb2.PaginationRequest(page_size=10)
        )
        response = stub.SearchUsers(request)
        print(f"Found {len(response.users)} users matching '{query}'")
        for user in response.users[:5]:
            print(f"  - {user.email}")
        print("✓ SearchUsers passed")
        return True
    except grpc.RpcError as e:
        print(f"✗ SearchUsers failed: {e.code()} - {e.details()}")
        return False


def test_deactivate_user(stub, user_id):
    """Test deactivating a user."""
    print("\n=== Testing DeactivateUser ===")
    try:
        request = user_pb2.DeactivateUserRequest(
            user_id=user_id,
            reason="Test deactivation"
        )
        response = stub.DeactivateUser(request)
        print(f"Deactivated user: {response.user.email}")
        print(f"Status: {user_pb2.UserStatus.Name(response.user.status)}")
        print("✓ DeactivateUser passed")
        return True
    except grpc.RpcError as e:
        print(f"✗ DeactivateUser failed: {e.code()} - {e.details()}")
        return False


def run_tests(host='localhost', port=50051):
    """Run all gRPC tests."""
    print(f"Connecting to gRPC server at {host}:{port}...")

    # Create channel and stub
    channel = grpc.insecure_channel(f'{host}:{port}')
    stub = user_pb2_grpc.UserServiceStub(channel)

    try:
        # Test 1: Health check
        if not test_health_check(stub):
            print("\n⚠ Health check failed, server may not be running")
            return

        # Test 2: List existing users
        test_list_users(stub)

        # Test 3: Create a new user
        user_id = test_create_user(stub)
        if not user_id:
            print("\n⚠ Could not create user, some tests will be skipped")
            return

        # Test 4: Get user by ID
        test_get_user(stub, user_id)

        # Test 5: Get user by email
        test_get_user_by_email(stub, "test@example.com")

        # Test 6: Search users
        test_search_users(stub, "test")

        # Test 7: Deactivate user
        test_deactivate_user(stub, user_id)

        print("\n" + "=" * 50)
        print("✓ All tests completed!")
        print("=" * 50)

    finally:
        channel.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Test gRPC UserService')
    parser.add_argument('--host', default='localhost', help='gRPC server host')
    parser.add_argument('--port', type=int, default=50051, help='gRPC server port')

    args = parser.parse_args()
    run_tests(host=args.host, port=args.port)
