from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Empresa, Colaborador, EPI
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_teste'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ehs_concet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# --- ROTAS DE NAVEGAÇÃO ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'adm.2026':
            return redirect(url_for('dashboard'))
        flash('Usuário ou senha incorretos!')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# --- ROTAS DE CADASTRO COM LISTAGEM ---

@app.route('/cadastro-usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        novo_user = User(
            nome=request.form.get('nome'),
            username=request.form.get('username'),
            email=request.form.get('email'),
            role=request.form.get('role'),
            ativo=True
        )
        db.session.add(novo_user)
        db.session.commit()
        return redirect(url_for('cadastro_usuario'))
    
    usuarios = User.query.all()
    return render_template('cadastro-usuarios.html', usuarios=usuarios)

@app.route('/cadastro-empresa', methods=['GET', 'POST'])
def cadastro_empresa():
    if request.method == 'POST':
        nova_empresa = Empresa(
            razao_social=request.form.get('razao_social'),
            nome_fantasia=request.form.get('nome_fantasia'),
            identificacao=request.form.get('identificacao'),
            cnae=request.form.get('cnae'),
            grau_risco=request.form.get('grau_risco'),
            email=request.form.get('email')
        )
        db.session.add(nova_empresa)
        db.session.commit()
        return redirect(url_for('cadastro_empresa'))
    
    empresas = Empresa.query.all()
    return render_template('cadastro-empresa.html', empresas=empresas)

@app.route('/cadastro-colaborador', methods=['GET', 'POST'])
def cadastro_colaborador():
    if request.method == 'POST':
        novo_colab = Colaborador(
            matricula=request.form.get('matricula'),
            nome=request.form.get('nome'),
            cpf=request.form.get('cpf'),
            cargo=request.form.get('cargo'),
            setor=request.form.get('setor'),
            status='Ativo'
        )
        db.session.add(novo_colab)
        db.session.commit()
        return redirect(url_for('cadastro_colaborador'))
    
    colaboradores = Colaborador.query.all()
    return render_template('cadastro-colaboradores.html', colaboradores=colaboradores)

# --- ROTA DE STATUS (Exemplo para desativar qualquer um) ---
@app.route('/alternar-status/<string:tipo>/<int:id>')
def alternar_status(tipo, id):
    # Lógica simples para mudar o status de qualquer item (EPI, Usuario, etc)
    # Exemplo: obj = User.query.get(id); obj.ativo = not obj.ativo; db.session.commit()
    flash(f'Status do item {id} atualizado!')
    return redirect(request.referrer)

if __name__ == '__main__':
    app.run(debug=True)
