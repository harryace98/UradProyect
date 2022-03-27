using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Web;
using DataCenter.Models;
using System.Data.Entity;

namespace DataCenter.Controllers
{
    public class BusinessRulesUrad : IDisposable
    {
        private Urad_DBEntities1 _context;

        public void BussinessRulesUrad() { }

        public void Dispose()
        {
            this._context.Dispose();
        }

        public List<EntradaDato> ObtenerEntradaDato(string nodo)
        {
            try
            {
                if (this._context == null)
                {
                    this._context = new Urad_DBEntities1();
                }

                List<EntradaDato> query = (from ed in _context.ENTRADADATO
                                           where ed.CODIGONODO == nodo
                                           select new
                                           {
                                               CodigoEntradaDato = ed.CODIGOENTRADADATO,
                                               CodigoNodo = ed.CODIGONODO,
                                               Velocidad = ed.VELOCIDAD,
                                               SNR = ed.SNR,
                                               HoraEntrada = (DateTime)ed.HORAENTRADA
                                           }).ToList().Select(x => new EntradaDato()
                                           {
                                               CodigoEntradaDato = x.CodigoEntradaDato,
                                               CodigoNodo = x.CodigoNodo,
                                               Velocidad = x.Velocidad,
                                               SNR = x.SNR,
                                               HoraEntrada = x.HoraEntrada.ToString("yyyy-mm-dd HH:mm:ss")

                                           }).ToList();

                return query;
            }
            catch (Exception ex)
            {
                throw new Exception("Error al obtener los datos de los nodos. " + ex.Message, ex);
            }
        }

