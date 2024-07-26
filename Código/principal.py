from flask import Flask,render_template,request,redirect
import json
import os #para localizar o caminho do diretorio que se encontra esse arquivo

app=Flask(__name__,template_folder='templates')

salva_titulo_site=[]#O titulo do site para funcionar a numeração deles
gets_site={}# Para adicionar os gets do editor
sites=[]#html modificado dos modelos
salva_login=[]#é uma lista que salva a variavel que recebe o request login da route /logar

@app.route('/')
def principal():
    return render_template('inicio.html')

@app.route('/login')
def login():
    print('Acessando a route /login')
    return render_template('login.html')

@app.route('/logar', methods=['POST'])
def check():
    login=request.form['login']
    salva_login.append(login)
    password=request.form['senha']
    
    diretorio_atual=os.path.dirname(os.path.abspath(__file__))#dirname(retorna o nome do caminho do diretorio)
    caminho_json= os.path.join(diretorio_atual,'dados.json')
    try:
        with open(caminho_json, 'r') as file:
            cadastros=json.load(file)

        for cadastro in cadastros:
            if login==cadastro["Usuario"] and password== cadastro["Senha"]:
                return render_template('meus_sites.html')

    except Exception as e:
        return f"Arquivo não encontrado {str(e)}"

    if login=='admin' and password=='abc':
        return render_template("meus_sites.html")

    if login=='' and password=='':
        return render_template('login.html')

@app.route('/cadastro')
def novo_cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar',methods=['POST'])   
def ok():
    nome=request.form['nome']
    senha=request.form['senha']
    email=request.form['email']

    dados={
        "Usuario":nome,
        "Senha":senha,
        "Email":email
    }
    diretorio_atual=os.path.dirname(os.path.abspath(__file__))
    caminho_json= os.path.join(diretorio_atual,'dados.json')

    try:
        with open(caminho_json, 'a') as file:
            json.dump(dados,file)
            file.write(',')
    except Exception as e:
        return f"Erro ao registrar {e}"
    
    return render_template ('login.html')

@app.route('/nova_senha')
def esqueceu_senha():
    return render_template('nova_senha.html')

@app.route('/redefinir_senha', methods=['POST'])
def altera_senha():
    email=request.form['email']
    diretorio_atual=os.path.dirname(os.path.abspath(__file__))
    caminho_json= os.path.join(diretorio_atual,'dados.json')
    try:
        with open(caminho_json,'r') as file:
            cadastros=json.load(file)

        for usuarios in cadastros:
            if email==usuarios['Email']:
                return render_template('altera_senha.html',email=email)#passar como parametro pro html a variavel que recebe o email
            
    except Exception as e:
        return f"Está ocorrendo problema em {e}"
    
@app.route('/senha_nova', methods=['POST'])
def senha_alterada():
    nova_senha=request.form['nova_senha']
    email=request.form['email']
    diretorio_atual=os.path.dirname(os.path.abspath(__file__))
    caminho_json= os.path.join(diretorio_atual,'dados.json')

    try:
        with open(caminho_json,'r') as file:
            cadastros=json.load(file)

        for usuarios in cadastros:
            if email==usuarios['Email']:
                usuarios['Senha']=nova_senha
            
        with open(caminho_json,'w') as file:
            json.dump(cadastros,file)
        return render_template('login.html')
    
    except Exception as e:
        return f"Não foi possivel alterar a senha {str(e)}"
    
@app.route('/meus_sites')
def usuario_sites():
    if len(sites)>=1:
        return render_template('meu_site.html')
    else:
        return render_template('meus_sites.html')

#Está aparecendo somente um site criado se excluir e criar outro aparece normalmente mas não vários em sequencia

@app.route('/excluir', methods=['POST'])
def excluir_site():
    if 'exclui_site' in request.form:
        sites.pop()
        salva_titulo_site.pop()
    return render_template('meus_sites.html',sites_html='')



@app.route('/estilo_pagina')
def modelo_sites():
    return render_template('estilo_pagina.html')

