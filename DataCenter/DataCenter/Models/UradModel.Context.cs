﻿//------------------------------------------------------------------------------
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
    using System.Data.Entity;
    using System.Data.Entity.Infrastructure;
    
    public partial class Urad_DBEntities1 : DbContext
    {
        public Urad_DBEntities1()
            : base("name=Urad_DBEntities1")
        {
        }
    
        protected override void OnModelCreating(DbModelBuilder modelBuilder)
        {
            throw new UnintentionalCodeFirstException();
        }
    
        public virtual DbSet<CONFIGURACION_NODOS> CONFIGURACION_NODOS { get; set; }
        public virtual DbSet<ENTRADADATO> ENTRADADATO { get; set; }
        public virtual DbSet<ERRORLOG> ERRORLOG { get; set; }
        public virtual DbSet<NODOS> NODOS { get; set; }
    }
}