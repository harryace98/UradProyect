//------------------------------------------------------------------------------
// <auto-generated>
//     Este código se generó a partir de una plantilla.
//
//     Los cambios manuales en este archivo pueden causar un comportamiento inesperado de la aplicación.
//     Los cambios manuales en este archivo se sobrescribirán si se regenera el código.
// </auto-generated>
//------------------------------------------------------------------------------

namespace DataCenter.Models
{
    using System;
    using System.Collections.Generic;
    
    public partial class ERRORLOG
    {
        public int ID { get; set; }
        public int IDEQUIPO { get; set; }
        public string CODIGOERROR { get; set; }
        public string MENSAJE_ERROR { get; set; }
        public string DATOS_ERROR { get; set; }
        public Nullable<System.DateTime> TIMESPAN { get; set; }
    }
}
