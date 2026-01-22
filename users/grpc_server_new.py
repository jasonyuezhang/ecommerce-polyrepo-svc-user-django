"""
Production gRPC server implementation for the user service.

This module provides a fully-functional gRPC server using generated proto stubs.
It runs on port 50051 (configurable via GRPC_PORT env var) alongside Django REST API on port 8000.
"""
import os
import sys
import logging
import signal
from concurrent import futures
import grpc

# Add parent directory to path for Django settings
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_service.settings')

import django
django.setup()

from django.conf import settings
from users.grpc_servicer import UserServiceServicer
from users.grpc_generated.proto.user.v1 import user_pb2_grpc

logger = logging.getLogger(__name__)


class GrpcServer:
    """Production gRPC server for user service."""

    def __init__(self, port: int = 50051, max_workers: int = 10):
        """
        Initialize gRPC server.

        Args:
            port: Port to listen on (default: 50051)
            max_workers: Maximum number of worker threads
        """
        self.port = port
        self.max_workers = max_workers
        self.server = None

    def start(self):
        """Start the gRPC server."""
        # Create thread pool
        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=self.max_workers),
            options=[
                ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50MB
                ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50MB
                ('grpc.keepalive_time_ms', 10000),
                ('grpc.keepalive_timeout_ms', 5000),
                ('grpc.keepalive_permit_without_calls', True),
                ('grpc.http2.max_pings_without_data', 0),
            ]
        )

        # Add servicer to server
        servicer = UserServiceServicer()
        user_pb2_grpc.add_UserServiceServicer_to_server(servicer, self.server)

        # Bind to port
        self.server.add_insecure_port(f'[::]:{self.port}')

        # Start server
        self.server.start()

        logger.info(f'✓ gRPC server started on port {self.port}')
        logger.info(f'  Workers: {self.max_workers}')
        logger.info(f'  Service: UserService (23 RPC methods)')
        print(f'gRPC UserService listening on port {self.port}')

    def stop(self, grace_period: int = 5):
        """
        Stop the gRPC server gracefully.

        Args:
            grace_period: Seconds to wait for pending RPCs to complete
        """
        if self.server:
            logger.info(f'Stopping gRPC server (grace period: {grace_period}s)...')
            self.server.stop(grace_period)
            logger.info('gRPC server stopped')

    def wait_for_termination(self):
        """Block until the server terminates."""
        if self.server:
            self.server.wait_for_termination()


def serve():
    """
    Run the gRPC server.

    Reads configuration from Django settings and environment variables.
    Handles graceful shutdown on SIGINT and SIGTERM.
    """
    # Get configuration
    port = getattr(settings, 'GRPC_PORT', 50051)
    max_workers = int(os.getenv('GRPC_MAX_WORKERS', '10'))

    # Create and start server
    server = GrpcServer(port=port, max_workers=max_workers)

    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        logger.info(f'Received signal {signum}, shutting down...')
        server.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start server
    logger.info('Starting gRPC UserService server...')
    logger.info(f'Django settings module: {os.getenv("DJANGO_SETTINGS_MODULE")}')
    logger.info(f'Database: {settings.DATABASES["default"]["NAME"]}')

    server.start()

    # Keep server running
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info('Keyboard interrupt received')
        server.stop()
        print('\nServer stopped.')


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )

    serve()
