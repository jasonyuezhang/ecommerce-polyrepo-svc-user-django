"""
Django management command to run the gRPC server.

Usage:
    python manage.py rungrpc
    python manage.py rungrpc --port 50052
    python manage.py rungrpc --workers 20
"""
from django.core.management.base import BaseCommand
from users.grpc_server_new import serve, GrpcServer


class Command(BaseCommand):
    help = 'Start the gRPC server for inter-service communication'

    def add_arguments(self, parser):
        parser.add_argument(
            '--port',
            type=int,
            default=50051,
            help='Port to listen on (default: 50051)',
        )
        parser.add_argument(
            '--workers',
            type=int,
            default=10,
            help='Maximum number of worker threads (default: 10)',
        )

    def handle(self, *args, **options):
        port = options['port']
        workers = options['workers']

        self.stdout.write(self.style.SUCCESS(
            f'Starting gRPC server on port {port} with {workers} workers...'
        ))

        server = GrpcServer(port=port, max_workers=workers)
        server.start()

        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nShutting down...'))
            server.stop()
            self.stdout.write(self.style.SUCCESS('Server stopped'))
