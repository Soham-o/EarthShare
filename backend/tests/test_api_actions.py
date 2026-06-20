def test_list_actions_requires_auth(client):
    resp = client.get("/api/v1/actions")
    assert resp.status_code == 401


def test_list_actions_returns_catalog(client, registered_user):
    headers, _, _ = registered_user
    resp = client.get("/api/v1/actions", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 6
    assert all(a["completed"] is False for a in body)


def test_complete_action_marks_it_done(client, registered_user):
    headers, _, _ = registered_user
    actions = client.get("/api/v1/actions", headers=headers).json()
    action_id = actions[0]["id"]

    resp = client.post("/api/v1/actions/complete", headers=headers, json={"action_id": action_id})
    assert resp.status_code == 201

    actions_after = client.get("/api/v1/actions", headers=headers).json()
    completed = next(a for a in actions_after if a["id"] == action_id)
    assert completed["completed"] is True


def test_completing_same_action_twice_is_rejected(client, registered_user):
    headers, _, _ = registered_user
    action_id = client.get("/api/v1/actions", headers=headers).json()[0]["id"]
    client.post("/api/v1/actions/complete", headers=headers, json={"action_id": action_id})
    resp = client.post("/api/v1/actions/complete", headers=headers, json={"action_id": action_id})
    assert resp.status_code == 409


def test_completing_unknown_action_returns_404(client, registered_user):
    headers, _, _ = registered_user
    resp = client.post("/api/v1/actions/complete", headers=headers, json={"action_id": "does_not_exist"})
    assert resp.status_code == 404


def test_progress_reflects_completed_actions_and_badges(client, registered_user):
    headers, _, _ = registered_user
    actions = client.get("/api/v1/actions", headers=headers).json()
    client.post("/api/v1/actions/complete", headers=headers, json={"action_id": actions[0]["id"]})

    resp = client.get("/api/v1/progress", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["total_actions_completed"] == 1
    first_step_badge = next(b for b in body["badges"] if b["id"] == "first_step")
    assert first_step_badge["earned"] is True
    champion_badge = next(b for b in body["badges"] if b["id"] == "earthshare_champion")
    assert champion_badge["earned"] is False
