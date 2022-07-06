from flask import request

from interface.go.GoPackage import GoPackage
from pull.GoPullEngine import GoPullEngine
from server import app
from server.interfaces.ApiResponse import ApiResponse
from server.middlewares import token_required

goPullEngine = GoPullEngine()


@app.route('/go/check', methods=['POST'])
@token_required
def go_check():
    """
        Check the compatibility of a Go package
    """
    # Process the request containing the go package
    data = request.json

    # Verify data sent
    if not data["name"]:
        # Malformed request
        return ApiResponse("Malformed package", None, ["Malformed request: Missing 'name' field."])

    if not data["version"]:
        # Malformed request
        return ApiResponse("Malformed package", None, ["Malformed request: Missing 'version' field."])

    origin = ""
    if data["origin"]:
        # The package has a specific origin to try
        origin = data["origin"]

    package = GoPackage(data["name"], data["version"], str(origin))
    compatibility = goPullEngine.pull_package(package)

    return ApiResponse("Compatibility result", compatibility.serialize(), []).build()
