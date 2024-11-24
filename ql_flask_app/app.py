from flask import Flask, render_template
from swap import swap_bp
from bond import bond_bp
from swaption import swaption_bp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Register Blueprints
app.register_blueprint(swap_bp)
app.register_blueprint(bond_bp)
app.register_blueprint(swaption_bp)

if __name__ == '__main__':
    app.run(debug=True)