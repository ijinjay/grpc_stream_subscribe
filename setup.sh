#!/bin/bash

WORK_DIR=$(cd "$(dirname "$0")" && pwd)
echo "work dir: $WORK_DIR"

cd "$WORK_DIR"  || exit
pip install -r requirements.txt
find proto -name "*.proto" -print0 | xargs -0 python -m grpc_tools.protoc --proto_path=./ --python_out ./ --grpc_python_out=./
