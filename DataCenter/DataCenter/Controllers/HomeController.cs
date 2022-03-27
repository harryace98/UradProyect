using DataCenter.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace DataCenter.Controllers
{
    public class HomeController : Controller
    {
        private string NodoSeleccionado = "N000";
        private BusinessRulesUrad catalogo = new BusinessRulesUrad();
        public ActionResult Index(string Nodos)
        {
            NodoSeleccionado = String.IsNullOrWhiteSpace(Nodos) ? "N000" : Nodos;
            ViewBag.Nodos= Nodos;
            return View();
        }

        public ActionResult DataExport()
        {

            return View();
        }

        [HttpGet]
        public JsonResult ObtenerEntradaDatobyFecha(string fechaInicio, string FechaFin, string nodo)
        {

            Datos lista = new Datos { 
                data = catalogo.ObtenerEntradaByFecha(Convert.ToDateTime(fechaInicio), Convert.ToDateTime(FechaFin), nodo) 
            };
            return Json(lista,JsonRequestBehavior.AllowGet);
        }

        [HttpGet]
        public JsonResult ObtenerDatosConsolidadosGrafica()
        {

            //DateTime dateTime = new DateTime(2022,02,27);
            DateTime dateTime = DateTime.Now;
            var lista = catalogo.ObtenerDatosGrafico(dateTime.AddHours(-12), dateTime, NodoSeleccionado);
            return Json(lista, JsonRequestBehavior.AllowGet);
        }

        [HttpGet]
        public JsonResult ObtenerDatosTransitoConsolidados()
        {
            //DateTime dateTime = new DateTime(2022, 02, 27);
            DateTime dateTime = DateTime.Now;
            var lista = catalogo.ObtenerDatosGraficoTransito(dateTime.AddHours(-12), dateTime, NodoSeleccionado);
            return Json(lista, JsonRequestBehavior.AllowGet);
        }

        [HttpGet]
        public JsonResult ObtenerDatosVelocidad(string nodo)
        {

            var lista = catalogo.ObtenerIndicadoresConsolidados(nodo);
            return Json(lista, JsonRequestBehavior.AllowGet);
        }
        public ActionResult About()
        {
            ViewBag.Message = "Aplicacion de visualizacion de los datos capturados por los nodos Urad.";

            return View();
        }

        public ActionResult Contact()
        {
            return View();
        }
    }
}