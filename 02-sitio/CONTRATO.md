# CONTRATO DEL SITIO NUEVO — Las Caracolas

Este archivo es la orden de trabajo y, a la vez, el criterio con el que el trabajo
se va a aceptar o rechazar. Está generado desde `config.json`: **no lo edites acá**,
se regenera.

---

## TAREA

Construir el sitio web nuevo de **Las Caracolas** — Pescadería, rotisería y sushi — como un sitio
estático de una sola página (`index.html`) más sus recursos, listo para publicarse.
Es un reemplazo del sitio que hoy no existe: su presencia actual es Instagram y un
PDF del menú alojado en Google Drive.

## ALCANCE

Escribí **únicamente** dentro del directorio actual (`02-sitio/`). Los archivos que
podés crear o modificar son:

- `index.html`
- `assets/` (imágenes, hojas de estilo, lo que necesites)
- `robots.txt`
- `sitemap.xml`

No toques nada fuera de este directorio. No crees README, ni notas, ni archivos de
prueba. No instales dependencias: es HTML, CSS y, si hace falta, JavaScript del lado
del navegador, sin frameworks ni CDN de terceros.

## DATOS REALES (usá estos, no inventes otros)

| Dato | Valor |
|---|---|
| Nombre | Las Caracolas |
| Qué es | Pescadería, rotisería y sushi |
| Rubro y ciudad | Pescadería y rotisería · mayor y menor · Rosario |
| Dirección | Corrientes 1402, esq. 9 de Julio — S2000 Rosario, Santa Fe |
| Teléfono | 0341 637-8697 |
| WhatsApp | +5493416378697 |
| Mensaje que abre el WhatsApp | «Hola! Quiero hacer un pedido.» |
| Horarios | Abierto hasta las 20:45 |
| Cómo llegar | https://goo.gl/maps/9EvYzcmyv2mSmsZ67 |
| Color de marca | `#F00070` (medido del logo real) |
| Habilitación | — |
| URL canónica (C03) | **(pendiente: el dominio todavía no está definido)** |
| Dominio previsto | lascaracolasrosario.com.ar — verificado libre en el NIC el 6/10/2026; todavía no comprado |

Redes (enlazalas tal cual):
- Instagram: https://www.instagram.com/lascaracolas_ar/
- TikTok: https://www.tiktok.com/@lascaracolas_ar
- Facebook: https://www.facebook.com/lascaracolas.ar

Productos y secciones de contenido:
- Pescados frescos por kilo: merluza, boga, cornalitos, y lo que marque la temporada
- Mariscos: enteros, pelados, media valva y cazuela
- Frescos y rebozados, listos para cocinar
- Rotisería: platos preparados, paella
- Sushi: la Sushi Burguer (dicen ser los creadores en Argentina) y combos
- Mayor y menor: atienden a particulares y a otros locales

Secciones que la navegación **tiene que tener** (la propuesta promete 7):
- Inicio · (portada con la Sushi Burguer y el pedido por WhatsApp)
- Pescados y mariscos · fresco del día, por kilo
- Frescos y rebozados · el catálogo que hoy es un PDF
- Rotisería · platos preparados y para llevar
- Sushi · la Sushi Burguer y los combos, con delivery
- Delivery · WhatsApp y las dos tiendas de PedidosYa
- Cómo llegar y contacto · dirección, teléfono, horarios y mapa

### Reglas de contenido

1. **Todo dato que sale de esta tabla se escribe como texto en el HTML** (no como
   imagen): dirección, teléfono, horarios y productos. Es lo que Google lee.
2. **Lo que dice «falta en la config» no se inventa y no se rellena con un
   supuesto.** Si falta el horario, la sección de horarios muestra «Consultá por
   WhatsApp» y vos lo anotás en tu respuesta final como dato pendiente.
