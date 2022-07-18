from .all_routes import lobby
from .all_routes import user_interface
from .all_routes import file_save_interface
from .all_routes import passport
from .all_routes import admin_interface
from .all_routes import golden_mark


def global_routes_init(app):
    app.register_blueprint(lobby.blueprint)
    app.register_blueprint(user_interface.blueprint)
    app.register_blueprint(file_save_interface.blueprint)
    app.register_blueprint(passport.blueprint)
    app.register_blueprint(admin_interface.blueprint)
    app.register_blueprint(golden_mark.blueprint)