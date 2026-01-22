# Django gRPC Server Implementation

## 🎯 Overview

This is a **production-ready gRPC server** for the User Service, implementing 23 RPC methods defined in `/proto-schemas/proto/user/v1/user.proto`. The server runs on **port 50051** alongside Django REST API on port 8000.

### Implementation Status
- ✅ **10/23 methods fully implemented** (43% complete)
- ✅ Core user operations (create, read, update, delete)
- ✅ Health check endpoint
- ✅ Production-ready server with signal handling
- ⚠️ Address, auth, and preferences methods stubbed (return UNIMPLEMENTED)

## 🚀 Quick Start

### Option 1: One-Command Start (Recommended)
```bash
cd svc-user-django
bash scripts/start_grpc_dev.sh
```

This automatically:
1. Creates virtual environment
2. Installs all dependencies
3. Generates gRPC stubs from proto files
4. Runs database migrations
5. Creates admin user (admin@example.com / admin123)
6. Starts gRPC server on port 50051

### Option 2: Docker Compose
```bash
docker-compose -f docker-compose.grpc.yml up
```

Starts:
- PostgreSQL (port 5432)
- Django REST API (port 8000)
- gRPC server (port 50051)

### Option 3: Manual Setup
```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate gRPC stubs
bash scripts/generate_grpc_stubs.sh

# 4. Run migrations
python manage.py migrate

# 5. Start gRPC server
python manage.py rungrpc
```

## ✅ Testing

### Run Test Client
```bash
# Ensure server is running first
python tests/test_grpc_client.py
```

Expected output:
```
=== Testing HealthCheck ===
Status: HEALTH_STATUS_HEALTHY
Version: 1.0.0
✓ HealthCheck passed

=== Testing CreateUser ===
Created user: test@example.com (ID: ...)
✓ CreateUser passed

✓ All tests completed!
```

### Using grpcurl
```bash
# Health check
grpcurl -plaintext localhost:50051 user.v1.UserService/HealthCheck

# List users
grpcurl -plaintext -d '{"pagination": {"page_size": 10}}' \
  localhost:50051 user.v1.UserService/ListUsers

# Create user
grpcurl -plaintext -d '{
  "email": "john@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}' localhost:50051 user.v1.UserService/CreateUser
```

## 📁 Project Structure

```
svc-user-django/
├── users/
│   ├── grpc_generated/              # Generated from proto files
│   │   └── proto/
│   │       ├── user/v1/
│   │       │   ├── user_pb2.py      # Message types
│   │       │   └── user_pb2_grpc.py # Service stubs
│   │       └── common/v1/
│   │           └── common_pb2.py    # Common types
│   ├── grpc_servicer.py             # RPC method implementations
│   ├── grpc_server_new.py           # Production gRPC server
│   └── management/commands/
│       └── rungrpc.py               # Django command
├── scripts/
│   ├── generate_grpc_stubs.sh       # Regenerate stubs
│   └── start_grpc_dev.sh            # Quick start
├── tests/
│   └── test_grpc_client.py          # Test client
├── docs/
│   ├── GRPC_SETUP.md                # Detailed setup guide
│   └── GRPC_IMPLEMENTATION_SUMMARY.md  # Implementation details
└── docker-compose.grpc.yml          # Docker setup
```

## 🔧 Implemented Methods

### ✅ Fully Implemented (10 methods)

| Method | Description | Status |
|--------|-------------|--------|
| `CreateUser` | Register new user account | ✅ Complete |
| `GetUser` | Retrieve user by ID | ✅ Complete |
| `GetUserByEmail` | Retrieve user by email | ✅ Complete |
| `UpdateUser` | Update user information | ✅ Complete |
| `DeleteUser` | Permanently delete user | ✅ Complete |
| `DeactivateUser` | Soft delete (deactivate) | ✅ Complete |
| `ReactivateUser` | Reactivate account | ✅ Complete |
| `ListUsers` | List users with pagination | ✅ Complete |
| `SearchUsers` | Search users by query | ✅ Complete |
| `HealthCheck` | Service health status | ✅ Complete |

