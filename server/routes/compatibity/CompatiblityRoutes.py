from flask import request

from codes.HttpCodes import HttpStatus
from enumerations.Language import Language
from interface.Package import Package
from interface.go.GoPackage import GoPackage
from logger.Logger import Logger
from modules.ModuleDispatcher import ModuleDispatcher
from server import app
from server.interfaces.ApiResponse import ApiResponse
from server.Middlewares import token_required

dispatcher = ModuleDispatcher()
__logger = Logger.get("GoRoutes")


@app.route('/check/<language>', methods=['POST'])
@token_required
def package_check(language: str):
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

    try:
        language_enum = Language.from_str(language)
        if not dispatcher.is_language_implemented(language_enum):
            raise KeyError
    except:
        __logger.info(f"Language: '{language}' has not been recognized or is not compatible with"
                      f" [{', '.join(dispatcher.get_languages_implemented())}]")
        return ApiResponse("Malformed request", None, [f"Incompatible '{language}' language."]).build()

    origin = ""
    if "origin" in data:
        # The package has a specific origin to try
        origin = data["origin"]

    target = None
    if "target" in data:
        target = data["target"]

    try:
        package = Package(data["name"], data["version"], str(origin), target)
    except Exception as e:
        __logger.info(f"Failed to build the package", e)
        return ApiResponse("Compatibility result", None, ["Invalid package data sent"], 400).build()

    try:
        compatibility = dispatcher.analyze(language_enum, package)
        __logger.info(f"Package: {package.name} - Compatibility {compatibility.compatible}")
        return ApiResponse("Compatibility result", compatibility.serialize(), []).build()
    except Exception as e:
        __logger.info(f"Failed to get the compatibility of package", e)
        return ApiResponse("Compatibility result", None, ["Invalid language"], 400).build()
