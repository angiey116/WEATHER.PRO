def register_routes(app):
    @app.get("/")
    def home():
        return "<h1>milestone 2</h1><p>Flask server is running.</p>"

    @app.post("/items")
    def create_item():
        return "create items"

    @app.get("/items")
    def list_items():
        return "read all items"

    @app.get("/items/<int:item_id>")
    def get_item(item_id):
        return f"read one: get /items"

    @app.put("/items/<int:item_id>")
    def update_item(item_id):
        return f"update items"
    @app.delete("/items/<int:item_id>")
    def delete_item(item_id):
        return f"delete items"