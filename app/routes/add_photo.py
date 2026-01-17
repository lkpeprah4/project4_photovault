from flask import Blueprint,request, jsonify
from flask_jwt_extended import jwt_required ,get_jwt_identity
from cloudinary.uploader import upload
from ..models import db, Photo, User

photo_bp=Blueprint("photo_bp", __name__ ,url_prefix="/photos")

#/photos/addphoto
@photo_bp.route('/addphoto', methods=["POST"])
@jwt_required()
def addphoto():
 
    title = request.form.get("title")
    description = request.form.get("description")
    visibility = request.form.get("visibility")
    image_file = request.files.get("image")

    
    if not image_file:
        return jsonify({"msg": "No image file provided. Make sure you upload an image using form-data."}), 400

    
    missing_fields = []
    if not title:
        missing_fields.append("title")
    if not description:
        missing_fields.append("description")
    if not visibility:
        missing_fields.append("visibility")

    if missing_fields:
        return jsonify({"msg": "Missing fields", "fields": missing_fields}), 400

    # 3️⃣ Validate visibility
    if visibility not in ["public", "private"]:
        return jsonify({"msg": "Invalid visibility. Must be 'public' or 'private'."}), 400

    # 4️⃣ Get user
    current_user_id = get_jwt_identity()

    # 5️⃣ Upload image to Cloudinary
    try:
        upload_result = upload(image_file)
        image_url = upload_result.get("secure_url")
    except Exception as e:
        return jsonify({"msg": "Failed to upload image", "error": str(e)}), 500

    # 6️⃣ Save photo in DB
    new_photo = Photo(
        title=title,
        description=description,
        visibility=visibility,
        user_id=current_user_id,
        image_url=image_url
    )

    db.session.add(new_photo)
    db.session.commit()

    return jsonify({
        "msg": "Photo added successfully",
        "image_url": image_url,
        "photo_id": new_photo.id
    }), 200


@photo_bp.route("/public", methods=["GET"])
def get_public_photos():
    photos = Photo.query.filter_by(visibility="public").all()

    result = []
    for p in photos:
        result.append({
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "image_url": p.image_url,
            "owner_id": p.user_id
        })

    return jsonify(result), 200

@photo_bp.route("/myphotos", methods=["GET"])
@jwt_required()
def my_photos():
    current_user_id = int(get_jwt_identity())

    photos = Photo.query.filter_by(user_id=current_user_id).all()

    result = []
    for p in photos:
        result.append({
            "id": p.id,
            "title": p.title,
            "visibility": p.visibility,
            "image_url": p.image_url
        })

    return jsonify(result), 200


@photo_bp.route("/<int:photo_id>", methods=["DELETE"])
@jwt_required()
def delete_photo(photo_id):
    current_user_id = int(get_jwt_identity())

    photo = Photo.query.get_or_404(photo_id)
    user = User.query.get(current_user_id)

    if photo.user_id != current_user_id and user.role != "admin":
        return jsonify({"msg": "You are not allowed to delete this photo"}), 403

    db.session.delete(photo)
    db.session.commit()

    return jsonify({"msg": "Photo deleted successfully"}), 200
