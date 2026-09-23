# ErsCh.dev Portfolio

Portafolio personal de Erick Salvador Chinchilla Chiquillo, construido con Astro y Tailwind CSS. El sitio presenta el perfil profesional, stack tecnológico, experiencia, educación, proyectos y un formulario de contacto conectado a una API Python.

## Uso local

### Frontend

Requisitos: Node.js 18 o superior.

```bash
npm install
npm run dev
```

El sitio estará disponible en `http://localhost:4321`.

Para generar y revisar la versión estática:

```bash
npm run build
npm run preview
```

### API

Requisitos: Python 3.10 o superior.

```bash
cd api
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn main:app --reload --port 8000
```

La API queda disponible en `http://localhost:8000`. Su documentación interactiva está en `/docs`.

Para desarrollo local, el frontend usa `http://localhost:8000` por defecto. En producción se debe definir `PUBLIC_API_URL` antes del build:

```env
PUBLIC_API_URL=https://api.tu-dominio.com
```

## Composición

```text
src/
  components/       Secciones reutilizables de la página
  data/             Contenido del perfil y proyectos
  layouts/          Documento HTML base y selector de idioma
  pages/            Rutas Astro; index.astro compone la página principal
  styles/           Tokens y estilos globales de Tailwind
api/
  main.py           API FastAPI y endpoint de contacto
  requirements.txt  Dependencias Python
```

La página principal se compone en `src/pages/index.astro` usando `BaseLayout`, `Header`, `Hero`, las secciones de contenido, `Contact` y `Footer`. El contenido editable del portafolio vive principalmente en `src/data/portfolio.ts`.

## Endpoint de contacto

`POST /api/contact` acepta `name`, `email` y `message` como formulario `multipart/form-data` o `application/x-www-form-urlencoded`. Valida los campos, aplica límites de longitud y registra el mensaje en el servidor. La respuesta exitosa es:

```json
{"ok": true, "message": "Mensaje recibido correctamente"}
```

La API incluye CORS configurable, pero todavía no envía correos ni guarda en una base de datos. Para producción se debe conectar un proveedor de correo o persistencia y definir `ALLOWED_ORIGINS` con el dominio real del frontend.

## Publicación

El frontend puede desplegarse en Netlify, Vercel, GitHub Pages u otro hosting estático. La API debe desplegarse como servicio Python independiente, por ejemplo en Render, Railway, Fly.io o un VPS. Nunca se deben subir archivos `.env` ni credenciales al repositorio.
