from fastapi import File, UploadFile, HTTPException, FastAPI
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, PackageLoader, select_autoescape
from starlette.responses import HTMLResponse
app = FastAPI()

# only used in development. For production one should use nginx for that url
# one problem with that middleware it is an unconfigurable cache-control header
app.mount("/api/inventory/static", StaticFiles(directory="static"), name="static")

@app.post("/api/inventory/{id}")
def upload(id: int, file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(f'static/{id}', 'wb') as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        file.file.close()

    return {"status": "OK"}
