from flask import Blueprint,request, jsonify
from flask_jwt_extended import jwt_required ,get_jwt_identity
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
    

    if not title or not description or not visibility:
        return jsonify({"msg":"ALL FIELDS ARE REQUIRED"}),400
    
    current_user_id = get_jwt_identity()

    new_photo=Photo(
        title=title,
        description=description,
        visibility=visibility,
        user_id=current_user_id,
        image_url="placeholder"
    )

    db.session.add(new_photo)
    db.session.commit()

    return jsonify ({"msg":"PHOTO ADDED SUCCESSFULLY"}),200