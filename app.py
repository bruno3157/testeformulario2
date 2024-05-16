from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

USUARIO_FIXO = 'usuario'
SENHA_FIXA = 'senha'

# Configuração do banco de dados SQLite
DATABASE = 'banco_de_dados.db'

def conectar_bd():
    return sqlite3.connect(DATABASE)

def criar_tabela():
    with conectar_bd() as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nome TEXT, telefone TEXT)")
        con.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    usuario = request.form['usuario']
    senha = request.form['senha']

    if usuario == USUARIO_FIXO and senha == SENHA_FIXA:
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

        with conectar_bd() as con:
            cur = con.cursor()
            cur.execute("INSERT INTO usuarios (nome, telefone) VALUES (?, ?)", (nome, telefone))
            con.commit()

        return 'Dados enviados com sucesso!'

    return render_template("enviar_dados.html")

if __name__ == '__main__':
    criar_tabela()  # Certificar-se de que a tabela foi criada antes de iniciar o aplicativo Flask
    app.run(debug=True)
