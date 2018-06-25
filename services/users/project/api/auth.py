from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_

from project.api.models import User
from project import db, bcrypt

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint('/auth/register', methods=['POST'])
def register_user():
    post_data = request.get_json()
