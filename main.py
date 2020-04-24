import webapp2
import jinja2
import os
from bd import*

formInicio = """
<form method="post">
    Bem Vindo ao TARSIER!
    <br><br>
    <label>
        Usuario:
        <input type="text" name="user" value="%(user)s">
    </label>
    <label>
        Senha:
        <input type="password" name="senha" value="%(senha)s">
    </label>
    <br>
    <p>%(error)s</p>
    <input type="submit" name="button" value="Entrar">
    <br>
</form>
<form method="post">
    <label>
        <p>Pergunta:</p>
        <textarea name="pergunta" rows="4" cols="50">%(resp)s</textarea>
    </label>
    <br>
    <p>%(erro)s</p>
    <br>
    <button name="button" type="submit">Entrar</button>
    <br>
</form>
"""

formCriar = """
<form method="post">
    <label>
        <p>Pergunta:</p>
        <textarea name="pergunta" rows="4" cols="50">%(pergunta)s</textarea>
    </label>
    <br><br>
    <label>
        Quantidade de alternativas:
        <input type="text" name="qtd" value="%(qtd)s">
    </label>
    <br><br>
    <input name="button" value="Enviar Dados" type="submit">
    <br>
</form>
<form method="post">
    <p>%(resp)s</p>
    <button name="button" type="submit">Entrar</button>
</form>
<br>%(error)s<br>
"""


form = """
<form method="post">
    TABELA
    <br><br>
    <label>
        <input type="text" name="cep" value="%(cep)s">
    </label>
    <br><br>    
	<table border="1">
		<tr> 
			<td>%(resp)s</td>
			<td>cell2</td>
			<td>cell3</td>
		</tr>
		<tr> 
			<td>cell1</td>
			<td>cell2</td>
			<td>cell3</td>
		</tr>
	</table>
    <p>%(error)s</p>
    <br>
    <input type="submit">
</form>
"""

form1 = '''
<form method="post">
    <p>Name: <input type="text" name="name" /></p>
    <p>Favorite foods:</p>
        <select name="favorite_foods" multiple size="4">
            <option value="apples">Apples</option>
            <option value="bananas">Bananas</option>
            <option value="carrots">Carrots</option>
            <option value="durians">Durians</option>
        </select>
    <p>Birth year: <input type="text" name="birth_year" /></p>
    <br>
    <p>%(nome)s</p>
    <p>%(comida)s</p>
    <p>%(ano)s</p>
    <p><input type="submit" /></p>
    <br>
</form>
'''


form2 = '''
<form method="post">
    Qual o seu sexo?
    <br><br>
    <input type="radio" name="sex" value="male">Male
    <br>
    <input type="radio" name="sex" value="female">Female
    <br>
    %(resp)s
    <p><input type="submit" /></p>
</form>
'''

form3 = '''
<form method="post">
    <p>%(s)s</p>
    <p>%(error)s</p>
    <p><input type="submit" /></p>
</form>
'''

'''def valid_CPF(cpf):

    if (cpf):
		if cpf.isdigit() :
			i = 10
			soma = 0
			for c in cpf[:9]:
				c = int (c)
				soma += i*c
				i = i - 1
			if (soma % 11) < 2:
				if int(cpf[9]) == 0:
					return cpf
			elif int (cpf[9]) == (11 - (soma % 11)):
				return cpf
    return None'''

def criar_form(form, resp, user_pergunta, user_qtd):
    return form % {"resp": resp, "pergunta": user_pergunta, "qtd": user_qtd, "error": ""}


class PaginaInicial(webapp2.RequestHandler):
    def write_form(self, error="", user="", senha="", resp="", erro=""):
        self.response.out.write(formInicio % {"error": error, "user": user, "senha": senha, "resp": resp, "erro": erro})

    def get(self):
        user_user = self.request.get('user')
        user_senha = self.request.get('senha')
        # self.redirect('/SecondPage')
        # self.write_form("", user_user, user_senha)
        self.write_form(self)


    def post(self):
        if(self.request.get('button') == "Entrar"):
            nome = self.request.get('user')
            senha = self.request.get('senha')

            a = Aluno(key_name=nome, nome=nome, senha=senha)
            a.put()

            self.write_form("", "", "", "TESTE", "")

        else:
            resp = Aluno.get_by_key_name("joao", parent=None).nome
            '''for p in Aluno.all():
                resp += p.nome + ": " + p.senha + "\n"
            '''
            self.write_form("", "", "", resp, "")
            # self.redirect('/SecondPage')

