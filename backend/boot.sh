#!/bin/bash

# 1. Volver a la raíz del proyecto si es necesario o 
# usar la ruta relativa correcta al entorno virtual
# Asumiendo que 'env' está en la carpeta superior a 'backend'
source ../env/bin/activate

# 2. (Opcional) Instalar dependencias si faltan
# pip install -r requirements.txt

# 3. Ejecutar la aplicación
python3 app.py