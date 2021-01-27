# Pulled from https://stackoverflow.com/questions/48308487/can-python-m-http-server-be-configured-to-handle-concurrent-requests
import sys
import socketserver
import http.server


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

port = 8000
if (len(sys.argv) > 1):
    port = int(sys.argv[1])
server = ThreadedHTTPServer(('', port), http.server.SimpleHTTPRequestHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass