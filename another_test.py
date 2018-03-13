from AppData.Scripts.funciones import base_datos as bd

base = bd()
datos=base.cargar_datos()
base.conversion_excel()
