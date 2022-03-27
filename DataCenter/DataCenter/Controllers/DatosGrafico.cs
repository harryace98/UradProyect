using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace DataCenter.Controllers
{
    public class DatosGrafico
    {
        public string Labels { get; set; }

        public double LinearChartData { get; set; }

        public double VelocidadNegativa { get; set; }

        public double VelocidadPositiva { get; set; }
    }
}