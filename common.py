import os
from google.protobuf import text_format
from proto import config_pb2

WORK_PATH = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(WORK_PATH, "conf", "server.pb.txt"), "r") as config_file:
    _server_config = text_format.Parse(
        config_file.read(), config_pb2.GrpcServerConfig()
    )
with open(os.path.join(WORK_PATH, "conf", "client.pb.txt"), "r") as config_file:
    _client_config = text_format.Parse(
        config_file.read(), config_pb2.GrpcClientConfig()
    )

SERVER_CONFIG = _server_config
CLIENT_CONFIG = _client_config