class PaginaCriar(webapp2.RequestHandler):

    def write_form(self, resp="", pergunta="", qtd="", error=""):
        self.response.out.write(formCriar % {"resp": resp, "pergunta": pergunta, "qtd": qtd, "error": error})

    def get(self):
        self.write_form(self)

    def post(self):

        if(self.request.get('button') == "Enviar Dados"):
            user_qtd = int(self.request.get('qtd'))
            user_pergunta = self.request.get('pergunta')
            i = 0
            resp = ''

            while i < user_qtd:
                resp += '<input type="text" name=%s/><br><br>'%str(i)
                i += 1

            self.write_form(resp, user_pergunta, user_qtd, "")

        else:

            '''i = 0
            resp = ''
            while i < 3:
                resp += self.request.get(str(i))
                i += 1'''
            self.write_form("", "", "", "")

class Pagina(webapp2.RequestHandler):

    def write_form(self, error="", sa="", qtd=""):
        if(qtd == ""):
            qtd = 0
        formul = '''<form method="post">
                        <p>Quantidade: <input type="text" name="qtd" value=%(qtd)s/><br></p>
                        <p>%(s)s</p>
                        <br>%(error)s
                    </form>
                 '''
        resp = ''
        temp = '%(sa)s'
        i = 0
        while i < int(qtd):
            resp += '<input type="text" name=%s value=%s/><br><br>' % (str(i), temp)
            i += 1

        if(qtd == 0):
            qtd = ""

        formul = formul % {"s": resp, "qtd": qtd, "error": "%(error)s<br><button name='button' value='Entrar' type='submit'>Entrar</button>"}

        self.response.out.write(formul % {"sa": sa, "error": error, "qtd": qtd})

    def get(self):
        self.write_form(self)

    def post(self):
        if(self.request.get('button') == "Entrar"):
            i = 0
            resp = ''
            while i < contador:
                resp += self.request.get(str(i)) + '<br>'
                i += 1

            self.write_form(resp, "", self.request.get("qtd"))
            # self.write_form(self.request.get('0'), "")
        else:
            self.write_form(self)



class MainPage(webapp2.RequestHandler):
    def write_form(self, resp=""):
        self.response.out.write(form2 % {"resp": resp})

    def get(self):
        self.write_form(self)

    def post(self):
        self.redirect('/SecondPage')
        '''name = self.request.get("sex")
        resp = 'Sexo: ' + name
        gay = '<input type="radio" name="sex" value="gay">Gay<br>' \
              '<input type="radio" name="sex" value="bi">Bi<br><br>'
        self.write_form(gay + resp)'''


'''class MainPage(webapp2.RequestHandler):
    def write_form(self, nome="", comida="", ano=""):
        self.response.out.write(form1 % {"nome": nome, "comida": comida, "ano": ano})

    def get(self):
        self.write_form(self)

    def post(self):
        name = self.request.get("name")
        favorite_foods = self.request.get_all("favorite_foods")
        birth_year = self.request.get_range("birth_year",
                                            min_value=1900,
                                            max_value=datetime.datetime.utcnow().year,
                                            default=1900)
        nome = 'Nome: ' + name
        comida = 'Comida: ' + favorite_foods[0]
        ano = 'Ano: ' + str(birth_year)
        self.write_form(nome, comida, ano)'''


class SecondPage(webapp2.RequestHandler):
    def write_form(self, error="", cep="", resp=""):
        self.response.out.write(form % {"error": error, "cep": cep, "resp": resp})

    def get(self):
        self.write_form(self)

    def post(self):
        self.redirect('/')
        '''cep = self.request.get('cep')
        self.write_form("", cep, cep)'''
        # self.response.out.write("Thanks! That's a totally valid cpf!")

class Teste(webapp2.RequestHandler):
    def get(self):
        template_values = {'Title': "Talister", 'Nome': "Elias"}

        template = jinja_environment.get_template('cadastro.html')
        self.response.write(template.render(template_values))


contador = 5
jinja_environment = jinja2.Environment(autoescape = True,
                                       loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__) + '/templates')))
app = webapp2.WSGIApplication([('/', Teste), ('/SecondPage', Pagina)], debug=True)

