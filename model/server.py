from typing import Annotated
from fastapi import FastAPI, File

app = FastAPI()

@app.post("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict")
async def predict(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


def start_server(args):
    import uvicorn
    uvicorn.run("model.server:app", reload=args.reload)

