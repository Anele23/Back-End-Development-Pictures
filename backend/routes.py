from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():

    return data
######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):

    if request.method == "GET":
        for image_data in data:
                if image_data["id"] == id:
                    return image_data
                
        resp = make_response({'message': f"Person not found with id {id}"})
        resp.status_code = 404
        return resp

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_image = request.json
    is_duplicate = False
    if not new_image:
        return {"Message": "Invalid input parameter"}, 422

    # Check for duplicates
    for image in data:
        if int(image['id']) == int(new_image['id']):
            is_duplicate = True
            return {"Message": f"picture with id {new_image['id']} already present"}, 302

    if not is_duplicate:
        try:
            data.append(new_image)
        except Exception as e:
            return {"Message": f"Error occurred: {str(e)}"}, 500

        resp = make_response({
            'id': new_image['id'],
            'pic_url': new_image['pic_url'],
            'event_country': new_image['event_country'],
            'event_state': new_image['event_state'],
            'event_city': new_image['event_city'],
            'event_date': new_image['event_date']
        })
        resp.status_code = 201
        return resp
            
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_image = request.json

    for index, image in enumerate(data):
        if image["id"] == id:
            data[index] = new_image
            return image, 201

    return {"message": "picture not found"}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for image in data:
        if image["id"] == id:
            data.remove(image)
            return {"message":f"{id}"}, 204
    return {"message": "image not found"}, 404
