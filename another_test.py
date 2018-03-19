from AppData.Scripts.funciones import base_datos as bd

base = bd()
datos=base.cargar_datos()
consulta = base.get_valores_pozo("Allegheny")
print(consulta[0,:])
