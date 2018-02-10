using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Volcano;
using Grpc.Core;
using System.Threading;

namespace gRPCService1
{
    public class PointFinderImpl : PointFinder.PointFinderBase
    {
        private object _lock = new object();

        public override Task<Vertex> CalculatePoint(Shape request, ServerCallContext context)
        {
            var r = new Random();

            lock (_lock)
            {
                // do "work"
                Thread.Sleep(5000);
            }

            return Task.FromResult<Vertex>(new Vertex
            {
                X = r.NextDouble(),
                Y = r.NextDouble(),
                Z = r.NextDouble()
            });
        }
    }
}
