from fastapi import FastAPI

app = FastAPI(
    title="Blog API",
    version="1.0.0"
)


@app.get("/blog")
def get_blogs():
    return []
