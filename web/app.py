from fastapi import File, UploadFile, HTTPException, FastAPI
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, PackageLoader, select_autoescape
from starlette.responses import HTMLResponse
app = FastAPI()

# only used in development. For production one should use nginx for that url
# one problem with that middleware it is an unconfigurable cache-control header
app.mount("/inventory/static", StaticFiles(directory="static"), name="static")

env = Environment(
    loader=PackageLoader("app"),
    autoescape=select_autoescape()
)
template = env.get_template("page.html")

@app.get("/inventory/{id}")
async def page(id: int):
    return HTMLResponse(template.render(
        image_src=f'/inventory/static/{id}',
        upload_url=f'/inventory/{id}/upload',
    ))

@app.post("/inventory/{id}/upload")
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
