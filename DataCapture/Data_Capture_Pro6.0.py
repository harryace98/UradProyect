#region Imporacion de las Librerias necesarias
import uRAD_RP_SDK11		# import uRAD library
import MySQLdb
import json
import os
import sys
from pathlib import Path
import time
from datetime import datetime
#endregion

#region Declaracion de Variables globales, Clases, objetos y excepciones globales

# Excepciones para el control de errores 
class AccesoException(Exception):		    #Excepcion de errores de conexion con la base de datos
    pass
class ConfiguracionException(Exception):	# Excepcion para errores relacionados con la configuracion (obteccion de datos,seteos,etc)
    pass
class ConexionUradException(Exception):     # Excepcion para error en la conexion del uRAD
    pass
class uRADException(Exception):             # Excepciones generales del uRAD
    pass

# Obejeto en el cual almacenamos los parametros de configuracion del Urad 
class ConfiguracionUrad:
    def __init__(self, mode, f0, BW, Ns, Ntar, Rmax, MTI, Mth, Alpha, distance_true, velocity_true, SNR_true, I_true, Q_true, movement_true):
        self._mode= mode
        self._f0 = f0
        self._BW = BW
        self._Ns = Ns
        self._Ntar = Ntar
        self._Rmax = Rmax
        self._MTI = MTI
        self._Mth = Mth
        self._Alpha = Alpha
        self._distance_true = distance_true
        self._velocity_true = velocity_true
        self._SNR_true = SNR_true
        self._I_true = I_true
        self._Q_true = Q_true
        self._movement_true = movement_true

    # getters para obtenerlos parametros de configuracion del Urad
    @property
    def mode(self):
        return self._mode
    @property
    def f0(self):
        return self._f0
    @property
    def BW(self):
        return self._BW
    @property
    def Ns(self):
        return self._Ns
    @property
    def Ntar(self):
        return self._Ntar
    @property
    def Rmax(self):
        return self._Rmax
    @property
    def MTI(self):
        return self._MTI
    @property
    def Mth(self):
        return self._Mth
    @property
    def Alpha(self):
        return self._Alpha
    @property
    def distance_true(self):
        return self._distance_true
    @property
    def velocity_true(self):
        return self._velocity_true
    @property
    def SNR_true(self):
        return self._SNR_true
    @property
    def I_true(self):
        return self._I_true
    @property
    def Q_true(self):
        return self._Q_true
    @property
    def movement_true(self):
        return self._movement_true

## objeto donde se almacena las credenciales de acceso a la base de datos         
class ConfiguracionAcessoDB:
    def __init__(self,host,user,passwd,Database,Idnodo):
        self._host = host
        self._user = user
        self._passwd = passwd
        self._Database = Database
        self._Idnodo = Idnodo
	
	#getter del campo host de la db
    @property
    def host(self):
        return self._host
	
	#getter del campo usuario de acceso a la db
    @property
    def user(self):
        return self._user
	
	#getter del campo de la contrasena para el acesso al db
    @property
    def passwd(self):
        return self._passwd
	
	#getter del campo del nombre de la base de datos
    @property
    def Database(self):
        return self._Database
	
	#getter del campo id del nodo
    @property
    def Idnodo(self):
        return self._Idnodo

