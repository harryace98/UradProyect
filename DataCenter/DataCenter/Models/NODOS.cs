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
    
    public partial class NODOS
    {
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Microsoft.Usage", "CA2214:DoNotCallOverridableMethodsInConstructors")]
        public NODOS()
        {
            this.CONFIGURACION_NODOS = new HashSet<CONFIGURACION_NODOS>();
            this.ENTRADADATO = new HashSet<ENTRADADATO>();
        }
    
        public string CODIGONODO { get; set; }
        public string NOMBRE_NODO { get; set; }
        public string DESCRIPCION { get; set; }
        public string IDEQUIPO { get; set; }
        public string UBICACION { get; set; }
        public Nullable<System.DateTime> TIMESPAN { get; set; }
    
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Microsoft.Usage", "CA2227:CollectionPropertiesShouldBeReadOnly")]
        public virtual ICollection<CONFIGURACION_NODOS> CONFIGURACION_NODOS { get; set; }
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Microsoft.Usage", "CA2227:CollectionPropertiesShouldBeReadOnly")]
        public virtual ICollection<ENTRADADATO> ENTRADADATO { get; set; }
    }
}