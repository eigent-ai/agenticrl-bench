import socket
import json
import os
import threading
import time
from pathlib import Path
from resource_manager import Resource, ResourceTracker

SOCKET_PATH = "/tmp/resmanager.sock"
SHARED_DIR = "/var/shared_resources"
TEMPLATE_DIR = "/opt/resmanager/templates"


class Broker:
    def __init__(self):
        self.registry = {}
        self.tracker = ResourceTracker()
        self.lock = threading.Lock()
        self.running = False

    def handle_create(self, data):
        name = data["name"]
        owner = data["owner"]
        size = data.get("size", 100)
        max_age = data.get("max_age", 60.0)
        max_size = data.get("max_size", 1048576)

        path = os.path.join(SHARED_DIR, name)
        with open(path, "wb") as f:
            f.write(b"x" * size)

        resource = Resource(
            name=name, path=path, owner=owner,
            size=size, max_age=max_age, max_size=max_size
        )

        with self.lock:
            self.registry[name] = resource
            self.tracker.track(resource)

        return {"status": "ok", "name": name, "path": path}

    def handle_destroy(self, data):
        name = data["name"]
        path = data.get("path", os.path.join(SHARED_DIR, name))

        if path.startswith(TEMPLATE_DIR):
            raise ValueError("Cannot destroy template assets")

        with self.lock:
            if name in self.registry:
                resource = self.registry.pop(name)
                if os.path.exists(resource.path):
                    os.remove(resource.path)
                return {"status": "ok", "name": name}
            else:
                if os.path.exists(path):
                    os.remove(path)
                return {"status": "ok", "name": name, "note": "not in registry"}

    def handle_list(self, data):
        with self.lock:
            return {"status": "ok", "resources": list(self.registry.keys())}

    def handle_cleanup_oldest(self, data):
        with self.lock:
            resource = self.tracker.cleanup_oldest()
            if resource is not None:
                if resource.name in self.registry:
                    del self.registry[resource.name]
                if os.path.exists(resource.path):
                    os.remove(resource.path)
                return {"status": "ok", "cleaned": resource.name}
            return {"status": "ok", "cleaned": None}

    def handle_tracker_count(self, data):
        with self.lock:
            return {"status": "ok", "count": self.tracker.count()}

    def periodic_cleanup(self):
        with self.lock:
            to_remove = []
            for name, resource in self.registry.items():
                if resource.is_expired() and resource.is_oversized():
                    to_remove.append(name)

            for name in to_remove:
                resource = self.registry.pop(name)
                if os.path.exists(resource.path):
                    os.remove(resource.path)

            return {"status": "ok", "cleaned": to_remove}

    def handle_periodic_cleanup(self, data):
        return self.periodic_cleanup()

    def handle_request(self, data):
        action = data.get("action")
        handlers = {
            "create": self.handle_create,
            "destroy": self.handle_destroy,
            "list": self.handle_list,
            "cleanup_oldest": self.handle_cleanup_oldest,
            "periodic_cleanup": self.handle_periodic_cleanup,
            "tracker_count": self.handle_tracker_count,
            "shutdown": lambda d: {"status": "shutdown"},
        }

        handler = handlers.get(action)
        if handler is None:
            return {"status": "error", "message": "Unknown action: {}".format(action)}

        try:
            return handler(data)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def start(self):
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)

        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.bind(SOCKET_PATH)
        self.server.listen(5)
        self.server.settimeout(1.0)
        self.running = True

        while self.running:
            try:
                conn, _ = self.server.accept()
            except socket.timeout:
                continue

            threading.Thread(
                target=self._handle_conn, args=(conn,), daemon=True
            ).start()

        self.server.close()
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)

    def _handle_conn(self, conn):
        try:
            data = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
                try:
                    json.loads(data.decode())
                    break
                except json.JSONDecodeError:
                    continue

            if data:
                request = json.loads(data.decode())
                response = self.handle_request(request)

                if response.get("status") == "shutdown":
                    self.running = False

                conn.sendall(json.dumps(response).encode())
        except Exception as e:
            try:
                conn.sendall(
                    json.dumps({"status": "error", "message": str(e)}).encode()
                )
            except Exception:
                pass
        finally:
            conn.close()


if __name__ == "__main__":
    broker = Broker()
    broker.start()
