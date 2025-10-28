# T3-Sistemas-Distribuidos

## Integrantes:
nombre - numero_alumno
- Rodrigo Figueroa - 21640378
- Martín Sánchez - 20624654

## Citas:
### IA generativa
**main.py**: En la función `load_jsonc(path)` se utilizó IA generativa para los patrones de regex. Acá el [link al chat](https://chatgpt.com/share/68ffeec3-93f4-8009-87de-7fc8db3733b6).

### Asistentes de programación:
Se utilizó Copilot a través del editor de texto VScode. Copilot tuvo la única funcionalidad
de completar código a medida que escribíamos. No fue prompteado para resolver la tarea. 
En particular, autocompletaba cuando se estaban escribiendo partes repetitivas en el código, ejemplo:

for key in transaction.write_set.keys():
for server in self.servers.values():

En casos como este, donde se volvía a iterar sobre los mismos elementos, naturalmente Copilot ayudaba a completar. Sin embargo el uso de este no fue muy extenso, ya que suele hacer supuestos que no son correctos para los protocolos.