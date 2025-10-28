from __future__ import annotations  # Solo lo dejo por si lo necesitan. Lo pueden eliminar
from sys import argv
import json

# Librerías adicionales por si las necesitan
# No son obligatorias y tampoco tienen que usarlas todas
# No puedes agregar ningún otro import que no esté en esta lista
import re
import os
import typing
import collections
import itertools
import dataclasses
import enum

# Recuerda que no se permite importar otros módulos/librerías a excepción de los creados
# por ustedes o las ya incluidas en este main.py
from enums import TransactionState, ValidationType, ServerResponse
from simulation import Simulation

def load_jsonc(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    clean_lines = []
    for line in lines:
        # ignoramos lineas que empiezan con comentario
        if re.match(r'^\s*//', line):
            continue
        # ignoramos comentarios al final de la línea
        clean_line = re.sub(r'//.*', '', line)
        clean_lines.append(clean_line.rstrip())

    cleaned_content = "\n".join(clean_lines)
    return json.loads(cleaned_content)


if __name__ == "__main__":
    # Completar con tu implementación o crea más archivos y funciones
    test_path = argv[1]
    path = os.path.realpath(test_path)
    test_dict = load_jsonc(test_path)
    simulation = Simulation(test_dict)
    simulation.run()
    simulation.generate_output_file(path)
