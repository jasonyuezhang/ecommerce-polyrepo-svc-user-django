# gRPC Server Setup Guide

This guide explains how to set up and use the gRPC server for the User Service.

## Overview

The User Service provides both REST API (port 8000) and gRPC (port 50051) interfaces for inter-service communication. The gRPC service implements all 23 RPC methods defined in `user.proto`.

## Architecture

```
svc-user-django/
├── users/
│   ├── grpc_generated/          # Generated Python stubs from proto files
│   │   └── proto/
│   │       ├── user/v1/
│   │       │   ├── user_pb2.py         # Generated message classes
│   │       │   └── user_pb2_grpc.py    # Generated service stubs
│   │       └── common/v1/
│   │           └── common_pb2.py       # Common types
│   ├── grpc_servicer.py         # Implementation of all RPC methods
│   ├── grpc_server_new.py       # Production gRPC server
│   └── management/commands/
│       └── rungrpc.py           # Django management command
├── scripts/
│   └── generate_grpc_stubs.sh   # Script to regenerate stubs from proto
└── tests/
    └── test_grpc_client.py      # Test client demonstrating usage
```

## Setup

### 1. Generate gRPC Stubs

First, generate Python stubs from the proto files:

```bash
# Ensure you're in the svc-user-django directory
cd svc-user-django

# Install gRPC tools
pip install grpcio-tools protobuf

# Generate stubs
bash scripts/generate_grpc_stubs.sh
```

This creates:
- `users/grpc_generated/proto/user/v1/user_pb2.py` - Message types
- `users/grpc_generated/proto/user/v1/user_pb2_grpc.py` - Service stubs
- `users/grpc_generated/proto/common/v1/common_pb2.py` - Common types

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `grpcio>=1.59,<2.0` - gRPC runtime
- `grpcio-tools>=1.59,<2.0` - Code generation tools
- `protobuf>=4.24,<5.0` - Protocol buffers

### 3. Run Database Migrations

```bash
python manage.py migrate
```

## Running the Server

### Option 1: Using Django Management Command

```bash
# Run with default settings (port 50051, 10 workers)
python manage.py rungrpc

# Run with custom port
python manage.py rungrpc --port 50052

# Run with more workers
python manage.py rungrpc --workers 20
```

### Option 2: Direct Execution

```bash
# Run the server module directly
python users/grpc_server_new.py
```

### Option 3: Docker Compose (Recommended for Development)

Run both REST API and gRPC server together:

```bash
docker-compose -f docker-compose.grpc.yml up
```

This starts:
- PostgreSQL on port 5432
- Django REST API on port 8000
- gRPC server on port 50051

## Testing the Server

### Using the Test Client

```bash
# Run the test client
python tests/test_grpc_client.py

# Connect to a different host/port
python tests/test_grpc_client.py --host localhost --port 50051
```

The test client runs through all major operations:
1. Health check
2. List users
3. Create user
4. Get user by ID
5. Get user by email
6. Search users
7. Deactivate user

### Manual Testing with grpcurl

