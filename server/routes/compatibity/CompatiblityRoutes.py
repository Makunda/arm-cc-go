from flask import request

from interface.go.GoPackage import GoPackage
from logger.Logger import Logger
from modules.ModuleDispatcher import ModuleDispatcher
from server import app
from server.interfaces.ApiResponse import ApiResponse
from server.middlewares import token_required

dispatcher = ModuleDispatcher()
__logger = Logger.get("GoRoutes")

@app.route('/check/<language>', methods=['POST'])
@token_required
def go_check(language:str):
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

    if not dispatcher.is_language_supported(language):
        # Malformed request
        return ApiResponse("Malformed request", None, [f"Incompatible '{language}' language."]).build()

    origin = ""
    if "origin" in data:
        # The package has a specific origin to try
        origin = data["origin"]

    package = GoPackage(data["name"], data["version"], str(origin))
    compatibility = dispatcher.analyze(language, package)

    __logger.info(f"Package: {package.name} - Compatibility {compatibility.compatible}")

    return ApiResponse("Compatibility result", compatibility.serialize(), []).build()
