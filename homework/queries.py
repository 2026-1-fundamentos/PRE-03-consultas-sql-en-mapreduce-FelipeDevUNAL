"""Ejercicio evaluativo"""

# pylint: disable=broad-exception-raised
# pylint: disable=import-error


def ejecutar():
    """
    Punto de entrada principal.

    Procesa el archivo `files/input/tips.csv` y genera 5 salidas en:

    - files/query_1/
    - files/query_2/
    - files/query_3/
    - files/query_4/
    - files/query_5/

    Cada carpeta contiene:
    - _SUCCESS
    - part-00000
    """

    import csv
    import os
    from collections import defaultdict
    from typing import Iterable, Callable, Iterator

    ruta_entrada = os.path.join("files", "input", "tips.csv")

    if not os.path.isfile(ruta_entrada):
        raise Exception(f"No existe el archivo de entrada: {ruta_entrada}")

    with open(ruta_entrada, encoding="utf-8") as f:
        lector = csv.DictReader(f)
        registros = list(lector)

    # Conversión de tipos
    for fila in registros:
        fila["total_bill"] = float(fila["total_bill"])
        fila["tip"] = float(fila["tip"])
        fila["size"] = int(float(fila["size"]))

    def motor_analitico(
        dataset: Iterable[dict],
        transformador: Callable[[dict], Iterator[tuple]],
        agregador: Callable[[object, list], tuple | None],
    ) -> list[tuple]:
        """Simulación de MapReduce en memoria."""

        acumulador = defaultdict(list)

        for elemento in dataset:
            for clave, valor in transformador(elemento):
                acumulador[clave].append(valor)

        salida = []
        for clave in sorted(acumulador, key=lambda x: str(x)):
            resultado = agregador(clave, acumulador[clave])
            if resultado:
                salida.append(resultado)

        return salida

    def guardar_salida(indice: int, contenido: list[str]) -> None:
        carpeta = os.path.join("files", f"query_{indice}")
        os.makedirs(carpeta, exist_ok=True)

        with open(os.path.join(carpeta, "_SUCCESS"), "w"):
            pass

        with open(os.path.join(carpeta, "part-00000"), "w") as archivo:
            archivo.write("\n".join(contenido))
            if contenido:
                archivo.write("\n")

    # --- Consulta 1 ---
    def t1(fila):
        yield fila["day"], 1

    def a1(clave, valores):
        return clave, sum(valores)

    res1 = motor_analitico(registros, t1, a1)
    lineas1 = [f"{d}\t{c}" for d, c in res1]
    guardar_salida(1, lineas1)

    # --- Consulta 2 ---
    def t2(fila):
        yield fila["sex"], (fila["tip"], 1)

    def a2(clave, valores):
        total = sum(v[0] for v in valores)
        cantidad = sum(v[1] for v in valores)
        return clave, total / cantidad

    res2 = motor_analitico(registros, t2, a2)
    lineas2 = [f"{k}\t{v:.6f}" for k, v in res2]
    guardar_salida(2, lineas2)

    # --- Consulta 3 ---
    def t3(fila):
        yield fila["smoker"], fila["tip"]

    def a3(clave, valores):
        return clave, sum(valores)

    res3 = motor_analitico(registros, t3, a3)
    lineas3 = [f"{k}\t{v:.6f}" for k, v in res3]
    guardar_salida(3, lineas3)

    # --- Consulta 4 ---
    def t4(fila):
        yield (fila["day"], fila["time"]), (fila["total_bill"], 1)

    def a4(clave, valores):
        total = sum(v[0] for v in valores)
        cantidad = sum(v[1] for v in valores)
        return clave, total / cantidad

    res4 = motor_analitico(registros, t4, a4)
    lineas4 = [f"{d}\t{t}\t{v:.6f}" for (d, t), v in res4]
    guardar_salida(4, lineas4)

    # --- Consulta 5 ---
    def t5(fila):
        yield fila["size"], fila["tip"]

    def a5(clave, valores):
        return clave, max(valores)

    res5 = motor_analitico(registros, t5, a5)
    lineas5 = [f"{k}\t{v:.6f}" for k, v in res5]
    guardar_salida(5, lineas5)


if __name__ == "__main__":
    ejecutar()