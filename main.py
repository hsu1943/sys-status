import uvicorn
from fastapi import FastAPI
from utils import response
from router import api

app = FastAPI()


# 默认接口
@app.post("/")
@app.put("/")
@app.delete("/")
@app.get("/")
@app.options("/")
@app.head("/")
@app.patch("/")
@app.trace("/")
async def index():
    return response.resp_200(data={
        'hi': 'Hello World'
    })

app.include_router(api.router, prefix='/sys-status/api')


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8005, reload=True, debug=False)
