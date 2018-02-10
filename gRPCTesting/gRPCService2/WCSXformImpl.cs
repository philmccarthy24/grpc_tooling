using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Volcano;
using Grpc.Core;

namespace gRPCService2
{
    public class WCSXformImpl : WCSXform.WCSXformBase
    {
        public override Task<PointResult> TransformCoord(WCS request, ServerCallContext context)
        {
            var r = new Random();
            return Task.FromResult<PointResult>(new PointResult
            {
                Ident = "Waymore corp inc",
                Tolerance = r.NextDouble(),
                MinErr = r.Next(),
                MaxErr = r.Next()
            });
        }
    }
}
