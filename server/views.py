from logger.Logger import Logger
from server import app
from server.interfaces.ApiResponse import ApiResponse

######################################################
#                    Variables                       #
######################################################
from server.middlewares import token_required

__logger = Logger.get("Server Views")


@app.route('/status')
def index():
    return ApiResponse("Health Check", {"Running": True}, []).build()


@app.route('/status/auth')
@token_required
def index_auth():
    return ApiResponse("Health Check", {"Running": True, "Authenticated": True}, []).build()


import server.routes.go.GoRoutes
