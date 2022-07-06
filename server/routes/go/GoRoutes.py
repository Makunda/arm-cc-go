from flask import request

from interface.go.GoPackage import GoPackage
from logger.Logger import Logger
from pull.GoPullEngine import GoPullEngine
from server import app
from server.interfaces.ApiResponse import ApiResponse
from server.middlewares import token_required

goPullEngine = GoPullEngine()
__logger = Logger.get("GoRoutes")

@app.route('/go/check', methods=['POST'])
@token_required
def go_check():
    """
       Check the compatibility of a Go package
    """
    # Process the request containing the go package
    data = request.json

    # Verify data sent
    if "name" not in data:
        # Malformed request
        return ApiResponse("Malformed request", None, ["Missing 'name' field."]).build()

    if "version" not in data:
        # Malformed request
        return ApiResponse("Malformed request", None, ["Missing 'version' field."]).build()

    origin = ""
    if "origin" in data:
        # The package has a specific origin to try
        origin = data["origin"]

    package = GoPackage(data["name"], data["version"], str(origin))
    compatibility = goPullEngine.pull_package(package)

    __logger.info(f"Package: {package.name} - Compatibility {compatibility.compatible}")

    return ApiResponse("Compatibility result", compatibility.serialize(), []).build()
