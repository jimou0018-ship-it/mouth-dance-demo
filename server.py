import http.server
import socketserver
import os

class Handler(http.server.SimpleHTTPRequestHandler):
    # 显式补齐关键 MIME，避免旧版 Python 缺失导致 wasm/mjs 加载失败
    extensions_map = dict(http.server.SimpleHTTPRequestHandler.extensions_map)
    extensions_map.update({
        '.mjs': 'text/javascript',
        '.wasm': 'application/wasm',
        '.task': 'application/octet-stream',
    })

    def end_headers(self):
        # 允许资源被同源 fetch（wasm instantiateStreaming 需要）
        self.send_header('Cross-Origin-Resource-Policy', 'cross-origin')
        super().end_headers()

    def log_message(self, *args):
        pass

PORT = int(os.environ.get('PORT', '3000'))
Handler.protocol_version = 'HTTP/1.1'
with socketserver.TCPServer(('0.0.0.0', PORT), Handler) as httpd:
    print(f'Serving mouth-dance-demo on 0.0.0.0:{PORT}', flush=True)
    httpd.serve_forever()
