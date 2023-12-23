from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load data from file
df_table_1 = pd.read_excel('C:/Users/hbarrant/Documents/hbarrant - p/Prueba tecnica CdEOps/prueba_ID_CdEOP/vedd-prueba-cdeop/output/Resultado_1.xlsx')
df_table_2 = pd.read_excel('C:/Users/hbarrant/Documents/hbarrant - p/Prueba tecnica CdEOps/prueba_ID_CdEOP/vedd-prueba-cdeop/output/Resultado_2.xlsx')

# Endpoint: Exercise 1
@app.route('/exercise1/<int:num_documento>')
def exercise1(num_documento):
    # Filter data for the given num_documento
    data_1 = df_table_1[df_table_1['num_documento'] == num_documento][['id_producto', 'valor_inicial', 'fecha_desembolso', 'plazo', 'cod_periodicidad', 'periodicidad', 'tasa', 'te', 'valor_final']]
    # Convert data to JSON and return
    return jsonify(data_1.to_dict(orient='records'))

# Endpoint: Exercise 2
@app.route('/exercise2/<int:num_documento>')
def exercise2(num_documento):
    # Filter data for the given num_documento
    data_2 = df_table_2[df_table_2['num_documento'] == num_documento][['valor_total']]
    # Convert data to JSON and return
    return jsonify(data_2.to_dict(orient='records'))

# Ruta para la página de inicio
@app.route('/')
def index():
    return "¡Bienvenido al API del Centro de Excelencia de Operación!"

if __name__ == '__main__':
    app.run()
