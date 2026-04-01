def test_create_task_without_token(client):
    response = client.post("/tasks", json={
        "title": "Ma tâche",
        "project_id": 1
    })
    assert response.status_code == 401


def test_create_task_success(client, auth_headers):
    project = client.post("/projects",
        json={"title": "Mon projet"},
        headers=auth_headers
    ).get_json()

    response = client.post("/tasks",
        json={
            "title": "Ma tâche",
            "project_id": project["id"],
            "priority": "high"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Ma tâche"
    assert data["priority"] == "high"
    assert data["status"] == "todo"


def test_get_tasks(client, auth_headers):
    project = client.post("/projects",
        json={"title": "Mon projet"},
        headers=auth_headers
    ).get_json()

    client.post("/tasks",
        json={"title": "Tâche 1", "project_id": project["id"]},
        headers=auth_headers
    )
    client.post("/tasks",
        json={"title": "Tâche 2", "project_id": project["id"]},
        headers=auth_headers
    )

    response = client.get(
        f"/tasks?project_id={project['id']}",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_update_task_status(client, auth_headers):
    project = client.post("/projects",
        json={"title": "Mon projet"},
        headers=auth_headers
    ).get_json()

    task = client.post("/tasks",
        json={"title": "Ma tâche", "project_id": project["id"]},
        headers=auth_headers
    ).get_json()

    response = client.put(f"/tasks/{task['id']}",
        json={"status": "done"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.get_json()["status"] == "done"