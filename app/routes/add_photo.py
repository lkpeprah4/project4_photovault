from flask import Blueprint,request, jsonify
from flask_jwt_extended import jwt_required ,get_jwt_identity
from cloudinary.uploader import upload
from ..models import db, Photo

photo_bp=Blueprint("photo_bp", __name__ ,url_prefix="/photos")

#/photos/addphoto
@photo_bp.route('/addphoto', methods=["POST"])
@jwt_required()
def addphoto():
    data=request.get_json()
    title=data.get("title")
    description=data.get("description")
    visibility=data.get("visibility")
    image_file= request.files["image"]
    
    if "image" not in request.files:
        return jsonify({"msg":"No image provided"}),400

    if not title or not description or not visibility:
        return jsonify({"msg":"ALL FIELDS ARE REQUIRED"}),400
    
    current_user_id = int(get_jwt_identity())

    upload_photo= upload(image_file)
    image_url=upload_photo.get("secure_url")

    new_photo=Photo(
        title=title,
        description=description,
        visibility=visibility,
        user_id=current_user_id,
        image_url=image_url
    )

    db.session.add(new_photo)
    db.session.commit()

    return jsonify ({"msg":"PHOTO ADDED SUCCESSFULLY" ,"image_url":image_url}),200