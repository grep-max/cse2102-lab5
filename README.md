# Lab 5: REST Publish-Subscribe System

A Flask REST server (`publisher.py`) that stores subscribers and notifies them when the published subject changes. Notifications are print statements in the server terminal.

## Files

| File | Purpose |
|---|---|
| `publisher.py` | The Flask publisher server |
| `test_publisher.py` | Pytest unit tests for every endpoint |
| `requirements.txt` | Python dependencies (`flask`, `pytest`) |
| `.devcontainer/devcontainer.json` | Codespace setup: Python 3.12, installs dependencies, forwards port 5000 |

## Endpoints

| Method | Path | Body (JSON) | Description |
|---|---|---|---|
| `POST` | `/add-subscriber` | `{"name": "...", "URI": "..."}` | Add (or replace) a subscriber |
| `DELETE` | `/delete-subscriber` | `{"name": "..."}` | Delete a subscriber by name (404 if unknown) |
| `GET` | `/list-subscribers` | — | List all subscribers and their URLs |
| `POST` | `/update-and-notify` | `{"subject-update": "..."}` | Update the subject and notify every subscriber |
| `GET` | `/subject` | — | Show the current subject |

Missing fields return `400` with an error message.

## Setup

In a GitHub Codespace the dependencies install automatically. Otherwise:

```bash
pip install -r requirements.txt
```

## Run the tests

```bash
python -m pytest -v
```

## Run the server (terminal 1)

```bash
python publisher.py
```

## Try it with curl (terminal 2)

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"Grace","URI":"http://grace.example.com"}' http://localhost:5000/add-subscriber
curl -X POST -H "Content-Type: application/json" -d '{"name":"Ada","URI":"http://ada.example.com"}' http://localhost:5000/add-subscriber
curl -X POST -H "Content-Type: application/json" -d '{"name":"Alan","URI":"http://example.com"}' http://localhost:5000/add-subscriber

curl http://localhost:5000/list-subscribers

curl -X DELETE -H "Content-Type: application/json" -d '{"name":"Grace"}' http://localhost:5000/delete-subscriber
curl -X DELETE -H "Content-Type: application/json" -d '{"name":"Bob"}' http://localhost:5000/delete-subscriber

curl -X POST -H "Content-Type: application/json" -d '{"subject-update":"buy IBM"}' http://localhost:5000/update-and-notify
```

After the last command, terminal 1 prints a `Notifying <name> at <URI> of the new subject: buy IBM` line for each remaining subscriber.

Note: use `http://localhost:5000`, not `https://` — the local Flask dev server does not serve HTTPS.

## Calling the Codespace from your own computer

In the Codespace **Ports** tab, right-click port 5000 → **Port Visibility → Public**, then copy the forwarded address (e.g. `https://<name>-5000.app.github.dev`):

```bash
curl -X POST -H "Content-Type: application/json" -d '{"subject-update":"buy IBM"}' https://<name>-5000.app.github.dev/update-and-notify
```

On Windows PowerShell use `curl.exe` instead of `curl`.
