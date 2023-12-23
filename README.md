En el Readme encontramos la manera de ejecutar los instaladores y la ejecución  del proyecto

# Recursos vitales

-El python usado en el entorno virtual es >=3.5.4, <=3.9.7
-Se requiere configuaración de ODBC de 64 bits con credenciales LZ 
-Se requiere Driver Cacerts almacenado en c 
-Archivo .PIP almacenado en el usuario de la maquina
-Se debe tener habilitado para el usuario ejecutor External Table
-En el archivo Config.json se deben cambiar las rutas de las clases subir y bajar Excel para que recoja y almacene los resultados
- Si la ejecución es desde casa, se debe activar citrix.

El proyecto con Python recoge los archivos excel y los lleva de Data Frames en python a la zona de procesos de la LZ con Spark, en la ejecución pedira la contraseña del usuario analítico para comprobar la conexión ODBC

# Instalación y ejecución del pryecto

1. Realizar la instalación del ambiente virtual dentro de la carpeta del Orquestador escribiendo en la consola: 
    >> "python -m venv .venv"

(Es posible que Visual Studio solicite emplear ese entorno por defecto, le podemos decir que Si, de esta manera cuando se vuelva a abrir el Visual Studio este abrirá por defecto).

2. Activar el ambiente virtual ubicandose en la nueva carpeta **.venv/Scripts** y escribiendo en la consola **activate**, para acceder a la carpeta podemos acceder con los siguientes comandos:
    >> "cd .venv" > "cd Scripts" > "activate" > cd.. > cd.. > cls
    ó más rápido
    >> ".venv\Scripts\activate"

3. Actualizar el Bibliotecario (Importante para mitigar conflictos de librerías):

    >> "python -m pip install --upgrade pip"

    Si se desea verificar antes la versión se puede ejecutar el comando:

    >> "pip list"

    Nota: Es importante que la actualización se haga desde el artifactory, para ello lo más práctico es tener un archivo llamado pip.ini dentro de una carpeta llamada pip en la carpeta del usuario del computador. El archivo pip.ini debe contener lo siguiente:

    [global]
    index-url=https://artifactory.apps.bancolombia.com/api/pypi/pypi-bancolombia/simple
    trusted-host=artifactory.apps.bancolombia.com
    user=false

4. Instalar los paquetes que requiere el orquetador escribiendo en la consola: 
    >> "pip install -e." (Más rápido) o 
    >> "pip install --no-cache-dir -e." (En caso que no funcione la anterior probar con esta)

5. Escribir el DSN y usuario en el archivo config.json, ubicado en la carpeta: 
    src > static > config.json.

10. Para ejecutar el orquestador hay que ubicarse en la carpeta donde está el archivo **ejecucion.py** y ejecutar en la consola el siguiente comando:
    
    >> python ejecucion.py

Y listo hora de ejecutar el Orquestador!!!

# PLUS ->> 
1. (Ingreso automático de la contraseña): Si se va a ejecutar muchas vecees en el día el orquestador, es posible que se desee que la contraseña sea ingresada de manera automática esta puede colocarse en las variables de entorno de la cuenta y ser llamada mediante el código <<os.getenv("pass")>>, donde **pass** es el nombre asignado a la variable de entorno de la cuenta al que su valor hay que escribir la contraseña, el código se debe colocar donde es solicitada la contraseña en la librería del orquestador (orquestador2 > orquestador.py > "password" > None > os.getenv("pass")). Para que funcione la primera vez que se instancia la variable de entorno hay que reiniciar todo el Visual Studio Code. <Claramente este paso implica un punto de seguiridad a tener en cuenta, y debería ser empleado con toda la cautela posible y eliminar la contraseña de las variables de entorno si esta no se va a emplear para evitar cualquier riesgo de seguridad de la información.>

2. Ejecución automática del orquestador a partir de un archivo Bat: Es posible ejecutar el orquestador a partir de un archivo .bat, en el cual hay que escribir lo siguiente:

    >> call .venv/Scripts/activate
    >> python script_ejecucion.py

3. # API
        Ejecutar en la terminal
         
         >> python API.py 
         
         Verenmos en la terminal el Endpoint,  se debe abrir en el el navegador de preferencia y adicionar “/exercise1/<num_documento>” o “/exercise2/<num_documento>”, según si se desea observar todos los productos por cliente, o únicamente el valor agregado por cliente respectivamente. 
         Ej:
          http://127.0.0.1:5000/exercise1/1081648945 
          http://127.0.0.1:5000/exercise2/1081648945