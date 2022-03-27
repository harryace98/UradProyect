using Microsoft.VisualStudio.TestTools.UnitTesting;
using DataCenter.Controllers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataCenter.Controllers.Tests
{
    [TestClass()]
    public class BusinessRulesUradTests
    {
        [TestMethod()]
        public void ObtenerEntradaByFechaTest()
        {
            BusinessRulesUrad catalogo = new BusinessRulesUrad();
            DateTime dateTime = DateTime.Now;
            List<EntradaDato> lista = catalogo.ObtenerEntradaByFecha(dateTime.AddMonths(-1), dateTime, "N000");
        }
    }
}