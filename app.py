from http.server import *
from random import randint

sessions = {}

class SessionHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/login": self.login,
            "/logout": self.logout,
            "/": self.home
        }
        self.cookie = None
        try:
            response = 200
            cookies = self.parse_cookies(self.headers["Cookie"])
            if "sid" in cookies:
                self.user = cookies["sid"] if (cookies["sid"] in sessions) else False
            else:
                self.user = False
            content = routes[self.path]()
        except:
            response = 404
            content = "Not Found"
        
        self.send_response(response)
        self.send_header('Content-type','text/html')

        if self.cookie:
            self.send_header('Set-Cookie', self.cookie)

        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))
        return
    
    def home(self):
        return "Welcome User!" if self.user else "Welcome Stranger!"

    def login(self):
        # Password would normally be checked here
        sid = self.generate_sid()
        self.cookie = "sid={}".format(sid)
        sessions[sid] = {"username", "useragent","ip address","expiry"}
        return "Logged In"

    def logout(self):
        if not self.user:
            return "Can't Log Out: No User Logged In"
        self.cookie = "sid="
        del sessions[self.user]
        return "Logged Out"

    def generate_sid(self):
        return "".join(str(randint(1,9)) for _ in range(100))

    def parse_cookies(self, cookie_list):
        return dict(((c.split("=")) for c in cookie_list.split(";"))) if cookie_list else {}

address = ('', 8000)
handler = SessionHandler
server = HTTPServer(address, handler)

server.serve_forever()