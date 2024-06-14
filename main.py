from fastapi import FastAPI, HTTPException, Response, Query
from gradio_client import Client, file
import shutil

app = FastAPI()

@app.get("/")
async def TraerPrenda(background_url: str = Query(..., description="URL de la imagen de fondo"),
                      garment_url: str = Query(..., description="URL de la imagen de prenda")):
    try:
        client = Client("ChrisJohnson111/test4")
        
        # Realiza la predicción con las URLs proporcionadas
        result = client.predict(
            dict={"background": file(background_url), "layers": [], "composite": None},
            garm_img=file(garment_url),
            garment_des="Hello!!",
            is_checked=True,
            is_checked_crop=False,
            denoise_steps=30,
            seed=42,
            api_name="/tryon"
        )
        
        # Suponiendo que result es una lista de rutas locales de imágenes generadas
        # Devuelve la primera imagen como respuesta
        if result:
            image_path = result[0]
            return await file_response(image_path)
        
        return {"error": "No se encontraron imágenes generadas por la predicción."}
        
    except Exception as e:
        return {"error": str(e)}  # Manejo básico de errores y devolución de mensaje de error

async def file_response(file_path: str):
    try:
        with open(file_path, mode="rb") as file:
            content = file.read()
        return Response(content, media_type="image/png")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
