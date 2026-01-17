from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Album

album_bp = Blueprint("album_bp", __name__, url_prefix="/albums")
 

@album_bp.route("/create", methods=["POST"])
@jwt_required()
def create_album():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not name:
        return jsonify({"msg": "Album name is required"}), 400

    current_user_id = int(get_jwt_identity())

    new_album = Album(
        name=name,
        description=description,
        user_id=current_user_id
    )
    db.session.add(new_album)
    db.session.commit()

    return jsonify({"msg": "Album created successfully", "album": {"id": new_album.id, "name": new_album.name}}), 201


@album_bp.route("/myalbums", methods=["GET"])
@jwt_required()
def my_albums():
    current_user_id = int(get_jwt_identity())
    albums = Album.query.filter_by(user_id=current_user_id).all()
    result = [{"id": a.id, "name": a.name, "description": a.description} for a in albums]
    return jsonify(result), 200