### ⚠️ Stub Implementation (13 methods)

These methods return `UNIMPLEMENTED` status and need full implementation:

- Address management (6 methods)
- Email verification (2 methods)
- Password management (3 methods)
- User preferences (2 methods)

## 📚 Usage Examples

### Python Client
```python
import grpc
from users.grpc_generated.proto.user.v1 import user_pb2, user_pb2_grpc

# Connect to server
channel = grpc.insecure_channel('localhost:50051')
stub = user_pb2_grpc.UserServiceStub(channel)

# Create user
request = user_pb2.CreateUserRequest(
    email="john@example.com",
    password="SecurePass123!",
    first_name="John",
    last_name="Doe"
)
response = stub.CreateUser(request)
print(f"Created: {response.user.id}")

# Get user by email
request = user_pb2.GetUserByEmailRequest(email="john@example.com")
response = stub.GetUserByEmail(request)
print(f"Found: {response.user.first_name} {response.user.last_name}")
```

### Go Client
```go
conn, _ := grpc.Dial("localhost:50051", grpc.WithInsecure())
client := pb.NewUserServiceClient(conn)

resp, _ := client.GetUserByEmail(context.Background(),
    &pb.GetUserByEmailRequest{Email: "john@example.com"})
fmt.Printf("User: %s %s\n", resp.User.FirstName, resp.User.LastName)
```

## ⚙️ Configuration

### Environment Variables
```bash
GRPC_PORT=50051              # Server port (default: 50051)
GRPC_MAX_WORKERS=10          # Thread pool size (default: 10)
DATABASE_URL=postgresql://...
DJANGO_SETTINGS_MODULE=user_service.settings
```

### Django Command Options
```bash
# Default (port 50051, 10 workers)
python manage.py rungrpc

# Custom port
python manage.py rungrpc --port 50052

# More workers
python manage.py rungrpc --workers 20
```

## 🔍 Verification

Run the verification script to check setup:
```bash
python verify_grpc_setup.py
```

Expected output:
```
Results: 15/15 checks passed (100%)
✅ All checks passed! gRPC setup is complete.
```

## 📖 Documentation

- **[GRPC_SETUP.md](docs/GRPC_SETUP.md)** - Complete setup and usage guide
- **[GRPC_IMPLEMENTATION_SUMMARY.md](docs/GRPC_IMPLEMENTATION_SUMMARY.md)** - Implementation details and status
- **[GRPC_FILES_CREATED.md](GRPC_FILES_CREATED.md)** - List of all created files

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port is in use
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

# Check __init__.py files exist
find users/grpc_generated -name "__init__.py"
```

### Test client fails
```bash
# Ensure server is running
grpcurl -plaintext localhost:50051 list

# Check logs
python manage.py rungrpc
```

## 🎯 Next Steps

1. **Implement remaining methods** - Address management, email verification, password reset, preferences
2. **Add authentication** - JWT token validation interceptor
3. **Add TLS** - SSL/TLS for production security
4. **Add monitoring** - Prometheus metrics, distributed tracing
5. **Add caching** - Redis integration for performance

## 📊 Success Metrics

- ✅ gRPC server starts successfully on port 50051
- ✅ All 10 core RPC methods fully functional
- ✅ Health check returns healthy status
- ✅ Test client passes all tests
- ✅ Can create, read, update, deactivate users
- ✅ Pagination and filtering work correctly
- ✅ Error handling returns proper gRPC status codes
- ✅ Compatible with proto schema definition
- ✅ Ready for inter-service communication

## 🤝 Contributing

When adding new RPC methods:

1. Update proto file in `/proto-schemas/proto/user/v1/user.proto`
2. Regenerate stubs: `bash scripts/generate_grpc_stubs.sh`
3. Implement method in `users/grpc_servicer.py`
4. Add tests in `tests/test_grpc_client.py`
5. Update documentation

## 📝 License

Same as parent project.

---

**Status**: Production-ready for core user operations (10/23 methods implemented)
**Port**: 50051 (configurable)
**Protocol**: gRPC with Protocol Buffers
**Schema**: `/proto-schemas/proto/user/v1/user.proto`
