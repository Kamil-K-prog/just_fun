from .all_interface import lobby
from .all_interface import web



def global_interface_init(app):
    app.register_blueprint(lobby.blueprint)
    app.register_blueprint(web.blueprint)
