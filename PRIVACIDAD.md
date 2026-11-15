# Privacidad: qué se publica y qué no

Este repositorio es la versión pública de un proyecto privado. La regla es simple: **se publica el método, nunca los datos ni las llaves.**

## Nunca entra aquí
- Tokens, llaves de API, contraseñas, secretos compartidos entre n8n y Apps Script.
- Enlaces o IDs de Google Sheets, Drive, Apps Script e implementaciones (`/exec`).
- Dominio y dirección del servidor de n8n, IDs de webhooks.
- Nombre de usuario del bot, IDs de chats, grupos y usuarios de Telegram.
- Correos, celulares, nombres completos y ciudad de los socios.
- Datos de clientes, montos reales de deudas o ventas, capturas de pedidos o comprobantes.
- El código de producción tal cual (trae constantes de configuración). Se describe la arquitectura y se publican plantillas.
- El nombre del repositorio privado, su rama o su usuario.

## Sí se publica
- El nombre del proyecto (Oura) y el tipo de negocio.
- La arquitectura, las decisiones técnicas y por qué se tomaron.
- La bitácora de tareas (qué se construyó y qué se aprendió), con fechas.
- Las reglas, roles y plantillas del sistema multiagente.
- Cifras agregadas del proyecto (commits, tareas, número de pruebas), nunca del negocio.

## Cómo se verifica
`verificar_privacidad.py` busca patrones de secretos (llaves de Google, tokens de Telegram, llaves de Groq/OpenAI/GitHub, llaves privadas), enlaces e IDs de Google, IDs de Telegram, celulares, correos y dominios de túnel. Además lee `.privacidad-local.txt`, una lista negra con nombres e IDs reales que **solo existe en el computador del dueño** (está en `.gitignore`), para que la lista misma no sea una filtración.

```bash
python verificar_privacidad.py --probar   # autoprueba de los patrones
python verificar_privacidad.py            # revisa la carpeta; código de salida 1 si hay hallazgos
```

El script no imprime el valor encontrado, solo archivo, línea y tipo. Si algo se filtró en un commit ya subido, no basta con borrarlo en un commit nuevo: hay que **rotar la llave** (crear una nueva e invalidar la vieja) y reescribir el historial.
