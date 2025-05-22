import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock


class TestFastHTMLAppMethods:
    """Test individual methods of FastHTMLApp without instantiating the full Toga app."""
    
    def test_cleanup_method(self):
        """Test the cleanup method works correctly."""
        # Mock the app class and create a fake instance
        mock_app = Mock()
        mock_app.server = Mock()
        
        # Import and test the cleanup method directly
        from app import FastHTMLApp
        result = FastHTMLApp.cleanup(mock_app, mock_app)
        
        mock_app.server.stop.assert_called_once()
        assert result is True

    def test_on_webview_loaded_method(self):
        """Test the on_webview_loaded method."""
        from app import FastHTMLApp
        
        mock_app = Mock()
        mock_widget = Mock()
        
        # Should not raise any exceptions
        FastHTMLApp.on_webview_loaded(mock_app, mock_widget)

    @pytest.mark.asyncio
    async def test_on_running_method(self):
        """Test the on_running method logic."""
        from app import FastHTMLApp
        
        mock_app = Mock()
        mock_app.server_exists = asyncio.Future()
        mock_app.server_exists.set_result("ready")
        
        mock_server = Mock()
        mock_server.listening_addresses = [("127.0.0.1", 8000)]
        mock_app.server = mock_server
        
        mock_webview = Mock()
        mock_app.webview = mock_webview
        
        mock_window = Mock()
        mock_app.main_window = mock_window
        
        await FastHTMLApp.on_running(mock_app)
        
        assert mock_webview.url == "http://127.0.0.1:8000/"
        mock_window.show.assert_called_once()

    @pytest.mark.asyncio
    async def test_on_running_waits_for_server(self):
        """Test that on_running waits for server to be ready."""
        from app import FastHTMLApp
        
        mock_app = Mock()
        mock_app.server_exists = asyncio.Future()
        mock_app.server_exists.set_result("ready")
        
        mock_server = Mock()
        # Start with empty addresses
        mock_server.listening_addresses = []
        mock_app.server = mock_server
        
        mock_webview = Mock()
        mock_app.webview = mock_webview
        
        mock_window = Mock()
        mock_app.main_window = mock_window
        
        # Set up server to become ready after short delay
        async def make_server_ready():
            await asyncio.sleep(0.1)
            mock_server.listening_addresses = [("127.0.0.1", 8000)]
        
        # Start the task and run on_running
        task = asyncio.create_task(make_server_ready())
        await FastHTMLApp.on_running(mock_app)
        await task
        
        assert mock_webview.url == "http://127.0.0.1:8000/"
        mock_window.show.assert_called_once()

    @patch('daphne.server.Server')
    @patch('daphne.endpoints.build_endpoint_description_strings')
    def test_web_server_method(self, mock_endpoints, mock_server):
        """Test the web_server method."""
        from app import FastHTMLApp
        
        mock_endpoints.return_value = ["tcp:port=8000:interface=127.0.0.1"]
        mock_server_instance = Mock()
        mock_server.return_value = mock_server_instance
        
        mock_app = Mock()
        mock_app.server_exists = asyncio.Future()
        mock_app.loop = asyncio.get_event_loop()
        
        with patch.object(mock_app.loop, 'call_soon_threadsafe') as mock_call:
            FastHTMLApp.web_server(mock_app)
            
        mock_endpoints.assert_called_once_with(host="127.0.0.1", port=0)
        mock_server.assert_called_once()
        mock_server_instance.run.assert_called_once()
        assert mock_app.server == mock_server_instance

    @patch('app.Thread')
    def test_startup_server_method(self, mock_thread_class):
        """Test the startup_server method."""
        from app import FastHTMLApp
        
        mock_app = Mock()
        mock_thread_instance = Mock()
        mock_thread_class.return_value = mock_thread_instance
        
        FastHTMLApp.startup_server(mock_app)
        
        mock_thread_class.assert_called_once_with(target=mock_app.web_server)
        mock_thread_instance.start.assert_called_once()
        assert isinstance(mock_app.server_exists, asyncio.Future)
        assert mock_app.on_exit == mock_app.cleanup

    @patch('toga.WebView')
    @patch('toga.MainWindow')
    def test_startup_method(self, mock_window, mock_webview):
        """Test the startup method."""
        from app import FastHTMLApp
        
        mock_webview_instance = Mock()
        mock_webview.return_value = mock_webview_instance
        mock_window_instance = Mock()
        mock_window.return_value = mock_window_instance
        
        mock_app = Mock()
        mock_app.startup_server = Mock()
        
        FastHTMLApp.startup(mock_app)
        
        mock_webview.assert_called_once()
        assert mock_app.webview == mock_webview_instance
        assert mock_app.main_window == mock_window_instance
        assert mock_app.main_window.content == mock_webview_instance
        mock_app.startup_server.assert_called_once()


@patch('app.FastHTMLApp')
def test_main_function(mock_app_class):
    """Test the main function creates the correct app."""
    from app import main
    
    mock_app = Mock()
    mock_app_class.return_value = mock_app
    
    result = main()
    
    mock_app_class.assert_called_once_with("FastHTML Toga Example", "com.dataconcise.fasthtml_toga")
    assert result == mock_app


class TestIntegration:
    """Integration tests that verify the components work together."""
    
    def test_app_imports_correctly(self):
        """Test that the app module imports without errors."""
        from app import FastHTMLApp, main
        assert FastHTMLApp is not None
        assert main is not None
    
    def test_fasthtml_app_imports_correctly(self):
        """Test that fasthtml components import correctly."""
        from fasthtml_app.main import app, rt, homepage
        assert app is not None
        assert rt is not None
        assert homepage is not None