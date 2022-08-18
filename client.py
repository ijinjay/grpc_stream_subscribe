import time
import grpc

from common import CLIENT_CONFIG
from proto import config_pb2, subscribe_pb2, subscribe_pb2_grpc


class SubscribeCilent:
    def __init__(self, config: config_pb2.GrpcClientConfig):
        self.config = config
        if config.enable_tls:
            client_ca = config.certfile
            root_certs = open(client_ca, "rb").read()
            credentials = grpc.ssl_channel_credentials(root_certs)
            channel = grpc.secure_channel(
                f"{config.server_host}:{config.port}", credentials
            )
        else:
            channel = grpc.insecure_channel(f"{config.server_host}:{config.port}")
        self.stub = subscribe_pb2_grpc.SubscribeServiceStub(channel)

    def subscribe(self, identifier: str, topic: str) -> None:
        request = subscribe_pb2.SubscribeRequest(id=identifier, topic=topic)
        return self.stub.Subscribe(request)

    def publish(self, topic: str, message: str) -> None:
        request = subscribe_pb2.PublishRequest(topic=topic, message=message)
        return self.stub.Publish(request)


if __name__ == "__main__":
    client = SubscribeCilent(CLIENT_CONFIG)
    response = client.subscribe(f"{time.time_ns()}", "test")
    for item in response:
        print(item.message)
