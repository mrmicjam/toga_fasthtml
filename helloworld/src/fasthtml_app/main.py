import pathlib
import queue

from fasthtml.common import H1, A, Div, Script, fast_app

# in android, default sesskey path isn't in a writable spot
app, rt = fast_app(key_fname=str(pathlib.Path(__file__).parent / ".sesskey"))

msg_queue = queue.Queue()


@app.get("/")
def homepage():
    return Div(
        H1("Hello from FastHTML"),
        Script("""
        async function call_event(url){
            await fetch(url);
        }
        """),
        A(
            "hello",
            href="javascript:void(0);",
            onclick="call_event('/hello');",
        ),
    )


@app.get("/hello")
def hello():
    msg_queue.put(1)
