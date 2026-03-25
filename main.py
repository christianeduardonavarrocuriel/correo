import web
import os
import sys


def set_static_cache_headers(seconds=604800):
    # Cache de 7 dias para recursos estaticos; immutable evita revalidaciones innecesarias.
    web.header('Cache-Control', f'public, max-age={seconds}, immutable')

# Definir las rutas
# Notar que '/' llevará a la clase 'index'
# Las rutas de estilos e imágenes se sirven manualmente si no se usa una carpeta 'static'
urls = (
    '/', 'index',
    '/styles/(.*)', 'styles',
    '/images/(.*)', 'images'
)

# Configurar el motor de plantillas
# El directorio es 'templates'
render = web.template.render('templates')

class index:
    def GET(self):
        # Desplegar templates/index.html
        return render.index()

class styles:
    def GET(self, file):
        # Servir archivos CSS desde la carpeta styles
        try:
            # Especificar el tipo de contenido para el CSS
            web.header('Content-Type', 'text/css')
            set_static_cache_headers()
            with open(os.path.join('styles', file), 'r') as f:
                return f.read()
        except FileNotFoundError:
            return web.notfound()

class images:
    def GET(self, file):
        # Servir imágenes desde la carpeta images
        try:
            # Intentar detectar el tipo de imagen basándose en la extensión
            if file.endswith('.png'):
                web.header('Content-Type', 'image/png')
            elif file.endswith('.webp'):
                web.header('Content-Type', 'image/webp')
            elif file.endswith('.jpg') or file.endswith('.jpeg'):
                web.header('Content-Type', 'image/jpeg')

            set_static_cache_headers()
            with open(os.path.join('images', file), 'rb') as f:
                return f.read()
        except FileNotFoundError:
            return web.notfound()

if __name__ == "__main__":
    # Para Render, necesitamos el puerto de la variable de entorno
    port = int(os.environ.get("PORT", 8080))
    
    # Se agrega el puerto a sys.argv para que web.py lo tome
    if len(sys.argv) <= 1:
         sys.argv.append(str(port))
    
    app = web.application(urls, globals())
    app.run()