        public List<EntradaDato> ObtenerEntradaByFecha(DateTime fechaInicio, DateTime fechaFin, string nodo)
        {
            try
            {
                if (this._context == null)
                {
                    this._context = new Urad_DBEntities1();
                }
                fechaInicio = fechaInicio.ToUniversalTime();
                fechaFin = fechaFin.ToUniversalTime();
                List<EntradaDato> query = (from ed in _context.ENTRADADATO
                                           where ed.CODIGONODO == nodo &&
                                           (ed.TIMESPAN <= fechaFin && ed.TIMESPAN >= fechaInicio)
                                           select new
                                           {
                                               CodigoEntradaDato = ed.CODIGOENTRADADATO,
                                               CodigoNodo = ed.CODIGONODO,
                                               Velocidad = ed.VELOCIDAD,
                                               SNR = ed.SNR,
                                               HoraEntrada = (DateTime)ed.HORAENTRADA
                                           }).ToList().Select(x => new EntradaDato()
                                           {
                                               CodigoEntradaDato = x.CodigoEntradaDato,
                                               CodigoNodo = x.CodigoNodo,
                                               Velocidad = x.Velocidad,
                                               SNR = x.SNR,
                                               HoraEntrada = x.HoraEntrada.ToString("yyyy-MM-dd HH:mm:ss")

                                           }).ToList();
                return query;
            }
            catch (Exception ex)
            {
                throw new Exception("Error al obtener los datos de los nodos. Function ObtenerEntradaByFecha. \n" + ex.Message, ex);
            }
        }
        public List<DatosGrafico> ObtenerDatosGrafico(DateTime fechaInicio, DateTime fechaFin, string nodo)
        {
            try
            {
                fechaInicio = fechaInicio.ToUniversalTime();
                fechaFin = fechaFin.ToUniversalTime();
                if (this._context == null)
                {
                    this._context = new Urad_DBEntities1();
                }

                var query = (from ed in _context.ENTRADADATO
                                           where ed.CODIGONODO == nodo &&
                                           (ed.TIMESPAN <= fechaFin && ed.TIMESPAN >= fechaInicio)
                                           select new 
                                           {
                                               CodigoNodo = ed.CODIGONODO,
                                               Velocidad = ed.VELOCIDAD,
                                               SNR = ed.SNR,
                                               HoraEntrada = (DateTime)ed.HORAENTRADA
                                           }).ToList();

                TimeSpan interval = new TimeSpan(0, 5, 0);  // 1 minutes.

                var groupedTimes = (from cc in query
                                    group new { cc } by new
                                    {
                                        fecha = cc.HoraEntrada.Ticks / interval.Ticks,
                                    }
                                   into g
                                    select new
                                    {
                                        fechaYhora = new DateTime(g.Key.fecha * interval.Ticks),
                                        VelocidadPositiva = g.Average(x => x.cc.Velocidad.Value >= 0 ? Math.Abs(x.cc.Velocidad.Value) : 0),
                                        VelocidadNegativa = g.Average(x => x.cc.Velocidad.Value < 0 ? Math.Abs(x.cc.Velocidad.Value) : 0),
                                        VelocidadPromedioTotal = g.Average(x => Math.Abs(x.cc.Velocidad.Value))
                                    });

                List<DatosGrafico> grafico = new List<DatosGrafico>();

                foreach (var item in groupedTimes)
                {
                    BarChart barChartdata = new BarChart {  };
                    DatosGrafico tempdata = new DatosGrafico
                    {
                        VelocidadNegativa = (double)item.VelocidadNegativa,
                        VelocidadPositiva = (double)item.VelocidadPositiva,
                        Labels = item.fechaYhora.ToString("MMM dd HH:mm"),
                        LinearChartData = (double)item.VelocidadPromedioTotal
                    };

                    grafico.Add(tempdata);
                }
                
                return grafico;
            }
            catch (Exception ex)
            {
                throw new Exception("Error al obtener los datos de los nodos. Function ObtenerEntradaByFecha. \n" + ex.Message, ex);
            }
        }
        public List<DatosGrafico> ObtenerDatosGraficoTransito(DateTime fechaInicio, DateTime fechaFin, string nodo)
        {
            try
            {
                fechaInicio = fechaInicio.ToUniversalTime();
                fechaFin = fechaFin.ToUniversalTime();
                if (this._context == null)
                {
                    this._context = new Urad_DBEntities1();
                }

                var query = (from ed in _context.ENTRADADATO
                             where ed.CODIGONODO == nodo &&
                             (ed.TIMESPAN <= fechaFin && ed.TIMESPAN >= fechaInicio)
                             select new
                             {
                                 CodigoNodo = ed.CODIGONODO,
                                 Velocidad = ed.VELOCIDAD,
                                 SNR = ed.SNR,
                                 HoraEntrada = (DateTime)ed.HORAENTRADA
                             }).ToList();

                TimeSpan interval = new TimeSpan(0, 5, 0);  // 1 minutes.

                var groupedTimes = (from cc in query
                                    group new { cc } by new
                                    {
                                        fecha = cc.HoraEntrada.Ticks / interval.Ticks,
                                    }
                                   into g
                                    select new
                                    {
                                        fechaYhora = new DateTime(g.Key.fecha * interval.Ticks),
                                        VelocidadPositiva = g.Where(x => x.cc.Velocidad <= 0).Count(),
                                        VelocidadNegativa = g.Where(x => x.cc.Velocidad > 0).Count(),
                                        VelocidadPromedioTotal = g.Count()
                                    });

                List<DatosGrafico> grafico = new List<DatosGrafico>();

                foreach (var item in groupedTimes)
                {
                    BarChart barChartdata = new BarChart { };
                    DatosGrafico tempdata = new DatosGrafico
                    {
                        VelocidadNegativa = (double)item.VelocidadNegativa,
                        VelocidadPositiva = (double)item.VelocidadPositiva,
                        Labels = item.fechaYhora.ToString("MMM dd HH:mm"),
                        LinearChartData = (double)item.VelocidadPromedioTotal
                    };

                    grafico.Add(tempdata);
                }

                return grafico;
            }
            catch (Exception ex)
            {
                throw new Exception("Error al obtener los datos de los nodos. Function ObtenerEntradaByFecha. \n" + ex.Message, ex);
            }
        }
        public List<double> ObtenerIndicadoresConsolidados(string Nodo)
        {
            DateTime datenow = DateTime.UtcNow;
            //DateTime datenow = new DateTime(2022, 02, 27,18,0,0).ToUniversalTime();
            DateTime Hora = datenow.AddHours(-1);
            DateTime dia = datenow.AddDays(-1);
            DateTime semana = datenow.AddDays(-7);
            DateTime mes = datenow.AddMonths(-1);
            DateTime Limite = datenow.AddDays(-90);

            List<double> datohora = new List<double>();
            try
            {
                if (this._context == null)
                {
                    this._context = new Urad_DBEntities1();
                }

                var query = (from ed in _context.ENTRADADATO
                                           where ed.CODIGONODO == Nodo && ed.TIMESPAN >= Limite
                                           select new 
                                           {
                                               CodigoNodo = ed.CODIGONODO,
                                               Velocidad = Math.Abs(ed.VELOCIDAD == null ? 0 : (double)ed.VELOCIDAD),
                                               SNR = ed.SNR,
                                               HoraEntrada = (DateTime)ed.TIMESPAN
                                           }).ToList();
                if (query.Count > 0)
                {
                    //agregando el dato de la hora 
                    if (query.Where(x => (x.HoraEntrada <= datenow && x.HoraEntrada >= Hora)).Count() <= 0)
                        datohora.Add(0);
                    else
                        datohora.Add((double)query.Where(x => (x.HoraEntrada <= datenow && x.HoraEntrada >= Hora))
                            .Average(x => x.Velocidad));

                    //agregando el dato del dia
                    if (query.Where(x => (x.HoraEntrada <= datenow && x.HoraEntrada >= dia)).Count() <= 0)
                    datohora.Add(0);
                    else
                        datohora.Add((double)query.Where(x => (x.HoraEntrada <= datenow && x.HoraEntrada >= dia))
                        .Average(x => x.Velocidad));
                    //agregando el dato de la semana 
                    if (query.Where(x => (x.HoraEntrada <= datenow && x.HoraEntrada >= semana)).Count() <= 0)
                        datohora.Add(0);
                    else
                        datohora.Add((double)query.Where(x => (x.HoraEntrada <= datenow && x.HoraEntrada >= semana))
                        .Average(x => x.Velocidad));
                    //agregando el dato del mes  
                    if (query.Where(x => (x.HoraEntrada <= datenow && x.HoraEntrada >= mes)).Count() <= 0)
                        datohora.Add(0);
                    else
                        datohora.Add((double)query.Where(x => (x.HoraEntrada <= datenow && x.HoraEntrada >= mes))
                        .Average(x => x.Velocidad));
                }
                else
                {
                    datohora.Add(0);
                    datohora.Add(0);
                    datohora.Add(0);
                    datohora.Add(0);
                }
                return datohora;
            }
            catch (Exception ex)
            {
                throw new Exception("Error al obtener los datos de los nodos. Function ObtenerIndicadoresConsolidados. \n" + ex.Message, ex);
            }

        }

    }
}