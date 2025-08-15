"""
My first application
"""

import asyncio
import queue
import threading

import toga
from toga.style import Pack

from fasthtml_app.main import app, msg_queue


class HelloWorld(toga.App):
    def web_server(self):
        from daphne.endpoints import build_endpoint_description_strings
        from daphne.server import Server

        endpoints = build_endpoint_description_strings(
            host="127.0.0.1",
            port=0,  # dynamic port allocation
        )
        endpoints = sorted(endpoints)

        self.server = Server(app, endpoints=endpoints)
        self.loop.call_soon_threadsafe(self.server_exists.set_result, "ready")

        # the runloop
        self.server.run()

    async def event_handler(self):
        while True:
            try:
                event = msg_queue.get(False, None)
            except queue.Empty:
                await asyncio.sleep(0.1)
            else:
                await self.handle_event(event)

    async def handle_event(self, event):
        info_dialog = toga.InfoDialog("Hello from Toga!", "Got event from fasthtml!")
        await self.main_window.dialog(info_dialog)

    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        # create an async background task that watches for new events
        self.background_tasks = set()
        task = asyncio.create_task(self.event_handler())
        self.background_tasks.add(task)
        task.add_done_callback(self.background_tasks.discard)

        self.webview = toga.WebView(
            on_webview_load=self.on_webview_loaded, style=Pack(flex=1)
        )

        self.main_window = toga.MainWindow()
        self.main_window.content = self.webview

        self.startup_server()

    def cleanup(self, app, **kwargs):
        print("Shutting down...")
        return True

    def startup_server(self):
        self.server_exists = asyncio.Future()
        self.server_thread = threading.Thread(target=self.web_server)
        self.server_thread.daemon = True  # makes it so c thread ends when python does
        self.server_thread.start()

        self.on_exit = self.cleanup

    async def on_running(self):
        await self.server_exists

        while not self.server.listening_addresses:
            await asyncio.sleep(0.1)

        host, port = self.server.listening_addresses[0]
        self.webview.url = f"http://{host}:{port}/"
        self.main_window.show()

    def on_webview_loaded(self, widget): ...


def main():
    return HelloWorld()
