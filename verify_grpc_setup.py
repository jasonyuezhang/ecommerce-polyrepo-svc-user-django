#!/usr/bin/env python3
"""
Verification script to ensure gRPC setup is complete.
Run this to check if all required files and dependencies are in place.
"""
import sys
import os
from pathlib import Path

def check_file(path, description):
    """Check if a file exists."""
    full_path = Path(path)
    exists = full_path.exists()
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {path}")
    return exists

def check_import(module_name, description):
    """Check if a Python module can be imported."""
    try:
        __import__(module_name)
        print(f"✓ {description}: {module_name}")
        return True
    except ImportError as e:
        print(f"✗ {description}: {module_name} - {e}")
        return False

def main():
    print("=" * 60)
    print("gRPC Setup Verification")
    print("=" * 60)
    print()

    checks = []

    print("📦 Checking Python Dependencies:")
    checks.append(check_import("grpc", "gRPC runtime"))
    checks.append(check_import("grpc_tools", "gRPC tools"))
    checks.append(check_import("google.protobuf", "Protocol Buffers"))
    checks.append(check_import("django", "Django"))
    print()

    print("📁 Checking Generated Proto Files:")
    checks.append(check_file("users/grpc_generated/proto/user/v1/user_pb2.py", "User messages"))
    checks.append(check_file("users/grpc_generated/proto/user/v1/user_pb2_grpc.py", "User service stubs"))
    checks.append(check_file("users/grpc_generated/proto/common/v1/common_pb2.py", "Common messages"))
    print()

    print("🔧 Checking Implementation Files:")
    checks.append(check_file("users/grpc_servicer.py", "gRPC servicer implementation"))
    checks.append(check_file("users/grpc_server_new.py", "gRPC server"))
    checks.append(check_file("users/management/commands/rungrpc.py", "Django management command"))
    print()

    print("📜 Checking Scripts:")
    checks.append(check_file("scripts/generate_grpc_stubs.sh", "Stub generation script"))
    checks.append(check_file("scripts/start_grpc_dev.sh", "Development start script"))
    print()

    print("🧪 Checking Test Files:")
    checks.append(check_file("tests/test_grpc_client.py", "Test client"))
    print()

    print("📖 Checking Documentation:")
    checks.append(check_file("docs/GRPC_SETUP.md", "Setup guide"))
    checks.append(check_file("docs/GRPC_IMPLEMENTATION_SUMMARY.md", "Implementation summary"))
    print()

    print("=" * 60)
    passed = sum(checks)
    total = len(checks)
    success_rate = (passed / total) * 100 if total > 0 else 0

    print(f"Results: {passed}/{total} checks passed ({success_rate:.0f}%)")
    print("=" * 60)
    print()

    if passed == total:
        print("✅ All checks passed! gRPC setup is complete.")
        print()
        print("Next steps:")
        print("1. Start the server: bash scripts/start_grpc_dev.sh")
        print("2. Run tests: python tests/test_grpc_client.py")
        print("3. Read docs: docs/GRPC_SETUP.md")
        return 0
    else:
        print("⚠️  Some checks failed. Please review the output above.")
        print()
        if not check_import("grpc", ""):
            print("💡 Install dependencies: pip install -r requirements.txt")
        if not check_file("users/grpc_generated/proto/user/v1/user_pb2.py", ""):
            print("💡 Generate stubs: bash scripts/generate_grpc_stubs.sh")
        return 1

if __name__ == "__main__":
    sys.exit(main())
