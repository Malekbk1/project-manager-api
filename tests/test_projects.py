def test_create_project_without_token(client):
    response = client.post("/projects", json={
        "title": "Mon projet"
    })
    assert response.status_code == 401


def test_create_project_success(client, auth_headers):
    response = client.post("/projects",
        json={"title": "Mon projet", "description": "Test"},
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Mon projet"


def test_get_projects(client, auth_headers):
    client.post("/projects",
        json={"title": "Projet 1"},
        headers=auth_headers
    )
    client.post("/projects",
        json={"title": "Projet 2"},
        headers=auth_headers
    )
    response = client.get("/projects", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


def test_update_project(client, auth_headers):
    response = client.post("/projects",
        json={"title": "Ancien titre"},
        headers=auth_headers
    )
    project_id = response.get_json()["id"]
    response = client.put(f"/projects/{project_id}",
        json={"title": "Nouveau titre"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.get_json()["title"] == "Nouveau titre"


def test_delete_project(client, auth_headers):
    response = client.post("/projects",
        json={"title": "A supprimer"},
        headers=auth_headers
    )
    project_id = response.get_json()["id"]
    response = client.delete(f"/projects/{project_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    response = client.get("/projects", headers=auth_headers)
    assert len(response.get_json()) == 0