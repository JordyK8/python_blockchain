from flask import Blueprint
from src.controllers.network_node_controller import enx_blockchain

# main blueprint to be registered with application
api = Blueprint('api', __name__)

#register network_nodes with api blueprint
api.register_blueprint(enx_blockchain, url_prefix="/bc")