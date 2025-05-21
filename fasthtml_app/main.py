from fasthtml.common import fast_app, H1

app, rt = fast_app()

@app.get("/")
def homepage():
    return H1("Hello from FastHTML")

