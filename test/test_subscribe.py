import pytest
import grpc

from common import CLIENT_CONFIG
from proto import subscribe_pb2, subscribe_pb2_grpc


class TestSubscribe:
    @pytest.fixture(scope="class")
    def grpc_stub(self):
        if CLIENT_CONFIG.enable_tls:
            client_ca = CLIENT_CONFIG.certfile
            root_certs = open(client_ca, "rb").read()
            credentials = grpc.ssl_channel_credentials(root_certs)
            channel = grpc.secure_channel(
                f"{CLIENT_CONFIG.server_host}:{CLIENT_CONFIG.port}", credentials
            )
        else:
            channel = grpc.insecure_channel(
                f"{CLIENT_CONFIG.server_host}:{CLIENT_CONFIG.port}"
            )
        stub = subscribe_pb2_grpc.SubscribeServiceStub(channel)
        return stub

    def test_subscribe(self, grpc_stub):
        request = subscribe_pb2.SubscribeRequest(id="1", topic="test")
        response = grpc_stub.Subscribe(request)
        assert next(response)

        pub_request = subscribe_pb2.PublishRequest(topic="test", message="hello")
        pub_response = grpc_stub.Publish(pub_request)
        assert pub_response.message == "OK"
        assert next(response).message == "hello"
