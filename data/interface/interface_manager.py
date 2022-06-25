from .all_interface import lobby



def global_interface_init(app):
    app.register_blueprint(lobby.blueprint)