@app.route('/neutro', methods=['POST'])
def modelo_neutro():
    return render_template('editor.html')



@app.route('/altera')
def altera_site():
    titulo=request.args.get('titulo')#request.args.get ele verifica o teste.html e verifica se o parametro 'titulo' existe nele para assim substitui-lo
    descricao=request.args.get('descricao')
    paragrafo1=request.args.get('paragrafo1')

    if 'NovoParagrafo' and 'novaDescricao': #Verifica se esses parametros aparecem no html ou seja a função, se não ele pula pro else assim deixando essas variaveis vazias para que ao retornar o template não haja erro pois não acessou essas variaveis
        NovoParagrafo=request.args.get('NovoParagrafo')
        NovaDescricao=request.args.get('novaDescricao')
    else:
        NovoParagrafo=''
        NovaDescricao=''
    
    gets_site['Titulo']=titulo
    gets_site['Descricao']=descricao
    gets_site['Paragrafo1']=paragrafo1
    gets_site['NovoParagrafo']=NovoParagrafo
    gets_site['NovaDescricao']=NovaDescricao

   
    return render_template('editor.html',titulo=titulo,descricao=descricao,paragrafo1=paragrafo1,NovoParagrafo=NovoParagrafo,NovaDescricao=NovaDescricao)


@app.route('/salva_mod', methods=['POST'])
def salva_modelo():
    titulo=gets_site.get('Titulo')#chama o dicionario.get e o nome da chave para pegar os valores corretos
    descricao=gets_site.get('Descricao')
    paragrafo1=gets_site.get('Paragrafo1')
    NovoParagrafo=gets_site.get('NovoParagrafo')
    NovaDescricao=gets_site.get('NovaDescricao')

    #salva o modelo sem o editor
    sites.append(render_template('teste_mod.html',titulo=titulo,descricao=descricao,paragrafo1=paragrafo1,NovoParagrafo=NovoParagrafo,NovaDescricao=NovaDescricao))
    salva_titulo_site.append(titulo)
    diretorio_atual=os.path.dirname(os.path.abspath(__file__))
    caminho_json=os.path.join(diretorio_atual,'dados.json')
    try:
        with open(caminho_json,'r')as file:
            cadastros=json.load(file)
        for usuarios in cadastros:
            if salva_login[0]==usuarios['Usuario']:#[0] para acessar o primeiro obj salvo na lista
                usuarios['Site']=sites#como está no for o usuarios recebe cadastros do json, nisso usuarios o substitui para receber a nova chave
                usuarios['Titulo Site']=titulo
                with open(caminho_json,'w')as file:
                    json.dump(cadastros,file)
    except:
        pass

    return render_template('meu_site.html',titulo=titulo)# O problema está ocorrendo ao tentar carregar esse html junto para mostrar os sites criado

@app.route('/retorna_sites')
def retorna_site():
    #Pegar os valores que estão salvos no dicionario e passar como parametros pro modelo
    
    titulo=gets_site.get('Titulo')
    descricao=gets_site.get('Descricao')
    paragrafo1=gets_site.get('Paragrafo1')
    NovoParagrafo=gets_site.get('NovoParagrafo')
    NovaDescricao=gets_site.get('NovaDescricao')

    return render_template('teste_mod.html',titulo=titulo,descricao=descricao,paragrafo1=paragrafo1,NovoParagrafo=NovoParagrafo,NovaDescricao=NovaDescricao)

@app.route('/my_account')
def minha_conta():
    diretorio_atual=os.path.dirname(os.path.abspath(__file__))
    caminho_json=os.path.join(diretorio_atual,'dados.json')
    try:
        with open(caminho_json,'r')as file:
            cadastros=json.load(file)
        for usuario in cadastros:
            if salva_login[0]==usuario['Usuario']:
                return render_template('minha_conta.html',usuario=usuario['Usuario'],email=usuario['Email'])
        
    except Exception as e:
        return f"Não foi possivel acessar {str(e)}"
    
if __name__=="__main__":
    app.run()