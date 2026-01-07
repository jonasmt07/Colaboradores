from flask import Blueprint

# Cria o Blueprint 'auth'. 
# O template_folder indica onde estão os HTMLs específicos deste módulo (opcional, mas organizado).
auth_bp = Blueprint('auth', __name__)

from . import routes