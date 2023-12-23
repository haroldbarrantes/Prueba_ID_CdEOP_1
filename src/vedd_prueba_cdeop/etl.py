# -*- coding: utf-8 -*-

"""
-----------------------------------------------------------------------------
-----------------------------------------------------------------------------
-- Equipo Entorno de Distribución
-----------------------------------------------------------------------------
-- Fecha Creación: 20231220
-- Última Fecha Modificación: 20231220
-- Autores: haroldbarrantes
-- Últimos Autores: haroldbarrantes
-- Descripción: Script de ejecución de los ETLs
-----------------------------------------------------------------------------
-----------------------------------------------------------------------------
"""
from orquestador2.step 	    import Step
from datetime	       		import datetime
from dateutil.relativedelta import relativedelta
import json
import pkg_resources
import pandas as pd
import os


class ExtractTransformLoad(Step):
    """
    Clase encargada de la ejecución de los ETLs
    necesarios para extraer y procesar la información
    de interés de la rutina.
    """

    @staticmethod
    def obtener_ruta():
        """
        Función encargada de identificar la
        carpeta static relacionada al paquete
        ------
        Return
        ------
        ruta_src : string
        Ruta static en el sistema o entorno de
        los recursos del paquete
        """
        return pkg_resources.resource_filename(__name__, 'static')

    def obtener_params(self):
        """
        Función encargada de obtener los parámetros
        necesarios para la ejecución del paso.
        ------
        Return
        ------
        params : dictionary
        Parámetros necesarios para ejecutar el paso.
        """
        #PARAMETROS GENERALES DEL PASO
        params = self.getGlobalConfiguration()["parametros_lz"]
        now = datetime.today()
        params_default = {
            "kwargs_year"  : now.year,
            "kwargs_month" : now.month,
            "kwargs_day"   : now.day
        }
        params_default.update(self.kwa)
        now = datetime(
            params_default["kwargs_year"]
            , params_default["kwargs_month"]
            , params_default["kwargs_day"]
        )
        params_calc = {
            #FECHAS
            "f_corte_y"  : \
                str((now + relativedelta(months=-1)).year),
            "f_corte_m"  : \
                str((now + relativedelta(months=-1)).month),
            "f_corte_d"  : \
                str((now + relativedelta(months=-1)).day),
            "f_actual_y" : \
                str(now.year),
            "f_actual_m" : \
                str(now.month),
            "f_actual_d" : \
                str(now.day)
        }
        params.update(params_calc)
        params.update(self.kwa)
        params.pop("password", None)
        return params

    def ejecutar(self):
        """
        Función que ejecuta el paso de la clase.
        """
        self.log.info(json.dumps(
            self.obtener_params(), \
            indent = 4, sort_keys = True))
        self.executeTasks()

    def ejecutar_modulos(self):
        """
        Función que ejecuta los módulos de información.
        """
        self.executeFolder(self.getSQLPath() + \
            type(self).__name__, self.obtener_params())
        
class Subir_excel(Step):
    def ejecutar(self):
        # ---------------------------------------------------------------------#
        print("===== CARGANDO CONSOLIDADO - SUBIENDO DATOS A LZ =====")

        # -- Traemos los parámetros  
        global_params = self.getGlobalConfiguration()
        parametros = self.getStepConfig()
        parametros.update(global_params)
        
        sparky = self.getSparky()
        #Buscamos la ruta del archivo de Obligaciones_clientes
        Obligaciones_clientes = "{}".format(parametros["ruta_obligaciones_clientes"])
        #Creamos un DF con pandas leyendo el archivo
        df1=pd.read_excel(Obligaciones_clientes, sheet_name='Obligaciones_clientes') 
        # crear diccionario con los tipos de datos en los campos a subir a la LZ
        dtype_dict_oblig = {
            'radicado': 'int64',
            'num_documento': 'int64',
            'cod_segm_tasa': 'string',
            'cod_subsegm_tasa': 'int',
            'cal_interna_tasa': 'string',
            'id_producto': 'string',
            'tipo_id_producto': 'string',
            'valor_inicial': 'double',
            'fecha_desembolso': 'datetime64[ns]',
            'plazo': 'double',
            'cod_periodicidad': 'int64',
            'periodicidad': 'string',
            'saldo_deuda': 'double',
            'modalidad': 'string',
            'tipo_plazo': 'string'
        }

        # Cambiar los tipos de datos de los campos
        df1 = df1.astype(dtype_dict_oblig)
        te_Obligaciones_clientes = "{}.{}".format(parametros["zona_p"],parametros["Obligaciones_clientes"])
        sparky.subir_df(df1, te_Obligaciones_clientes, modo = "overwrite")

        #Buscamos la ruta del archivo de Obligaciones_clientes
        tasas_productos = "{}".format(parametros["ruta_tasas"])
        #Creamos un DF con pandas leyendo el archivo
        df2=pd.read_excel(tasas_productos, sheet_name='Tasas') 
        # crear diccionario con los tipos de datos en los campos a subir a la LZ
        dtype_dict_tasas = {
        'cod_segmento': 'string',
        'segmento': 'string',
        'cod_subsegmento': 'string',
        'calificacion_riesgos': 'string',
        'tasa_cartera': 'double',
        'tasa_operacion_especifica': 'double',
        'tasa_hipotecario': 'double',
        'tasa_leasing': 'double',
        'tasa_sufi': 'double',
        'tasa_factoring': 'double',
        'tasa_tarjeta': 'double'
        }
        # Cambiar los tipos de datos de los campos
        df2 = df2.astype(dtype_dict_tasas)
        te_tasas_productos = "{}.{}".format(parametros["zona_p"],parametros["tasas_productos"])
        sparky.subir_df(df2, te_tasas_productos, modo = "overwrite")

class GuardarCopiasExcel(Step):
    def ejecutar(self):
        # ---------------------------------------------------------------------#
        print("===== DESCARGANDO CONSOLIDADOS - BAJANDO DATOS DE LA LZ =====")
 
        # Traemos los parámetros 
        global_params = self.getGlobalConfiguration()
        parametros = self.getStepConfig()
        parametros.update(global_params)

        #Traer el df consolidado 
        resultado1_lz = """select * from """ "{}.{}".format(parametros["zona_p"],parametros["tabla_result1"]) 
        resultado2_lz = """select * from """ "{}.{}".format(parametros["zona_p"],parametros["tabla_result2"]) 
        
        #imprimir el df en excel del consolidado colas en la ruta con el mismo nombre 
        #para actualizar el control de datos
        helper = self.getHelper()
        #Guardar nuevo historico en local del KPI Colas General 
        archivo_resultado1_lz = helper.obtener_dataframe(resultado1_lz)
        archivo_resultado1_lz.to_excel("{}".format(parametros["archivo_resultado1_lz"]), index=0)
        #Guardar nuevo historico en local del KPI rangos 
        archivo_resultado2_lz = helper.obtener_dataframe(resultado2_lz)
        archivo_resultado2_lz.to_excel("{}".format(parametros["archivo_resultado2_lz"]), index=0)


