from flask import Blueprint, render_template

swaption_bp = Blueprint('swaption', __name__)

@swaption_bp.route('/swaption')
def swaption():
    return render_template('swaption.html')