# Objeto que nos permite realizar las funciones de conexion y consulta a la base de datos
class AccesoDB:
    def __init__(self, host,user,passwd,Database):
        self.__host = host
        self.__user = user
        self.__passwd = passwd
        self.__Database = Database

	## metodo para verificar la conexion con la base de datos.
    def VerificarConexion(self):
        try:
            db = MySQLdb.connect(host=self.__host,user=self.__user,password=self.__passwd,db=self.__Database)
            return True
        except MySQLdb._exceptions.DatabaseError as e:
            raise AccesoException("Error de la base de datos Mysql. ", e) from e 
        except Exception as e:
            raise AccesoException("Error en la conexion con la base de datos. ", e) from e
        except BaseException as e:
            raise Exception("Error al intentar realizar la conexion. ", e) from e 

	## Metodo que nos permite realizar todos los querys de consulta a la base de datos
    def EjecutarQueryConsulta(self, sqlQuery):
        dataList = []
        try:
            db = MySQLdb.connect(host=self.__host,user=self.__user,password=self.__passwd,db=self.__Database)
            cursor = db.cursor()
            cursor.execute(sqlQuery)
            records = cursor.fetchall()
            for row in records:
                dataList.append(row)
            db.close()
            return dataList
        except MySQLdb._exceptions.DatabaseError as e:
            raise AccesoException("Error de la base de datos Mysql. ", e) from e
        except Exception as e:
            raise AccesoException("Error en la conexion con la base de datos. ", e) from e
        except BaseException as e:
            raise Exception("Error al intentar realizar la conexion. ", e) from e

	## Metodo que nos permite realizar consultas a la base de datos y obtener un Json de respuesta
    def EjecutarConsultaToJson(self,sqlQuery,args):
        
        try:
            db = MySQLdb.connect(host=self.__host,user=self.__user,password=self.__passwd,db=self.__Database)
            cursor = db.cursor()
            cursor.execute(sqlQuery, args)
            row_headers=[x[0] for x in cursor.description] #Extraemos el encabezado de la consulta
            dataResult = cursor.fetchall()
            json_data=[]
            for result in dataResult:
                json_data.append(dict(zip(row_headers,result)))
            return json.dumps(json_data)
        except MySQLdb._exceptions.DatabaseError as e:
            raise AccesoException("Error de la base de datos Mysql. ", e) from e
        except Exception as e:
            raise AccesoException("Error en la conexion con la base de datos. ", e) from e
        except BaseException as e:
            raise Exception("Error al intentar realizar la conexion. ", e) from e

	## metodo que nos permite ejecutar los querys de Insert en la base de datos 
    ## La variable de entrada Valores debe ser una lista 
    def EjecutarQueryInsercion(self, sqlQuery, Valores):
        try:
            db = MySQLdb.connect(host=self.__host,user=self.__user,password=self.__passwd,db=self.__Database)
            cursor = db.cursor()
            cursor.executemany(sqlQuery, Valores)
            db.commit()
        except MySQLdb._exceptions.DatabaseError as e:
            raise AccesoException("Error de la base de datos Mysql. " , e) from e
        except Exception as e:
            raise AccesoException("Error en la conexion con la base de datos. ", e) from e
        except BaseException as e:
            raise Exception("Error al intentar realizar la conexion. ", e) from e
        finally:
            db.close()

## Clase que nos permite almacenar los errores en un fichero y en la base de datos
class Errorlog:
    def __init__(self,conexionDB):
        self._conexionDB = conexionDB
        
    def GuardarErrorDB(self,MensajeError):
        try:
            idequipo = ObtenerIdEquipo(self._conexionDB)
            sqlQuery = "INSERT INTO ERRORLOG(IDEQUIPO,CODIGOERROR,MENSAJE_ERROR,DATOS_ERROR) VALUES(%i,%s,%s,%s)"
            args = (idequipo,"00",MensajeError,"no data")
            self._conexionDB.EjecutarQueryInsercion(sqlQuery,args)
        except AccesoException as e:
            raise AccesoException("Error al intentar insertar la entrada dato. ", e) from e
        except BaseException as e:
            raise Exception("Error no controlado al intentar ingresar la entrada dato. ", e) from e

    def GuardarErrorArchivo(self,MensajeError):
        try:
            DirectorioActual = "/home/pi/UradCapture/ErrorRegister.log"
            fileObj = Path(DirectorioActual)
            if fileObj.exists():
                ArchivoError = open(DirectorioActual, "a")
                ArchivoError.write(MensajeError + "\n")
                ArchivoError.close()
            else:
                ArchivoError = open(DirectorioActual, "w")
                ArchivoError.write(MensajeError + "\n")
                ArchivoError.close()
        except OSError as e:
            raise Exception("Error del sistema de archivos. ", e)
        except BaseException as e:
            raise Exception("Error no controlado al intentar guardar los logs. ", e)
	
###########################################################

#Declaracion de Metodos y Funciones

# Metodo para cerrar el programa (Opcional por ahora)
def DetenerUrad():
    try:
        return_code = uRAD_RP_SDK11.turnOFF()
        
    except:
        print("Error. ")
        time.sleep(10)

## metodo que nos permite leer el archivo de configuracion y obtener las credenciales de acceso a la base de datos
# y establecer el Codigo del nodo que se ha asignado a la base de datos  
def CargarConfiguracionArchivo():
    try:
        DireccionArchivoConfig = "/home/pi/UradCapture/configuracionInicial.conf"
        dataConfig = open(DireccionArchivoConfig, "r")
        serializedConfig = json.loads(dataConfig.read())
        connectionconfig = ConfiguracionAcessoDB(serializedConfig["host"],serializedConfig["user"],serializedConfig["password"],serializedConfig["db"],serializedConfig["IdNodo"])
        dataConfig.close()
        return connectionconfig
    except FileNotFoundError as e:
        raise ConfiguracionException("Error. No se encontro el archivo en la ruta especificada. revisar el nombre y la ruta del archivo. ", e) from e
    except PermissionError as e:
        raise ConfiguracionException("Error. No se cuentan con los permisos de lectura en el archivo de configuracion .config . ", e) from e
    except BaseException as e:
        raise ConfiguracionException("Error no controlado al intentar obtener la configuracion de acceso a la base de datos ",  e) from e

