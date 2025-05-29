import queue

from fasthtml.common import H1, A, Div, fast_app

app, rt = fast_app()


msg_queue = queue.Queue()


@app.get("/")
def homepage():
    return Div(H1("Hello from FastHTML"), A("hello", href="/hello"))


@app.get("/hello")
def hello():
    msg_queue.put(1)