3. **No hay fotos propias del cliente.** No hay que usar fotos de terceros ni
   imágenes bajadas de internet. Construí las piezas gráficas que necesites como
   SVG propios (patrones, siluetas, íconos), todos con `alt` descriptivo en
   español. `C08` (srcset) queda declarado como pendiente por este motivo.
4. Español de Argentina, trato de **vos**, sin signos de admiración apilados y sin
   emojis en el cuerpo del texto.
5. **No inventes el dominio ni la URL canónica.** Si la tabla dice que están
   pendientes, poné exactamente `href="PENDIENTE-DOMINIO"` en el `canonical` y en el
   `og:url`, y anotalo en tu respuesta. Un dominio adivinado a partir del nombre del
   negocio puede ser el sitio de otra empresa: el criterio C18 rechaza cualquier
   dominio que no esté declarado en esa tabla.

## ACEPTACIÓN

El trabajo se acepta sólo si pasa **los 18 criterios** de esta lista. Son
ejecutables: el script que los corre después parsea tu `index.html` y tus archivos.

| # | Criterio | Tipo |
|---|---|---|
| C01 | Idioma declarado es-AR | bloqueante |
| C02 | Descripción para Google de 120 a 165 caracteres | bloqueante |
| C03 | URL canónica | bloqueante |
| C04 | Datos estructurados JSON-LD válidos | bloqueante |
| C05 | 8+ llamados a WhatsApp | bloqueante |
| C06 | Toda imagen con texto alternativo real | bloqueante |
| C07 | Carga diferida (salvo la portada) | bloqueante |
| C08 | Imágenes con srcset | declarable |
| C09 | Exactamente un h1 | bloqueante |
| C10 | 5+ h2 (jerarquía) | bloqueante |
| C11 | 6+ etiquetas Open Graph | bloqueante |
| C12 | Navegación con las secciones prometidas | bloqueante |
| C13 | robots.txt | bloqueante |
| C14 | sitemap.xml | bloqueante |
| C15 | Dirección y teléfono como texto visible | bloqueante |
| C16 | Enlace telefónico tel: | bloqueante |
| C17 | Formulario con etiquetas reales | bloqueante |
| C18 | Ningún dominio de terceros sin declarar | bloqueante |

Detalle de los que se prestan a confusión:

- **C02:** la meta description debe medir entre 120 y 165 caracteres.
  Contá los caracteres antes de entregar.
- **C05:** 8 enlaces `wa.me` como mínimo, todos apuntando a
  `https://wa.me/5493416378697`. El número va en formato internacional sin `+`.
- **C06/C07:** **todas** las `<img>` con `alt` de 3 caracteres o más; todas con
  `loading="lazy"` salvo la de portada, que va primero y con `fetchpriority="high"`.
- **C09/C10:** exactamente **un** `<h1>`, y **5 o más** `<h2>`.
- **C12:** la `<nav>` o el `<header>` tiene que tener al menos **7 enlaces**.
- **C15:** la dirección y el teléfono tienen que poder leerse como texto en el DOM.
- **C17:** si ponés un formulario, cada campo necesita su `<label>`.

## RESTRICCIONES

1. Nada de CDN ni de librerías externas: el sitio tiene que funcionar sin red más
   allá del propio archivo.
2. Nada de datos inventados: ni teléfonos, ni horarios, ni precios, ni reseñas, ni
   direcciones. Si te falta un dato, decilo, no lo completes.
3. Nada de fotos de terceros.
4. No corras `git`. No publiques nada. No salgas del directorio.
5. No uses `target="_blank"` en enlaces internos: no navega en webviews.

## EVIDENCIA QUE TENÉS QUE DEVOLVER

1. La lista de archivos que creaste, con su tamaño.
2. **La cuenta de caracteres de tu meta description** y el valor exacto.
3. Cuántos enlaces `wa.me`, cuántos `<h1>`, cuántos `<h2>` y cuántas `<img>` con
   `alt` quedaron en el archivo final — contados sobre el archivo, no de memoria.
4. Qué datos de la tabla quedaron **pendientes** y por qué.