# Metodo que inicia el uRAD    
def IniciarUrad():
    try:
        return_message = uRAD_RP_SDK11.turnON()
        if (return_message == -1):
            raise ConexionUradException("Error en la conexion con el uRAD. ")
        elif (return_message == -2):
            raise ConexionUradException("Error no controlado al inciar el uRAD. Error proveniente de la libreria")
    except ConexionUradException as e:
            raise ConexionUradException("Se ha presentado un error con el uRAD", e) from e
    except Exception as e:
            raise uRADException("Error. ", e) from e    
    except BaseException as e:
        raise uRADException("Error general no controlado al iniciar el uRAD. ", e) from e 
         
## Metodo que nos permite obtener los parametros de configuracion para el Urad
def ObtenerParametrosConfigUrad(ConexionDB,Idnodo):
    try:
        sqlQuery="SELECT ID, CODIGONODO, F0, BW, NS, NTAR, MTH, RMAX, ALPHA, MOVIMIENTO FROM CONFIGURACION_NODOS WHERE CODIGONODO = %s"
        args=(Idnodo,)
        JsonResult =json.loads(ConexionDB.EjecutarConsultaToJson(sqlQuery,args))
        ConfigData = ConfiguracionUrad(3,JsonResult[0]["F0"],JsonResult[0]["BW"],JsonResult[0]["NS"],JsonResult[0]["NTAR"],JsonResult[0]["RMAX"],1,JsonResult[0]["MTH"],JsonResult[0]["ALPHA"],True,True,True,False,False,JsonResult[0]["MOVIMIENTO"])
        CodResultado = uRAD_RP_SDK11.loadConfiguration(ConfigData.mode, ConfigData.f0, ConfigData.BW, ConfigData.Ns, ConfigData.Ntar, ConfigData.Rmax, ConfigData.MTI, ConfigData.Mth, ConfigData.Alpha, ConfigData.distance_true, ConfigData.velocity_true, ConfigData.SNR_true, ConfigData.I_true, ConfigData.Q_true, ConfigData.movement_true)
        if (CodResultado == -1):
            raise ConexionUradException("Error en la conexion con el uRAD. ")
        elif (CodResultado == -2):
            raise ConexionUradException("Error no controlado al cargar los datos al uRAD. ")
        return ConfigData

    except MySQLdb._exceptions.DatabaseError as e:
            raise AccesoException("Error del Mysql connect. ", e) from e
    except ConexionUradException as e:
            raise ConexionUradException("Se ha presentado un error con el uRAD", e) from e
    except Exception as e:
            raise ConfiguracionException("Error. ", e) from e    
    except BaseException as e:
        raise ConfiguracionException("Error no controlado al realizar obtencion de los parametros de configuracion del uRAD. ", e) from e 
    
## Metodo que nos permite obtener el idequipo de la base de datos
def ObtenerIdEquipo(ConexionDB,Idnodo):
    try:
        sqlQuery="SELECT IDEQUIPO FROM NODOS WHERE CODIGONODO= %s"
        args=(Idnodo,)
        idEquipo=ConexionDB.EjecutarConsultaToJson(sqlQuery,args)
        return idEquipo
    except MySQLdb._exceptions.DatabaseError as e:
            raise AccesoException("Error del Mysql connect. ", e) from e
    except ConexionUradException as e:
            raise ConexionUradException("Se ha presentado un error con el uRAD", e) from e
    except Exception as e:
            raise ConfiguracionException("Error. ", e) from e    
    except BaseException as e:
        raise ConfiguracionException("Error no controlado al realizar obtencion de los parametros de configuracion del uRAD. ", e) from e 
    
# Metodo para guardar los datos capturados en la base de datos    
def InsertarEntradaDatosDB(ConexionDB,Valores):
    try:
        sqlQuery = "INSERT INTO ENTRADADATO(CODIGONODO,VELOCIDAD,SNR,HORAENTRADA,TIMESPAN) VALUES(%s,%s,%s,%s,now())"
        ConexionDB.EjecutarQueryInsercion(sqlQuery,Valores)
        return "Correcto"
    except AccesoException as e:
        raise AccesoException("Error al intentar insertar la entrada dato. ", e) from e
    except BaseException as e:
        raise Exception("Error no controlado al intentar ingresar la entrada dato. ", e) from e
#endregion

