import pytest
from fasthtml.common import H1
from fasthtml_app.main import app, rt, homepage


class TestFastHTMLApp:
    def test_app_creation(self):
        """Test that the FastHTML app is created properly."""
        assert app is not None
        assert rt is not None

    def test_homepage_function(self):
        """Test the homepage function returns correct HTML."""
        result = homepage()
        # Check that it's an H1 element by examining its tag
        assert hasattr(result, 'tag') and result.tag == 'h1'
        assert str(result) == "<h1>Hello from FastHTML</h1>"

    def test_homepage_route(self):
        """Test that the homepage route is registered."""
        # Check if the route exists in the app
        routes = [route for route in app.routes if route.path == "/"]
        assert len(routes) > 0
        
        # Find the GET route
        get_route = next((route for route in routes if "GET" in route.methods), None)
        assert get_route is not None