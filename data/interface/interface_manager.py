from .all_interface import название



def global_interface_init(app):
    app.register_blueprint(название.blueprint)