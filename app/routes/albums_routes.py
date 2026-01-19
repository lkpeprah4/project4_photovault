from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Album, Photo

album_bp = Blueprint("album_bp", __name__, url_prefix="/albums")


# CREATE ALBUM
@album_bp.route("/create", methods=["POST"])
@jwt_required()
def create_album():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"msg": "Album name is required"}), 400

    user_id = int(get_jwt_identity())

    album = Album(name=name, user_id=user_id)
    db.session.add(album)
    db.session.commit()

    return jsonify({"msg": "Album created", "album_id": album.id}), 201


# ADD PHOTO TO ALBUM
@album_bp.route("/<int:album_id>/add-photo/<int:photo_id>", methods=["POST"])
@jwt_required()
def add_photo_to_album(album_id, photo_id):
    user_id = int(get_jwt_identity())

    album = Album.query.get_or_404(album_id)
    photo = Photo.query.get_or_404(photo_id)

    if album.user_id != user_id or photo.user_id != user_id:
        return jsonify({"msg": "Not authorized"}), 403

    photo.album_id = album.id
    db.session.commit()

    return jsonify({"msg": "Photo added to album"}), 200


# VIEW ALBUMS
@album_bp.route("/my-albums", methods=["GET"])
@jwt_required()
def my_albums():
    user_id = int(get_jwt_identity())
    albums = Album.query.filter_by(user_id=user_id).all()

    result = []
    for a in albums:
        result.append({
            "id": a.id,
            "name": a.name,
            "photo_count": len(a.photos)
        })

    return jsonify(result), 200
  
# VIEW PHOTOS IN ALBUM
@album_bp.route("/<int:album_id>/photos", methods=["GET"])
@jwt_required()
def view_album_photos(album_id):
    user_id = get_jwt_identity()
    album = Album.query.get(album_id)

    if album.user_id != user_id:
        return jsonify({"msg": "Not authorized to view this album"}), 403

    photos = Photo.query.filter_by(album_id=album.id).all()
    result = []
    for p in photos:
        result.append({
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "image_url": p.image_url,
            "visibility": p.visibility
        })

    return jsonify(result), 200


# REMOVE PHOTO FROM ALBUM
@album_bp.route("/<int:album_id>/remove-photo/<int:photo_id>", methods=["DELETE"])
@jwt_required()
def remove_photo_from_album(album_id, photo_id):
    user_id = int(get_jwt_identity())
    album = Album.query.get_or_404(album_id)
    photo = Photo.query.get_or_404(photo_id)

    if album.user_id != user_id or photo.user_id != user_id:
        return jsonify({"msg": "Not authorized"}), 403
    
    photo.album_id = None
    db.session.commit()

    return jsonify({"msg": "Photo removed from album"}), 200
