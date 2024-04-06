from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
import uuid

class Game:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.games = {}
        return cls._instance

    def create_game(self, element):
        game_id = str(uuid.uuid4())
        server_element = random.choice(["piedra", "papel", "tijera"])
        result = self.calculate_result(element, server_element)
        self.games[game_id] = {
            "elemento": element,
            "elemento_servidor": server_element,
            "resultado": result
        }
        return game_id

    def calculate_result(self, player_element, server_element):
        if player_element == server_element:
            return "empate"
        elif (
            (player_element == "piedra" and server_element == "tijera") or
            (player_element == "tijera" and server_element == "papel") or
            (player_element == "papel" and server_element == "piedra")
        ):
            return "gano"
        else:
            return "perdio"

class GameHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/partidas":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            element = json.loads(post_data.decode("utf-8"))["elemento"]
            game_id = game.create_game(element)
            game_data = {
                "id": game_id,
                "elemento": element,
                "elemento_servidor": game.games[game_id]["elemento_servidor"],
                "resultado": game.games[game_id]["resultado"]
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(game_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == "/partidas":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(game.games).encode("utf-8"))
        elif self.path.startswith("/partidas?resultado="):
            result = self.path.split("=")[1]
            filtered_games = {
                game_id: game_data
                for game_id, game_data in game.games.items()
                if game_data["resultado"] == result 
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(filtered_games).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def main():
    global game
    game = Game()

    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, GameHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()
