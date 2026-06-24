#!/usr/bin/env python3
"""No-cache static server for the Eastern Cape Boer War map (port 8090)."""
import http.server, socketserver, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = 8090

class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        super().end_headers()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), H) as httpd:
    print(f"serving Eastern Cape map on :{PORT}", flush=True)
    httpd.serve_forever()
