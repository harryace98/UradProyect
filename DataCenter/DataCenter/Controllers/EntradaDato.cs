using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace DataCenter.Controllers
{
    public class EntradaDato
    {
        public int CodigoEntradaDato { get; set; }
        public string CodigoNodo { get; set; }
        public float? Velocidad { get; set; }
        public float? SNR { get; set; }
        public string HoraEntrada { get; set; }
    }
}