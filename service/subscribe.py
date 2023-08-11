from cmath import inf
import collections
from email import message
import logging
from pydoc_data.topics import topics
import threading
from typing import Iterator

import grpc

from proto import (
    subscribe_pb2,
    subscribe_pb2_grpc,
)

logging.basicConfig(
    format=
    "%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
)


class SubscribeServicer(subscribe_pb2_grpc.SubscribeServiceServicer):
    def __init__(self):
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__file__)
        self.logger.setLevel(logging.INFO)
        self.subscribers = collections.defaultdict()
        self.topic_messages = collections.defaultdict()

    def Subscribe(
        self, request: subscribe_pb2.SubscribeRequest,
        context: grpc.ServicerContext
    ) -> Iterator[subscribe_pb2.SubscribeResponse]:
        self.logger.info(f"{request.id} subscribe to {request.topic}")
        if request.topic not in self.subscribers:
            self.subscribers[request.topic] = {}
        if request.id in self.subscribers[request.topic]:
            raise grpc.StatusCode.ALREADY_EXISTS
        state = threading.Condition()
        self.subscribers[request.topic][request.id] = state

        def on_rpc_done():
            self.logger.info(f"{request.id} unsubscribe from {request.topic}")
            if request.id in self.subscribers[request.topic]:
                state = self.subscribers[request.topic].pop(request.id)
                with state:
                    state.notify_all()

        context.add_callback(on_rpc_done)
        yield subscribe_pb2.SubscribeResponse(
            message=f"Welcome {request.id} to {request.topic}")

        while request.id in self.subscribers[request.topic]:
            if request.topic in self.topic_messages:
                yield subscribe_pb2.SubscribeResponse(
                    message=f"{self.topic_messages[request.topic]}")
            with state:
                state.wait()

    def Publish(
            self, request: subscribe_pb2.PublishRequest,
            context: grpc.ServicerContext) -> subscribe_pb2.PublishResponse:
        self.logger.info("Publish %s to %s", request.message, request.topic)
        if request.topic in self.subscribers:
            with self.lock:
                self.topic_messages[request.topic] = request.message
            for subscriber in self.subscribers[request.topic].values():
                with subscriber:
                    subscriber.notify_all()
        return subscribe_pb2.PublishResponse(message=f"OK")
