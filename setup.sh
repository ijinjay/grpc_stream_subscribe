pip install -r requirements.txt

find proto -name "*.proto" -print | xargs python -m grpc_tools.protoc --proto_path=./ --python_out ./ --grpc_python_out=./
