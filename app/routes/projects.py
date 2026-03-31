from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Project, User

projects_bp = Blueprint("projects", __name__)

@projects_bp.route("", methods=["GET"])
@jwt_required()
def get_projects():
    user_id = get_jwt_identity()
    projects = Project.query.filter_by(user_id=user_id).all()
    return jsonify([p.to_dict() for p in projects]), 200

@projects_bp.route("", methods=["POST"])
@jwt_required()
def create_project():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400

    project = Project(title=data["title"], description=data.get("description",""), user_id=user_id)
    db.session.add(project)
    db.session.commit()

    return jsonify({"message": "Project created successfully", "project": project.to_dict()}), 201

@projects_bp.route("/<int:project_id>", methods=["PUT"])
@jwt_required()
def update_project(project_id):
    user_id = get_jwt_identity()
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()

    if not project:
        return jsonify({"error": "Project not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    project.title = data.get("title", project.title)
    project.description = data.get("description", project.description)
    project.status = data.get("status", project.status)

    db.session.commit()
    return jsonify({"message": "Project updated successfully", "project": project.to_dict()}), 200

@projects_bp.route("/<int:project_id>", methods=["DELETE"])
@jwt_required()     
def delete_project(project_id):
    user_id = get_jwt_identity()
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()

    if not project:
        return jsonify({"error": "Project not found"}), 404

    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted successfully"}), 200