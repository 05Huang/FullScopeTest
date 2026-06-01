"""
FullScopeTest 代理服务器
前端静态文件 + API 反向代理
"""
import http.server
import urllib.request
import os
import sys

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), 'dist')
BACKEND_URL = 'http://localhost:5211'
PORT = 3000

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def do_GET(self):
        if self.path.startswith('/api/') or self.path.startswith('/health') or self.path == '/metrics':
            self._proxy_request('GET')
        else:
            # SPA fallback: 如果文件不存在，返回 index.html
            file_path = os.path.join(FRONTEND_DIR, self.path.lstrip('/'))
            if not os.path.exists(file_path) or os.path.isdir(file_path):
                if not self.path.startswith('/assets/'):
                    self.path = '/index.html'
            super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/'):
            self._proxy_request('POST')
        else:
            self.send_error(404)

    def do_PUT(self):
        if self.path.startswith('/api/'):
            self._proxy_request('PUT')
        else:
            self.send_error(404)

    def do_DELETE(self):
        if self.path.startswith('/api/'):
            self._proxy_request('DELETE')
        else:
            self.send_error(404)

    def _proxy_request(self, method):
        url = BACKEND_URL + self.path
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        headers = {}
        for key in ['Authorization', 'Content-Type', 'X-Organization-ID']:
            if key in self.headers:
                headers[key] = self.headers[key]

        try:
            req = urllib.request.Request(url, data=body, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=30) as resp:
                resp_body = resp.read()
                self.send_response(resp.status)
                self.send_header('Content-Type', resp.headers.get('Content-Type', 'application/json'))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(resp_body)
        except urllib.error.HTTPError as e:
            resp_body = e.read()
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(resp_body)
        except Exception as e:
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(f'{{"error": "Proxy error: {str(e)}"}}'.encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Organization-ID')
        self.end_headers()

    def log_message(self, format, *args):
        if '/api/' in str(args[0]):
            print(f"[PROXY] {args[0]}")

if __name__ == '__main__':
    print(f"FullScopeTest 代理服务器启动")
    print(f"  前端: http://localhost:{PORT}")
    print(f"  后端: {BACKEND_URL}")
    print(f"  按 Ctrl+C 停止")
    server = http.server.HTTPServer(('0.0.0.0', PORT), ProxyHandler)
    server.serve_forever()
