# 6 · La web con stock en vivo (Fase 7)

## La ambición
Una web de catálogo nueva y bonita que muestre **lo que hay de verdad**: cuando un socio registra una venta desde el bot o la app, el producto baja de "Disponible ahora" en minutos, sin que nadie edite la web.

Secciones previstas:
- **Disponible ahora** (stock > 0).
- **Nuevos ingresos** (llegados recientemente).
- **Por encargo** (sin stock, o productos que se piden a Shein bajo demanda).
- Buscador, tonos/colores por producto y **carrito que termina en un mensaje de WhatsApp** con el pedido armado.
- Ocultar productos a mano desde la app.

El diseño visual, la estructura y los colores los define el dueño (con su diseño en Canva) **antes** de que se escriba una línea: la IA no propone un diseño propio.

## El problema: los tiempos
Google Sheets + Apps Script es gratis y cómodo, pero no es rápido:

| Medición real | Valor |
|---|---|
| Primer llamado tras un rato sin uso (arranque en frío) | 10–20 s |
| Lectura típica en el servidor | 0,7–2,1 s |
| Ida y vuelta percibida desde el navegador | 3–6 s |
| Cuotas de Apps Script | Limitadas por día y por usuario |

Una web pública no puede esperar 10 s ni depender de que Apps Script aguante cada visita.

## La solución: la web nunca espera al Sheet

```
Venta / compra / ajuste en la app o el bot
        │  (la escritura ya pasa por el Apps Script)
        ▼
Pestaña catalogo_publico (solo: nombre, precio de lista, tonos, estado, foto)
        │
        ├──► Endpoint público de un Apps Script APARTE, con CacheService de 1–5 min
        │
        └──► n8n cada N minutos (o al detectar un cambio): genera catalogo.json
                   y lo publica en el hosting estático vía GitHub
                                │
                                ▼
            Web estática (Cloudflare Pages, gratis) lee catalogo.json del mismo dominio:
            carga en milisegundos, desde la CDN, aunque Google esté lento
```

Decisiones de diseño:
1. **Separación total.** La web solo conoce `catalogo_publico`, servida por un Apps Script independiente. Nunca ve costos, márgenes, clientes ni el Sheet. Una prueba automática verifica que la respuesta no trae esos campos.
2. **Instantánea en JSON en la CDN** como fuente principal. La web abre al instante; el endpoint con caché queda como respaldo y para verificar.
3. **Frescura acotada y medible:** objetivo "una venta se refleja en la web en ≤ 5 minutos". Es suficiente para un negocio que vende por WhatsApp, y evita llamar a Google en cada visita.
4. **Sin stock → Por encargo**, no "agotado": la venta no se pierde.
5. **Fotos fuera de Drive.** El original queda en Drive; n8n genera una copia **WebP en dos tamaños** y la publica en el hosting. La web no depende de enlaces de Drive (lentos y con límites).
6. **Flujo de fotos por Telegram:** el bot lista los productos sin foto; el socio envía la foto **como archivo** (sin compresión); n8n la procesa y la publica. Fotos repetidas o muy pesadas se rechazan con aviso.

## Pruebas planeadas
- La respuesta del endpoint y el JSON **nunca** incluyen costo, margen ni clientes.
- Producto sin foto → imagen de reserva.
- Venta en la app → la web la refleja en ≤ 5 min.
- Celular y escritorio; foto repetida o muy pesada.

## Estimación
5–8 sesiones, una vez entregado el diseño. Depende de: diseño en Canva, logo y fotos.

## Si tu negocio crece más allá de esto
La arquitectura deja una salida clara: la web ya consume un JSON estático, así que cambiar Sheets por una base de datos real (Supabase, Postgres) solo cambia **quién genera el JSON**, no la web.
