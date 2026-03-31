from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Task, Project

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    project_id = request.args.get("project_id")

    if not project_id:
        return jsonify({"error": "project_id is required"}), 400

    project = Project.query.filter_by(
        id=project_id,
        user_id=user_id
    ).first()

    if not project:
        return jsonify({"error": "project not found"}), 404

    tasks = Task.query.filter_by(project_id=project_id).all()
    return jsonify([t.to_dict() for t in tasks]), 200


@tasks_bp.route("", methods=["POST"])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or "title" not in data or "project_id" not in data:
        return jsonify({"error": "title and project_id are required"}), 400

    project = Project.query.filter_by(
        id=data["project_id"],
        user_id=user_id
    ).first()

    if not project:
        return jsonify({"error": "project not found"}), 404

    task = Task(
        title=data["title"],
        description=data.get("description", ""),
        priority=data.get("priority", "medium"),
        project_id=data["project_id"]
    )

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "task not found"}), 404

    project = Project.query.filter_by(
        id=task.project_id,
        user_id=user_id
    ).first()

    if not project:
        return jsonify({"error": "access denied"}), 403

    data = request.get_json()
    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "status" in data:
        task.status = data["status"]
    if "priority" in data:
        task.priority = data["priority"]

    db.session.commit()
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "task not found"}), 404

    project = Project.query.filter_by(
        id=task.project_id,
        user_id=user_id
    ).first()

    if not project:
        return jsonify({"error": "access denied"}), 403

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "task deleted"}), 200