#region METODO MAIN 
Horaincio = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
print("se ha iniciado el programa de captura. " + Horaincio)
time.sleep(0.5)
while True:
    try:
        # obtenemos las credenciales de conexion con la base de datos
        CredencialesConexion = CargarConfiguracionArchivo()
        print("Se ha ralizado la carga de la configuracion de manera correcta")
        # flag que nos indica si hay conexion con la base de datos 
        ConexionDBCorrecta = False
        # flag que indica si hay error en el uRAD
        errorUrad = False
        conexionDB = AccesoDB(CredencialesConexion.host,CredencialesConexion.user,CredencialesConexion.passwd,CredencialesConexion.Database)
        # Instanciamos el objeto Errorlog para almacenar los errores
        errorLog = Errorlog(conexionDB)
        print("se verifica la conexion con la base de datos")
        while ConexionDBCorrecta==False: 
            try:
                ConexionDBCorrecta = conexionDB.VerificarConexion()
                #print(ConexionDBCorrecta)
            except AccesoException as e:
                HoraError = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                msgError= "[" + HoraError + "] - Falla en la verificacion. no se pudo realizar la conexion con la base de datos. " + str(e)
                errorLog.GuardarErrorArchivo(msgError)
            except Exception as e:
                HoraError = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                msgError= "[" + HoraError + "] - Falla en la verificacion. no se pudo realizar la conexion con la base de datos. " + str(e)
                errorLog.GuardarErrorArchivo(msgError)
            except BaseException as e:
                HoraError = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                msgError= "[" + HoraError + "] - Falla en la verificacion. Error no controlado. " + str(e)
                errorLog.GuardarErrorArchivo(msgError)
            finally:
                time.sleep(10)
        print("Inicamos urad y carga parametros de configuracion")
        # iniciamos el uRAD
        IniciarUrad()
        # Cargamos los parametros de configuracion del uRAD            
        ObtenerParametrosConfigUrad(conexionDB,CredencialesConexion.Idnodo)
        time.sleep(2)
        print("Iniciamos captura de datos")
        while errorUrad==False:
            try:
                time.sleep(0.5)
                Valores = []
                HoraEntradaDato = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                return_message, resultados, raw_results = uRAD_RP_SDK11.detection()
                if (return_message == -1):
                    raise ConexionUradException("Error en la conexion con el uRAD. ")
                elif (return_message == -2):
                    raise ConexionUradException("Error no controlado al inciar el uRAD. Error proveniente de la libreria")
                if(resultados == 0):
                    continue

                Targets = resultados[0]
                Distance = resultados[1]
                Velocity = resultados[2]
                SNR = resultados[3]
                for i in range(Targets):

                    if (SNR[i] > 0 and Velocity[i] != 0):
                        # Imprime la informacion 
                        Valores.append((CredencialesConexion.Idnodo,str(Velocity[i] * 3.6),str(SNR[i]),HoraEntradaDato))
                # Insertamos los datos en la base de datos
                
                InsertarEntradaDatosDB(conexionDB,Valores)
                #print("Captura de datos correcta")
            except AccesoException as e:
                HoraError = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                msgError= "[" + HoraError + "] - Error de conexion con la base de datos.  " + str(e)
                errorLog.GuardarErrorArchivo(msgError)
                errorUrad=True
            except ConexionUradException as e:
                HoraError = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                msgError= "[" + HoraError + "] - Error de conexion con el Urad. " + str(e)
                errorLog.GuardarErrorArchivo(msgError)
                errorLog.GuardarErrorDB(msgError)
                errorUrad=True
            except uRADException as e:
                HoraError = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                msgError= "[" + HoraError + "] - Error del Urad. " + str(e)
                errorLog.GuardarErrorArchivo(msgError)
                errorLog.GuardarErrorDB(msgError)
                errorUrad=True
            except BaseException as e:
                HoraError = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                msgError= "[" + HoraError + "] - Error no controlado. " + str(e)
                errorLog.GuardarErrorArchivo(msgError)  
                errorUrad=True
    except AccesoException as e:
        HoraError = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print("[" + HoraError + "] - Error de conexion con la base de datos.  " + str(e))
    except ConfiguracionException as e:
        HoraError = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print("[" + HoraError + "] - Error de conexion con la base de datos.  " + str(e))
    except ConexionUradException as e:
        HoraError = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print("[" + HoraError + "] - Error de conexion con el Urad. " + str(e))
    except uRADException as e:
        HoraError = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print("[" + HoraError + "] - Error del Urad. " + str(e))
    except KeyboardInterrupt as e:
        HoraError = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print("[" + HoraError + "] - Se ha interrumpido el programa de captura de manera inesperada. " + str(e))
        DetenerUrad()
        sys.exit("Programa Finalizado")
    except BaseException as e: # donde se manejan todas las excepciones del codigo
        HoraError = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print("[" + HoraError + "] - Error del Urad. " + str(e))
    finally:
        DetenerUrad()
        sys.exit("Programa Finalizado")       
#endregion