from DBschema import UserSchema
from bson.objectid import ObjectId
from bson import json_util
import json
from flask import jsonify, request


class UserControler:
    def __init__(self, db, app):
        self.userschema = UserSchema()
        self.db = db
        self.app = app
        self.registerRoute()

    def getApp(self):
        return self.app

    def registerRoute(self):
        self.app.add_url_rule(
            "/", view_func=self.index, methods=["GET"], strict_slashes=False
        )
        self.app.add_url_rule(
            "/users", view_func=self.allUser, methods=["GET"], strict_slashes=False
        )
        self.app.add_url_rule(
            "/users/<userId>",
            view_func=self.findUser,
            methods=["GET"],
            strict_slashes=False,
        )
        self.app.add_url_rule(
            "/users", view_func=self.addUser, methods=["POST"], strict_slashes=False
        )
        self.app.add_url_rule(
            "/users/<userId>",
            view_func=self.updateUser,
            methods=["PUT"],
            strict_slashes=False,
        )
        self.app.add_url_rule(
            "/users/<userId>",
            view_func=self.deleteUser,
            methods=["DELETE"],
            strict_slashes=False,
        )

    def index(self):
        return """
            The application should provide the following REST API endpoints:<br>
            GET /users - Returns a list of all users.<br>
            GET /users/<id> - Returns the user with the specified ID.<br>
            POST /users - Creates a new user with the specified data.<br>
            PUT /users/<id> - Updates the user with the specified ID with the new data.<br>
            DELETE /users/<id> - Deletes the user with the specified ID.

        """

    def allUser(self):
        users = self.db.users.find()
        return json.loads(json_util.dumps(users))

    def findUser(self, userId):
        print(userId)
        id = str(userId)
        user = self.db.users.find_one({"_id": ObjectId(id)})
        if user == None:
            return jsonify(f"No user found on ID {userId}")
        return json.loads(json_util.dumps(user))

    def addUser(self):
        data = request.json

        # Validation of data
        try:
            self.userschema.load(data)
        except Exception as e:
            return jsonify(f"{e}")

        # Validation of uniqueness of email.
        uniqueuser = self.db.users.find_one({"email": data["email"]})
        if uniqueuser != None:
            return "Email already registered."

        _id = self.db.users.insert_one(data).inserted_id
        return jsonify(f"User Successfully added on ID:{_id}")

    def updateUser(self, userId):
        # validating user exists or not
        user = self.db.users.find_one({"_id": ObjectId(str(userId))})
        if user == None:
            return jsonify(f"No user found on ID {userId}")

        data = request.json
        # Validation of data
        try:
            self.userschema.load(data, partial=True)
        except Exception as e:
            return jsonify(f"{e}")
        result = self.db.users.update_one(
            {"_id": ObjectId(str(userId))}, {"$set": data}
        )
        user = self.db.users.find_one({"_id": ObjectId(str(userId))})
        return json.loads(json_util.dumps(user))

    def deleteUser(self, userId):
        delres = self.db.users.find_one_and_delete({"_id": ObjectId(str(userId))})
        if delres == None:
            return jsonify(f"No user found on ID {userId}")
        return f"Successfully deleted user on ID : {userId}"
