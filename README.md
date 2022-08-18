# grpc_stream_subscribe
Simple pub/sub using grpc's unarystream connection.

# setup
```
bash setup.sh
```

# run

1. set python environment
```
export PYTHONPATH="./"
```

2. run server
```
python grpc_server.py
```

3. run client
```
python client.py
```

4. test case
```
pytest -s test
```

