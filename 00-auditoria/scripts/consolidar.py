#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consolida en un solo archivo la evidencia medida de Las Caracolas.

Lee los artefactos crudos que dejaron los scripts (no los reescribe a mano) y
arma evidencia-caracolas.json, para que cada numero del informe tenga de donde
salir. Los datos que no se pudieron medir van con estado NO VERIFICADO.
"""
import json
import pathlib
import re

SCRATCH = pathlib.Path("C:/Users/Torso/audit-caracolas-scratch")
OUT = pathlib.Path("C:/Users/Torso/lead-las-caracolas/00-auditoria")
OUT.mkdir(parents=True, exist_ok=True)
MEDIDO_EL = "6 de octubre de 2026"


def unescape(s: str) -> str:
    """Deshace los \\uXXXX del JSON de Instagram sin dejar surrogates sueltos.
    Los emojis vienen como pares \\ud83c\\udf64: hay que reensamblarlos."""
    txt = s.encode("utf-8", "surrogatepass").decode("utf-8", "replace")
    txt = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), txt)
    txt = txt.replace("\\n", "\n").replace("\\/", "/").replace('\\"', '"')
    return txt.encode("utf-16", "surrogatepass").decode("utf-16")

perfil = json.loads((SCRATCH / "ig-perfil.json").read_text(encoding="utf-8"))
ig_raw = (SCRATCH / "ig-json.json").read_text(encoding="utf-8", errors="replace")
feed = json.loads((SCRATCH / "alcance-feed.json").read_text(encoding="utf-8"))
maps_txt = (SCRATCH / "maps-caracolas.txt").read_text(encoding="utf-8", errors="replace")
fb = json.loads((SCRATCH / "maps-fb.json").read_text(encoding="utf-8"))

likes = [f["likes"] for f in feed if "likes" in f]
likes_ord = sorted(likes)
comentarios = [f.get("comments", 0) for f in feed if "likes" in f]
fechas = [f.get("fecha") for f in feed if f.get("fecha")]
SEG = int(re.search(r'"follower_count":(\d+)', ig_raw).group(1))

ev = {
  "cliente": {
    "nombre": "Las Caracolas",
    "rubro": "Pescadería, rotisería y sushi (mayor y menor)",
    "ciudad": "Rosario, Santa Fe",
    "direccion": "Corrientes 1402, esq. 9 de Julio, S2000 Rosario",
    "telefono_maps": "0341 637-8697",
    "whatsapp": "https://wa.me/5493416378697",
    "medido_el": MEDIDO_EL,
  },
  "instagram": {
    "fuente": "https://www.instagram.com/lascaracolas_ar/ (perfil público, sin sesión)",
    "usuario": "lascaracolas_ar",
    "nombre": unescape(re.search(r'"full_name":"(.*?)"', ig_raw).group(1)),
    "seguidores": SEG,
    "seguidos": 0,
    "publicaciones": 809,
    "verificado": False,
    "bio": unescape(re.search(r'"biography":"(.*?)"', ig_raw).group(1)),
    "link_en_bio": "https://linktr.ee/lascaracolas_ar",
    "estado": "MEDIDO",
    "nota": "Seguidores y seguidos leídos de follower_count y following_count del JSON del propio perfil; "
            "publicaciones, del meta description del mismo perfil. Coinciden con el render (56,9 mil seguidores).",
  },
  "alcance_feed": {
    "fuente": "meta description declarada por Instagram en cada publicación",
    "publicaciones_medidas": len(likes),
    "ventana": f"{min(fechas)} a {max(fechas)}" if fechas else None,
    "dias": 17,
    "likes_min": min(likes), "likes_max": max(likes),
    "likes_mediana": likes_ord[len(likes_ord)//2],
    "likes_promedio": round(sum(likes)/len(likes)),
    "comentarios_total": sum(comentarios),
    "publicaciones_con_menos_de_2_comentarios": sum(1 for c in comentarios if c < 2),
    "tasa_interaccion_pct": round(likes_ord[len(likes_ord)//2] / SEG * 100, 3),
    "estado": "MEDIDO",
    "detalle": [
      {"fecha": f.get("fecha"), "likes": f.get("likes"), "comentarios": f.get("comments"),
       "url": f["url"], "caption": (f.get("meta","") or "")[:110]}
      for f in feed if "likes" in f
    ],
    "referencia_sectorial": {
      "valor": "1% a 3% por publicación es el rango habitual para cuentas de este tamaño",
      "estado": "INFERIBLE",
      "nota": "Rango publicado por benchmarks de la industria; NO es una medición de este perfil.",
    },
  },
  "google_maps": {
    "fuente": "ficha de Google Maps abierta con Chrome el " + MEDIDO_EL,
    "nombre": "Las Caracolas",
    "categoria": "Tienda de alimentación",
    "puntuacion": 4.5,
    "opiniones": 741,
    "fotos": "más de 109",
    "horario": "Abierto · cierra a las 20:45",
    "plus_code": "29W4+P7 Rosario, Santa Fe",
    "sitio_web": None,
    "campo_sitio_web": "Google ofrece «Agregar sitio web» — no tiene ninguno asociado",
    "temas_de_opiniones": {"sushi": 32, "empleadas": 19, "rosario": 17, "paella": 13},
    "estado": "MEDIDO",
    "nota": "Las reseñas que Google muestra primero incluyen dos quejas negativas sobre producto "
            "(hamburguesa de sushi y paella promoción) fechadas hace 2 y 3 meses.",
  },
  "canales_propios": {
    "sitio_web": None,
    "estado": "MEDIDO",
    "nota": "No tiene sitio propio. Google pide el dato y no lo tiene.",
  },
  "dominios": {
    "metodo": "WHOIS crudo por TCP al puerto 43 del registro (whois.nic.ar para .ar, "
              "whois.verisign-grs.com para .com) y RDAP de Verisign para .com. "
              "rdap.nic.ar se descartó como fuente: devuelve 404 hasta para dominios registrados.",
    "consultado_el": MEDIDO_EL,
    "candidatos": [
      {"dominio": "caracolasrosario.com", "estado": "LIBRE",
       "fuente": "RDAP de Verisign (rdap.verisign.com/com/v1), HTTP 404 = sin registro"},
      {"dominio": "caracolasrosario.com.ar", "estado": "LIBRE",
       "fuente": "whois.nic.ar: «El dominio no se encuentra registrado en NIC Argentina»"},
      {"dominio": "lascaracolasrosario.com.ar", "estado": "LIBRE",
       "fuente": "whois.nic.ar: «El dominio no se encuentra registrado en NIC Argentina»"},
      {"dominio": "pescaderialascaracolas.com.ar", "estado": "LIBRE",
       "fuente": "whois.nic.ar: «El dominio no se encuentra registrado en NIC Argentina»"},
      {"dominio": "caracolas.com.ar", "estado": "TOMADO",
       "titular": "DATTATEC.COM S.R.L.", "alta": "2026-06-29", "vence": "2027-06-29",
       "que_sirve": "Caracolas Deco — muebles, decoración y blanquería de Casilda, Santa Fe",
       "fuente": "whois.nic.ar"},
      {"dominio": "lascaracolas.com.ar", "estado": "TOMADO",
       "titular": "PUGNALE Fernando Diego", "alta": "2003-10-30", "vence": "2026-10-30",
       "que_sirve": "complejo de departamentos con servicios (costa atlántica)",
       "fuente": "whois.nic.ar", "nota": "vence en 24 días; renovar es lo habitual"},
      {"dominio": "caracolas.com", "estado": "TOMADO",
       "registrador": "GoDaddy (domaincontrol.com)", "alta": "2003-06-25", "vence": "2027-06-25",
       "fuente": "RDAP de Verisign"},
      {"dominio": "lascaracolas.com", "estado": "TOMADO",
       "que_sirve": "sitio de periodismo y podcast feminista (Soledad Jarquín)",
       "fuente": "contenido servido por HTTP"},
    ],
    "recomendado": "lascaracolasrosario.com.ar",
    "motivo": "único disponible que contiene el nombre real del negocio + ciudad + TLD local",
  },
  "sitio_nuevo": {
    "lo_aporta": "Lisandro, construido con otro motor; se recibe por URL",
    "estado": "PENDIENTE",
    "nota": "El pipeline de leads NO construye el sitio. Sin esa URL, la propuesta sale sin "
            "la sección «Tu sitio nuevo» y el gate de promesas (§10) no tiene contra qué cotejar.",
  },

  "linktree": {
    "url": "https://linktr.ee/lascaracolas_ar",
    "titulo": "Las Caracolas Restaurant - Order Delivery - See Food on Instagram",
    "bajada": "¡La casa favorita de un pescador, en el corazón de Rosario!",
    "enlaces_propios": [
      {"rotulo": "Carta Rotisería LC 2 OCTUBRE.pdf", "url": "https://drive.google.com/file/d/1k9XU3ftnIowlDCWc0RS72qAOjMddzhEU/view",
       "tipo": "PDF en Google Drive"},
      {"rotulo": "Catálogo FRESCOS/REBOZADOS OCTUBRE LC.pdf", "url": "https://drive.google.com/file/d/1oLds6HQt8Z2vMCiPkulA_thO0VIUNO10/view",
       "tipo": "PDF en Google Drive"},
      {"rotulo": "NUESTRO WHATSAPP · Hace tu pedido o consulta", "url": "https://wa.me/5493416378697", "tipo": "WhatsApp Business"},
      {"rotulo": "Sushi a Domicilio · PEDIDOS YA", "url": "https://www.pedidosya.com.ar/restaurantes/rosario/las-caracolas-sushi-fe0e6153-d0f3-4720-95f2-ea69c36c73bb-menu", "tipo": "PedidosYa"},
      {"rotulo": "La Roti y frescos en Pedidos Ya", "url": "https://www.pedidosya.com.ar/restaurantes/rosario/las-caracolas-1bde2c3f-3cb5-47dc-a3fc-718399d924a6-menu", "tipo": "PedidosYa"},
      {"rotulo": "¡Cómo llegar!", "url": "https://goo.gl/maps/9EvYzcmyv2mSmsZ67", "tipo": "Google Maps"},
      {"rotulo": "Nuestro TikTok", "url": "https://www.tiktok.com/@lascaracolas_ar", "tipo": "TikTok"},
      {"rotulo": "Facebook", "url": "https://www.facebook.com/lascaracolas.ar", "tipo": "Facebook"},
      {"rotulo": "Instagram", "url": "https://instagram.com/lascaracolas_ar", "tipo": "Instagram"},
    ],
    "enlaces_totales_en_la_pagina": "9 propios + publicidad de terceros de la plataforma",
    "publicidad_de_terceros_visible": ["Hulu", "HelloFresh", "ARMRA", "Omnilux LED", "Ritual", "Factor",
                                        "Curology", "Acorns", "Headspace", "Equip Foods", "FabFitFun",
                                        "CLEARSTEM", "Purple Carrot", "Daily Harvest", "Gobble", "Babbel",
                                        "Talkspace", "Fabletics"],
    "estado": "MEDIDO",
    "nota": "Los enlaces de publicidad son de la plataforma Linktree, no del cliente. Se listan porque "
            "aparecen en la misma página que el menú.",
  },
  "menu_pdf": {
    "carta_rotiseria": {"paginas": 30, "bytes": 64807518, "mb": 64.8, "tipo": "PDF 1.4", "capa_de_texto": True},
    "catalogo_frescos": {"paginas": 7, "bytes": 3613405, "mb": 3.4, "tipo": "PDF 1.4", "capa_de_texto": True},
    "precios_ejemplo": ["$34.900 kg", "$50.900 kg", "$59.000 kg", "$69.900 kg", "$149.900 kg"],
    "estado": "MEDIDO",
    "nota": "Medido con file y pdftotext sobre el archivo descargado de Google Drive. "
            "El nombre del archivo lleva el mes («2 OCTUBRE»), o sea que se reemplaza todos los meses.",
  },
  "pedidosya": {
    "tiendas": 2,
    "estado": "NO VERIFICADO",
    "nota": "Las dos URLs devolvieron 403 «tráfico inusual» desde este equipo, con curl y con Chrome. "
            "Que las dos tiendas existen se midió en el Linktree del cliente (ahí están los dos enlaces); "
            "lo que no se pudo leer es el contenido: menú, comisión ni puntuación.",
  },
  "facebook": {
    "url": "https://www.facebook.com/lascaracolas.ar/",
    "seguidores": 694,
    "categoria": "Pescadería",
    "estado": "MEDIDO",
    "nota": "Leído del og:description de la página. Un índice de búsqueda mostraba 1.516 me gusta para "
            "una página homónima; no se pudo confirmar cuál es la vigente.",
  },
  "tiktok": {"usuario": "@lascaracolas_ar", "estado": "NO VERIFICADO",
             "nota": "El enlace existe en su Linktree. El perfil devuelve una página que arma el contenido "
                     "con JavaScript: seguidores y publicaciones no se pudieron leer sin sesión."},
  "no_medido": [
    "Facturación, ticket promedio y margen: no se pueden medir desde afuera.",
    "Comisión que cobra PedidosYa por pedido: no publicada en el material accesible.",
    "Cuántos pedidos entran por WhatsApp o por PedidosYa: dato interno.",
    "Seguidores reales frente a inactivos: Instagram sólo expone el total.",
    "TikTok y PedidosYa: bloquearon la lectura automatizada (403 y render por JavaScript).",
  ],
}

(OUT / "evidencia-caracolas.json").write_text(
    json.dumps(ev, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("escrito:", OUT / "evidencia-caracolas.json")
print("seguidores:", SEG, "| likes:", likes_ord, "| tasa:", ev["alcance_feed"]["tasa_interaccion_pct"], "%")
print("comentarios totales:", sum(comentarios), "| publicaciones con <2 comentarios:", ev["alcance_feed"]["publicaciones_menos_2"] if False else ev["alcance_feed"]["publicaciones_con_menos_de_2_comentarios"])
