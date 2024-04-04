# - paths dev & prod 
# - send error
import os
from pathlib import Path, PurePosixPath
from flask import jsonify, request, current_app, redirect
import jwt
import requests
import match

class GetRights():
    """docstring for SendErrot"""
    def __new__(self, userdata :dict, module :str, mode :str):
        rights = userdata['permissions']
        match mode:
            case "ro":
                r = self.hasReadPermission(rights, module)
            case "rw":
                r = (self.hasWritePermission(rights, module) and self.hasReadPermission(rights, module))
            case "w":
                r = self.hasWritePermission(rights, module)
        if r:
            return True, None
        else:
            return False, SendError("You don't have the permissions to access this ressource", 403)
    def hasReadPermission(rights: dict, module: str):
        return module in rights['read']
    def hasWritePermission(rights: dict, module: str):
        return module in rights['write']

class PathUtils():
    rootpath = None
    
    def __init__(self):
        if os.getenv("DEBUG", "FALSE") == "TRUE":
            self.rootpath = Path(__file__).parent.parent / "dev_env"
        else:
            self.rootpath = PurePosixPath("/") / "var" / "lib" / "kirbi"
    
    def getRootPath(self) -> Path: 
        """Retrieve the application root path

        Returns:
            Path: path to the root data directory
        """
        return self.rootpath
    
    def getDataPath(self) -> Path:
        """Retrieve the application data path

        Returns:
            Path: path to the data directory
        """
        return self.rootpath / "data"
    
    def getSharedPath(self) -> Path:
        """Retrieve the application shared path

        Returns:
            Path: path to the shared directory
        """
        return self.rootpath / "shared"

class SendError(object):
    """docstring for SendErrot"""
    def __new__(self, message: str, code: int=400, debug: str="") -> tuple[str, int]:
        if debug != "":
            debug = " > "+debug
        print(message+debug)    
        return jsonify({"status": "error", "error_message": message}), code

class GetUserSession(object):
    """docstring for SendErrot"""
    def __new__(self):
        if request.cookies.get('token') is not None:
            token = request.cookies.get('token')
        else :
            try :
                authorization = request.headers['Authorization'].split(" ")
                if authorization[0] == "Bearer":
                    token = authorization[1]
                else :
                    return False, "Invalid authentication method", None
            except (KeyError, IndexError) :
                return False, "Please provide 'token' cookie OR username and password as HTTP basic auth header", redirect("/auth/login", code=302)
            
        pUtils = PathUtils()
        with open(pUtils.getSharedPath() / "jwt_rsa.pem", mode="rb") as pubkey:
            try:
                data = jwt.decode(token, pubkey.read(), algorithms="RS256")
                return True, data, None
            except jwt.exceptions.InvalidSignatureError:
                return False, "Invalid signature", None
            except jwt.exceptions.DecodeError:
                return False, "Wrong token format", None
            except jwt.ExpiredSignatureError:
                return False, "Expired token", redirect("/auth/login", code=302)
            except jwt.exceptions.InvalidAlgorithmError:
                return False, "Unexpected algorithm", None

    @staticmethod
    def request(url: str, method: str, data: dict = None):
        """
        Send a request to another API with the user's token
        """
        headers = {
            "Authorization": f"Bearer {request.cookies.get('token')}"
        }
        if data is not None:
            r = requests.request(method, url, headers=headers, json=data)
        else:
            r = requests.request(method, url, headers=headers)
        return r
class GetRights():
    """docstring for SendErrot"""
    def __new__(self, userdata :dict, module :str, mode :str):
        rights = userdata['permissions']
        match mode:
            case "ro":
                r = self.hasReadPermission(rights, module)
            case "rw":
                r = (self.hasWritePermission(rights, module) and self.hasReadPermission(rights, module))
            case "w":
                r = self.hasWritePermission(rights, module)
        if r:
            return True, None
        else:
            return False, SendError("You don't have the permissions to access this ressource", 403)
    def hasReadPermission(rights: dict, module: str):
        return module in rights['read']
    def hasWritePermission(rights: dict, module: str):
        return module in rights['write']

def RedirectToLoginURL() -> redirect:
    return redirect("/auth/ui/login?redirect=" + request.url, code=302)

class Kirbi(object):
    @staticmethod
    def liste_apis():
        return [
            "serveurs",
            "ordinateurs",
            "logiciels",
            "licences",
            "ipam",
            "utilisateurs",
            "authentfication",
        ]