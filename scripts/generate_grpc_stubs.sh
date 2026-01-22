#!/bin/bash
# Generate Python gRPC stubs from proto files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PROTO_ROOT="$(cd "$PROJECT_ROOT/../proto-schemas" && pwd)"
OUTPUT_DIR="$PROJECT_ROOT/users/grpc_generated"

echo "Generating gRPC stubs..."
echo "Proto root: $PROTO_ROOT"
echo "Output dir: $OUTPUT_DIR"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Generate Python stubs from proto files
python -m grpc_tools.protoc \
    -I"$PROTO_ROOT" \
    --python_out="$OUTPUT_DIR" \
    --grpc_python_out="$OUTPUT_DIR" \
    --pyi_out="$OUTPUT_DIR" \
    "$PROTO_ROOT/proto/user/v1/user.proto" \
    "$PROTO_ROOT/proto/common/v1/common.proto"

echo "Stubs generated successfully!"

# Fix import paths in generated files
echo "Fixing import paths..."
cd "$OUTPUT_DIR"

# Fix imports in user_pb2.py
if [ -f "proto/user/v1/user_pb2.py" ]; then
    sed -i.bak 's/from proto.common.v1 import common_pb2/from users.grpc_generated.proto.common.v1 import common_pb2/g' proto/user/v1/user_pb2.py
    sed -i.bak 's/from proto.user.v1 import user_pb2/from users.grpc_generated.proto.user.v1 import user_pb2/g' proto/user/v1/user_pb2_grpc.py
    rm -f proto/user/v1/*.bak
fi

echo "Import paths fixed!"
echo "Done!"
