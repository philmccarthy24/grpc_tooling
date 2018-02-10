using Grpc.Core;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Volcano;

namespace gRPCService2
{
    class Program
    {
        static void Main(string[] args)
        {
            int port = int.Parse(args[0]);

            Server server = new Server
            {
                Services = { WCSXform.BindService(new WCSXformImpl()) },
                Ports = { new ServerPort("localhost", port, ServerCredentials.Insecure) }
            };
            server.Start();

            Console.WriteLine("WCSXform server listening on port " + port);
            Console.WriteLine("Press any key to stop the server...");
            Console.ReadKey();

            server.ShutdownAsync().Wait();
        }
    }
}
