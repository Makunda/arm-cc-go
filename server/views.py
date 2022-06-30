from server import app
from server.interfaces.ApiResponse import ApiResponse


@app.route('/status')
def index():
    return ApiResponse("Test message", {"Hello": "World"}, []).build()