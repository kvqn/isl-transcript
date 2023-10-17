from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

def start_server(args):
    import uvicorn
    uvicorn.run("model.server:app", reload=args.reload)

