from flask import render_template
from app.models import Employee, db
from . import main_bp

@main_bp.route('/')
def home():
    """
    Rota principal pública. Exibe lista de colaboradores para consulta.
    """
    employees = Employee.query.all()
    
    # Lógica para filtrar unidades (Distinct)
    # TODO: Se o sistema crescer, mover essa lógica para um Service ou Manager
    units_query = db.session.query(Employee.unidade).distinct().order_by(Employee.unidade).all()
    units = [u[0] for u in units_query if u[0]]
    
    return render_template('main/home.html', employees=employees, units=units)