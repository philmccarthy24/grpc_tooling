# Experiments with gRPC Tooling

**linkerd-1.3.5** dir contains example linkerd config to perform:

- Routing of gRPC service requests
- Looking up of target service by name (as defined in .proto)
- Load-balancing of services using a round robbin strategy (optimal when it is known all service calls for a particular service will be synchronous)

**gRPCTesting** dir contains VS2015 solution with two simple C# gRPC test services (just console apps), each containing a unary RPC.

**gRPCTesting/PythonClient** contains:

- *Proto2Py.bat*, which generates Python bindings for the two C# services (Python 3.4+ is a pre-requisite, and the commands ```pip install grpcio``` and ```pip install grpcio-tools``` must be run once first to install dependent packages)
- *PythonClient.py* which shows an example Python gRPC client calling the two gRPC services through the linkerd proxy (only single ip/port required). The first set of calls also demonstrate the load balancing feature; because the first service has a blocking synchronous method, if linkerd is configured with just one service endpoint, the call takes 15 seconds. When configured with three service entries for three service instances listening on three different ports, the call takes 5 seconds.