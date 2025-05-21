import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import daphne
import asyncio
from threading import Thread


class FastHTMLApp(toga.App):
    def web_server(self):
        from fasthtml_app.main import app
        from daphne.server import Server
        from daphne.endpoints import build_endpoint_description_strings

        endpoints = build_endpoint_description_strings(
            host="127.0.0.1",
            port=0  # dynamic port allocation
        )
        endpoints = sorted(endpoints)

        self.server = Server(app, endpoints=endpoints)
        self.loop.call_soon_threadsafe(self.server_exists.set_result, "ready")

        # the runloop
        self.server.run()

    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.webview = toga.WebView(
            on_webview_load=self.on_webview_loaded, style=Pack(flex=1)
        )

        self.main_window = toga.MainWindow()
        self.main_window.content = self.webview

        self.startup_server()

    def cleanup(self, app, **kwargs):
        print("Shutting down...")
        self.server.stop()
        return True

    def startup_server(self):
        self.server_exists = asyncio.Future()
        self.server_thread = Thread(target=self.web_server)
        self.server_thread.start()

        self.on_exit = self.cleanup


    async def on_running(self):
        await self.server_exists

        while not self.server.listening_addresses:
            await asyncio.sleep(0.1)

        host, port = self.server.listening_addresses[0]
        self.webview.url = f"http://{host}:{port}/"
        self.main_window.show()

    def on_webview_loaded(self, widget):
        ...


def main():
    return FastHTMLApp("FastHTML Toga Example", "com.dataconcise.fasthtml_toga")

if __name__ == "__main__":
    main().main_loop()
