import web
import os
import sys

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
            f = open(os.path.join('styles', file), 'r')
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
            elif file.endswith('.jpg') or file.endswith('.jpeg'):
                web.header('Content-Type', 'image/jpeg')
            
            f = open(os.path.join('images', file), 'rb')
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
