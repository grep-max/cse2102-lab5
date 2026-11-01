# Lab 5: What I Did

I built a REST publish-subscribe server in Python Flask, starting from the provided `publisher.py` example.

**Publisher state.** All subscribers live in the publisher server in a dictionary that maps each subscriber's name to its URL. The current subject is a module-level variable.

**Endpoints.**
- `POST /add-subscriber` takes a name and a URL and stores the subscriber. A second add with the same name replaces that subscriber's URL.
- `DELETE /delete-subscriber` takes only a name and removes that subscriber. An unknown name, such as `Bob`, returns 404.
- `GET /list-subscribers` returns every subscriber with its URL as JSON, and also prints them on the server.
- `POST /update-and-notify` updates the published subject and notifies every subscriber with a print statement on the backend. The response lists who was notified.
- I added `GET /subject` to read the current subject back.

**Fixes to the starter code.** In the example, `update-and-notify` assigned `subject` without `global`, so the stored subject never changed. I fixed that. I also added input validation: a request with a missing field or a body that is not JSON returns 400 instead of crashing the server.

**Testing.** `test_publisher.py` has 12 pytest unit tests. They use Flask's test client and cover adding, listing, deleting (including an unknown name), notifying (checking the printed notifications), confirming that a deleted subscriber is no longer notified, and rejecting bad input. A fixture resets the server's state before each test. I also tested by hand: I ran the server in one Codespace terminal and sent curl commands from a second terminal.

**Codespace.** The `.devcontainer` configuration sets up Python 3.12, installs Flask and pytest automatically, and forwards port 5000. With the port set to Public, I can also call the server from my own computer.
