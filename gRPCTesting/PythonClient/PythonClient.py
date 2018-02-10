import gRPCService1_pb2
import gRPCService1_pb2_grpc
import gRPCService2_pb2
import gRPCService2_pb2_grpc
import grpc

# note the use of a single channel and ip/port for ALL gRPC services! This is the
# ip/port of the linkerd http/2 proxy router
channel = grpc.insecure_channel('localhost:4141')

# create the service stubs
PointFinderService = gRPCService1_pb2_grpc.PointFinderStub(channel)
WCSXformService = gRPCService2_pb2_grpc.WCSXformStub(channel)

# call 3 rpcs in parallel, on the first service
result_futures = []
for i in range(0,3):
	result_future = PointFinderService.CalculatePoint.future(gRPCService1_pb2.Shape(identifier="hello"))
	result_futures.append(result_future)

for result_future in result_futures:
	print(result_future.result())

# call an rpc on the second service
point = WCSXformService.TransformCoord(gRPCService2_pb2.WCS(name="boo"))
print(point)