Install [grpcurl](https://github.com/fullstorydev/grpcurl):

```bash
# Install grpcurl (macOS)
brew install grpcurl

# List available services
grpcurl -plaintext localhost:50051 list

# List methods in UserService
grpcurl -plaintext localhost:50051 list user.v1.UserService

# Call health check
grpcurl -plaintext localhost:50051 user.v1.UserService/HealthCheck

# Get user by ID
grpcurl -plaintext -d '{"user_id": "123e4567-e89b-12d3-a456-426614174000"}' \
  localhost:50051 user.v1.UserService/GetUser

# List users
grpcurl -plaintext -d '{"pagination": {"page_size": 10}}' \
  localhost:50051 user.v1.UserService/ListUsers
```

## Implemented RPC Methods

### Core User Operations (Fully Implemented)
- ✅ `CreateUser` - Register a new user account
- ✅ `GetUser` - Retrieve user by ID
- ✅ `GetUserByEmail` - Retrieve user by email
- ✅ `UpdateUser` - Update user information
- ✅ `DeleteUser` - Permanently delete a user
- ✅ `DeactivateUser` - Soft delete (deactivate account)
- ✅ `ReactivateUser` - Reactivate deactivated account
- ✅ `ListUsers` - List users with pagination and filters
- ✅ `SearchUsers` - Search users by query
- ✅ `HealthCheck` - Service health status

### Address Management (Stub Implementation)
- ⚠️ `UpdateUserProfile` - Update profile information
- ⚠️ `AddUserAddress` - Add address to user
- ⚠️ `UpdateUserAddress` - Update existing address
- ⚠️ `DeleteUserAddress` - Remove address
- ⚠️ `ListUserAddresses` - List all user addresses
- ⚠️ `SetDefaultAddress` - Set default shipping/billing address

### Authentication & Verification (Stub Implementation)
- ⚠️ `VerifyEmail` - Send verification email
- ⚠️ `ConfirmEmailVerification` - Confirm email verification token
- ⚠️ `ChangePassword` - Change user password
- ⚠️ `RequestPasswordReset` - Initiate password reset
- ⚠️ `ResetPassword` - Complete password reset

### Preferences (Stub Implementation)
- ⚠️ `GetUserPreferences` - Get notification preferences
- ⚠️ `UpdateUserPreferences` - Update preferences

> ⚠️ Stub implementations return `UNIMPLEMENTED` error. These need to be fully implemented based on requirements.

## Configuration

### Environment Variables

```bash
# gRPC Server Configuration
GRPC_PORT=50051              # Port to listen on
GRPC_MAX_WORKERS=10          # Thread pool size

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Django
DJANGO_SETTINGS_MODULE=user_service.settings
DEBUG=true
SECRET_KEY=your-secret-key
```

### Django Settings

The `GRPC_PORT` setting is defined in `user_service/settings.py`:

```python
GRPC_PORT = int(os.getenv('GRPC_PORT', 50051))
```

## Client Usage Examples

### Python Client

```python
import grpc
from users.grpc_generated.proto.user.v1 import user_pb2, user_pb2_grpc

# Create channel
channel = grpc.insecure_channel('localhost:50051')
stub = user_pb2_grpc.UserServiceStub(channel)

# Create a user
request = user_pb2.CreateUserRequest(
    email="john@example.com",
    password="SecurePassword123!",
    first_name="John",
    last_name="Doe"
)
response = stub.CreateUser(request)
print(f"Created user: {response.user.id}")

# Get user by email
request = user_pb2.GetUserByEmailRequest(email="john@example.com")
response = stub.GetUserByEmail(request)
print(f"Found: {response.user.first_name} {response.user.last_name}")

# List users with pagination
request = user_pb2.ListUsersRequest(
    pagination=common_pb2.PaginationRequest(page_size=20)
)
response = stub.ListUsers(request)
print(f"Total users: {response.pagination.total_count}")
```

### Go Client (Example)

```go
package main

import (
    "context"
    "log"

    "google.golang.org/grpc"
    pb "github.com/ecommerce/proto-schemas/gen/go/user/v1"
)

func main() {
    // Connect to server
    conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    client := pb.NewUserServiceClient(conn)

    // Get user by email
    resp, err := client.GetUserByEmail(context.Background(), &pb.GetUserByEmailRequest{
        Email: "john@example.com",
    })
    if err != nil {
        log.Fatal(err)
    }

    log.Printf("Found user: %s %s", resp.User.FirstName, resp.User.LastName)
}
```

## Error Handling

The server returns standard gRPC status codes:

- `OK` - Success
- `NOT_FOUND` - User not found
- `ALREADY_EXISTS` - User with email already exists
- `INVALID_ARGUMENT` - Invalid request parameters
- `UNIMPLEMENTED` - Method not yet implemented
- `INTERNAL` - Server error

Example error handling in Python:

```python
import grpc

try:
    response = stub.GetUser(request)
except grpc.RpcError as e:
    if e.code() == grpc.StatusCode.NOT_FOUND:
        print("User not found")
    elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
        print(f"Invalid argument: {e.details()}")
    else:
        print(f"Error: {e.code()} - {e.details()}")
```

## Performance Tuning

### Server Options

The server is configured with these performance options:

```python
options=[
    ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50MB max send
    ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50MB max receive
    ('grpc.keepalive_time_ms', 10000),  # Send keepalive every 10s
    ('grpc.keepalive_timeout_ms', 5000),  # Wait 5s for keepalive ack
    ('grpc.keepalive_permit_without_calls', True),  # Allow keepalive without calls
    ('grpc.http2.max_pings_without_data', 0),  # Unlimited pings
]
```

### Recommendations

- **Thread Pool Size**: Set `GRPC_MAX_WORKERS` based on expected concurrent RPCs (default: 10)
- **Database Connections**: Ensure Django `CONN_MAX_AGE` is set for connection pooling
- **Load Balancing**: Use a load balancer (e.g., nginx with grpc_pass) for multiple instances

## Troubleshooting

### Server won't start

```bash
# Check if port is already in use
lsof -i :50051

# Check Django settings
python manage.py shell
>>> from django.conf import settings
>>> settings.GRPC_PORT
```

### Import errors

```bash
# Regenerate stubs
bash scripts/generate_grpc_stubs.sh

# Verify __init__.py files exist
find users/grpc_generated -name "__init__.py"
```

### Connection refused

```bash
# Verify server is running
grpcurl -plaintext localhost:50051 list

# Check server logs
docker-compose -f docker-compose.grpc.yml logs grpc
```

## Next Steps

1. **Implement remaining methods** - Complete stub implementations for address, auth, and preferences
2. **Add authentication** - Implement JWT token validation for secured RPCs
3. **Add monitoring** - Integrate Prometheus metrics and distributed tracing
4. **Add TLS** - Configure SSL/TLS for production security
5. **Add rate limiting** - Implement rate limiting middleware
6. **Add caching** - Add Redis caching for frequently accessed data

## Resources

- [gRPC Python Documentation](https://grpc.io/docs/languages/python/)
- [Protocol Buffers Guide](https://developers.google.com/protocol-buffers)
- [gRPC Best Practices](https://grpc.io/docs/guides/performance/)
- [Proto Schema](/proto-schemas/proto/user/v1/user.proto)
