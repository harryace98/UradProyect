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
    
    public partial class CONFIGURACION_NODOS
    {
        public int ID { get; set; }
        public string CODIGONODO { get; set; }
        public int F0 { get; set; }
        public int BW { get; set; }
        public int NS { get; set; }
        public int NTAR { get; set; }
        public int MTH { get; set; }
        public int RMAX { get; set; }
        public int ALPHA { get; set; }
        public int MOVIMIENTO { get; set; }
    
        public virtual NODOS NODOS { get; set; }
    }
}