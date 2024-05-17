from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Substitua pela sua chave secreta

# Configurações do banco de dados MySQL no Railway
db_config = {
    'user': 'root',
    'password': 'fzwiXJlnSSkEECUNjOHqiDKlfKvvmGri',
    'host': 'roundhouse.proxy.rlwy.net',
    'database': 'railway',
    'port': '47387',
}

def conectar_bd():
    return mysql.connector.connect(**db_config)

def criar_tabela():
    con = conectar_bd()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bdform (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            telefone VARCHAR(255) NOT NULL
        )
    """)
    con.commit()
    con.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    usuario = request.form['usuario']
    senha = request.form['senha']

    if usuario == 'usuario_fixo' and senha == 'senha_fixa':
        session['usuario'] = usuario
        return redirect(url_for('pagina_protegida'))
    else:
        return 'Credenciais inválidas. Por favor, tente novamente.'

@app.route("/pagina-protegida")
def pagina_protegida():
    if 'usuario' in session:
        return 'Bem-vindo à página protegida!'
    else:
        return redirect(url_for('index'))

@app.route("/enviar-dados", methods=['GET', 'POST'])
def enviar_dados():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']

        con = conectar_bd()
        cur = con.cursor()
        cur.execute("INSERT INTO bdform (nome, telefone) VALUES (%s, %s)", (nome, telefone))
        con.commit()
        con.close()

        return 'Dados enviados com sucesso!'

    return render_template("enviar_dados.html")

if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)
