import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Sirve recursos estáticos desde las carpetas existentes.
app.mount("/styles", StaticFiles(directory="styles"), name="styles")
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/")
def index():
    return FileResponse(os.path.join("templates", "index.html"))

if __name__ == "__main__":
    import uvicorn

    # Render asigna el puerto en la variable de entorno PORT.
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
