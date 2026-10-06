#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consulta WHOIS cruda por TCP al puerto 43 del registro, sin cliente whois.

rdap.nic.ar no es autoritativo (devuelve 404 hasta para dominios registrados),
asi que la unica respuesta que vale para .ar sale del whois del NIC.

Uso: python whois-ar.py caracolasrosario.com.ar [mas dominios...]
"""
import socket
import sys

SERVIDORES = {
    ".ar": "whois.nic.ar",
    ".com": "whois.verisign-grs.com",
}
PUERTO = 43


def whois(dominio: str, host: str) -> str:
    with socket.create_connection((host, PUERTO), timeout=25) as s:
        s.sendall((dominio + "\r\n").encode())
        partes = []
        while True:
            datos = s.recv(4096)
            if not datos:
                break
            partes.append(datos)
    return b"".join(partes).decode("utf-8", "replace")


def clasificar(texto: str, dominio: str) -> str:
    t = texto.lower()
    libres = ["no se encuentra registrado", "no existe", "not found", "no data found",
              "no match", "disponible", "no registrado", "free"]
    tomado = ["registrant", "registered on", "domain name:", "fecha de alta",
              "titular", "nameserver", "ns1.", "estado:"]
    if any(p in t for p in libres):
        return "LIBRE"
    if any(p in t for p in tomado):
        return "REGISTRADO"
    return "INDETERMINADO"


if __name__ == "__main__":
    for dominio in sys.argv[1:]:
        host = next((h for suf, h in SERVIDORES.items() if dominio.endswith(suf)), None)
        if not host:
            print(f"--- {dominio}: sin servidor WHOIS conocido"); continue
        try:
            txt = whois(dominio, host)
        except Exception as e:
            print(f"--- {dominio}: ERROR {e}"); continue
        estado = clasificar(txt, dominio)
        print(f"\n=== {dominio}  ->  {estado}  (via {host}) ===")
        lineas = [l.strip() for l in txt.splitlines()
                  if l.strip() and not l.strip().startswith(("%", "#"))]
        for l in lineas[:18]:
            print("   ", l[:110])
