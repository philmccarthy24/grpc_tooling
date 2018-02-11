import subprocess as s
import random
import os
import msvcrt as m

# plan to extend this as a simple flask web app to show/manage services, size of redundant set per svc, port of linkerd,
# and anything else can think of

ephemeralPortMin = 49152
ephemeralPortMax = 65535
allocatedPortList = []

def gen_next_unique_port():
	nextPort = random.randint(ephemeralPortMin, ephemeralPortMax)
	while nextPort in allocatedPortList:
		nextPort = random.randint(ephemeralPortMin, ephemeralPortMax)
	allocatedPortList.append(nextPort)
	return nextPort

# set up some paths - could put in config
svcProcess1Path = r'C:\Workspace\grpc_tooling\gRPCTesting\gRPCService1\bin\Release\gRPCService1.exe'
svcProcess2Path = r'C:\Workspace\grpc_tooling\gRPCTesting\gRPCService2\bin\Release\gRPCService2.exe'
linkerdDiscoDir = r'C:\Program Files\linkerd-1.3.5\disco'
linkerdDir = r'C:\Program Files\linkerd-1.3.5'
linkerdApp = r'linkerd-1.3.5.jar'
linkerdConfigPath = r'config\linkerd.yaml'

# set up target services - again this stuff could reside in a config file.
# service def is a triple of (path, gRPC service name, num instances in redundant set)
# A single process could contain multiple services, however this script assumes
# it doesn't, and that the single arg is the port. guess service command line should be configurable.
# !! Basically I don't think the data model is quite correct in this script !!!
serviceDefList = []
serviceDefList.append((svcProcess1Path, 'volcano.PointFinder', 3)) 
serviceDefList.append((svcProcess2Path, 'volcano.WCSXform', 1))

# spool up process instances. this assumes the processes wait on stdin for key+enter to terminate
# their instances. possible to specify the "stop service instance" behaviour with
# a user-defined code in config?
serviceInstances = []
for svcDef in serviceDefList:
	for i in range(0, svcDef[2]):
		svcPort = gen_next_unique_port()
		svcProc = s.Popen([svcDef[0], str(svcPort)], stdin = s.PIPE, stdout = s.PIPE)
		serviceInstances.append((svcDef[1], svcPort, svcProc))
		print("Spooled up {0} on port {1}".format(svcDef[1], svcPort))

# next thing to do is update the linkerd discovery files, so incoming requests get
# routed properly. this is a bit fiddly, if data model was better, this would be easier
for svcDef in serviceDefList:
	with open(os.path.join(linkerdDiscoDir, svcDef[1]), 'w') as f:
		for svcInst in serviceInstances:
			if svcDef[1] == svcInst[0]:
				f.write("127.0.0.1 {0}\n".format(svcInst[1]))

# finally spool up linkerd
print("Starting service mesh...")
linkerd_process = s.Popen(["java.exe", "-jar", linkerdApp, linkerdConfigPath], cwd=linkerdDir)

print("Success. Press any key to shut everything down")
m.getch()
print("Shutting down...")

# send a keypress to each service process, to terminate it gracefully
for svcInst in serviceInstances:
	p = svcInst[2]
	p.stdin.write('x\r\n'.encode())
	p.stdin.close()
	p.wait()

# kill linkerd process
linkerd_process.terminate()
