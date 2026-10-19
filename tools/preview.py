"""Loopback-only fixture preview using the shipped SDK and the author's real files."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
import re
import signal
from pathlib import Path
from urllib.parse import unquote, urlsplit

from extension_tools import ROOT, path_in, read_json
from retromao import check_source


def make_server(source, port, fixtures):
    source = Path(source).resolve()
    kind, manifest = check_source(source)
    data = {"kind": kind, "manifest": manifest, "fixtures": read_json(fixtures)}
    if kind == "PLATFORM":
        data["platform"] = read_json(source / "platform.json")
    if kind == "LANGUAGE":
        data["source"] = read_json(source.parent / "zh-Hans.json")
        data["context"] = read_json(ROOT / "contracts/message-context.json")

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            route = unquote(urlsplit(self.path).path)
            try:
                if route == "/__preview/data.json":
                    return self.respond(json.dumps(data, ensure_ascii=False).encode("utf-8"), "application/json")
                if route.startswith("/plugin/") and kind == "SCRIPT":
                    target = path_in(source, route.removeprefix("/plugin/"))
                    content = target.read_bytes()
                    if target.suffix == ".html":
                        inject = '<script src="/__preview/mock-host.js"></script><script src="/__retromao/retromao.js"></script>'
                        content = content.decode("utf-8")
                        # The bridge must exist before any author script runs.
                        head = re.search(r"<head(?:\s[^>]*)?>", content, flags=re.I)
                        content = (content[:head.end()] + inject + content[head.end():] if head else inject + content).encode("utf-8")
                    return self.respond(content, mimetypes.guess_type(target)[0] or "application/octet-stream")
                if route.startswith("/__retromao/"):
                    target = path_in(ROOT / "sdk/runtime", route.removeprefix("/__retromao/"))
                elif route.startswith("/__preview/"):
                    target = path_in(ROOT / "tools/preview", route.removeprefix("/__preview/"))
                elif route == "/":
                    target = ROOT / "tools/preview/index.html"
                else:
                    self.send_error(404)
                    return
                self.respond(target.read_bytes(), mimetypes.guess_type(target)[0] or "application/octet-stream")
            except (ValueError, OSError):
                self.send_error(404)

        def respond(self, content, content_type):
            self.send_response(200)
            self.send_header("Content-Type", content_type + ("; charset=utf-8" if content_type.startswith("text/") or content_type in ("application/json", "application/javascript") else ""))
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(content)

        def log_message(self, *_):
            pass

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def serve(source, port, fixtures):
    server = make_server(source, port, fixtures)
    def stop(*_):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, stop)
    print(f"Preview: http://127.0.0.1:{server.server_port}/ | Ctrl+C: stop", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
