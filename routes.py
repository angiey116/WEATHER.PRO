# routes.py

def register_routes(app):

    @app.get("/")
    def home():
        return "<h1>milestone 2</h1><p>Flask server is running.</p>"

    @app.post("/items")
    def create_item():
        return "CREATE: POST /items"

    @app.get("/items")
    def list_items():
        return "READ ALL: GET /items"

    @app.get("/items/<int:item_id>")
    def get_item(item_id):
        return f"READ ONE: GET /items/{item_id}"

    @app.put("/items/<int:item_id>")
    def update_item(item_id):
        return f"UPDATE: PUT /items/{item_id}"

    @app.delete("/items/<int:item_id>")
    def delete_item(item_id):
        return f"DELETE: DELETE /items/{item_id}"