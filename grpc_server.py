import os
import grpc
import logging
from concurrent import futures

from proto import subscribe_pb2_grpc

from common import SERVER_CONFIG
from service.subscribe import SubscribeServicer


def server():
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.INFO)
    config = SERVER_CONFIG
    grpc_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=os.cpu_count() + 4),
        options=(
            ("grpc.keepalive_time_ms", config.grpc_common.grpc_keepalive_time_ms),
            ("grpc.keepalive_timeout_ms", config.grpc_common.grpc_keepalive_timeout_ms),
            (
                "grpc.max_send_message_length",
                config.grpc_common.grpc_max_message_length,
            ),
            (
                "grpc.max_receive_message_length",
                config.grpc_common.grpc_max_message_length,
            ),
            (
                "grpc.max_connection_idle_ms",
                config.grpc_common.grpc_max_connection_idle_ms,
            ),
            (
                "grpc.keepalive_permit_without_calls",
                config.grpc_common.grpc_keepalive_permit_without_calls,
            ),
            (
                "grpc.http2.max_pings_without_data",
                config.grpc_common.grpc_max_pings_without_data,
            ),
            (
                "grpc.http2.min_ping_interval_without_data_ms",
                config.grpc_common.grpc_min_ping_interval_without_data_ms,
            ),
        ),
    )
    subscribe_pb2_grpc.add_SubscribeServiceServicer_to_server(
        SubscribeServicer(), grpc_server
    )
    port = config.port
    if config.enable_tls:
        logger.info("Enable TLS with %s and %s", config.certfile, config.keyfile)
        try:
            private_key = open(config.keyfile, "rb").read()
            cert_chain = open(config.certfile, "rb").read()
        except:
            raise Exception("Failed to read keyfile or certfile")
        credentials = grpc.ssl_server_credentials([private_key, cert_chain])
        grpc_server.add_secure_port(f"{config.host}:{config.port}", credentials)
    else:
        logger.info("Disable TLS, using insecure mode")
        grpc_server.add_insecure_port(f"{config.host}:{config.port}")
    grpc_server.start()
    grpc_server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    server()
