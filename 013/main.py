

from flask import Flask, render_template, redirect, request, flash, send_from_directory
import json
import ast
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'IGORKEVEN'

logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')

@app.route('/adm')
def adm():
    if logado == True:
        with open('usuarios.json') as usuariosTemp:
            usuarios = json.load(usuariosTemp)
            
        return render_template("administrador.html",usuarios=usuarios)
    if logado == False:
        return redirect('/')

@app.route('/usuarios')
def usuarios():
    if logado == True:
        arquivo = []
        for documento in os.listdir('013/arquivos'):
            arquivo.append(documento)

        return render_template("usuarios.html", arquivos=arquivo)
    else:
        return redirect('/')



@app.route('/login', methods=['POST'])
def login():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    with open('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)
        cont = 0
        for usuario in usuarios:
            cont += 1

            if nome == 'adm' and senha == '000':
                logado = True
                return redirect('/adm')

            if usuario['nome'] == nome and usuario['senha'] == senha:
                logado = True
                return redirect('/usuarios')
            
            if cont >= len(usuarios):
                flash('USUARIO INVALIDO')
                return redirect("/")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    global logado
    user = []
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    user = [
        {
            "nome": nome,
            "senha": senha
        }
    ]
    with open('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)

    usuarioNovo = usuarios + user

    with open('usuarios.json', 'w') as gravarTemp:
        json.dump(usuarioNovo, gravarTemp, indent=4 )
    logado = True
    flash(F'{nome} CADASTRADO!!')
    return redirect('/adm')


@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    global logado
    logado = True
    usuario = request.form.get('usuarioPexcluir')
    usuarioDict = ast.literal_eval(usuario)
    nome = usuarioDict['nome']
    with open('usuarios.json') as usuariosTemp:
        usuariosJson = json.load(usuariosTemp)
        for c in usuariosJson:
            if c == usuarioDict:
                usuariosJson.remove(usuarioDict)
                with open('usuarios.json', 'w') as usuarioAexcluir:
                    json.dump(usuariosJson, usuarioAexcluir, indent=4)

    flash(F'{nome} EXCLUIDO')
    return redirect('/adm')


@app.route("/upload", methods=['POST'])
def upload():
    global logado
    logado = True
    
    arquivo = request.files.get('documento')
    nome_arquivo = arquivo.filename.replace(" ","-")
    arquivo.save(os.path.join('012/arquivos/', nome_arquivo))

    flash('Arquivo salvo')
    return redirect('/adm')



@app.route('/download', methods=['POST'])
def download():
    nomeArquivo = request.form.get('arquivosParaDownload')

    return send_from_directory('arquivos', nomeArquivo, as_attachment=True)



if __name__ in "__main__":
    app.run(debug=True)    