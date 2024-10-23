from ast import Try
import mysql.connector
from Banco import Banco

class Usuarios(object):
    def __init__(self, id_usuario = 0, nome = "", telefone ="", email = "", usuario = "", senha = ""):
        self.info = {}
        self.id_usuario = id_usuario
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.usuario = usuario
        self.senha = senha

    def insertUser(self):
        Banco = Banco()
        try:
            c= Banco.conexao.cursor()
            c.execute("INSERT INTO usuario(nome, telefone, email, usuario, senha)VALUES(%s,%s,%s,%s,%s)", 
                            (self.nome, self.telefone, self.email, self.usuario, self.senha))
            Banco.conexao.commit()
            c.close()
            return "Usuario cadastrado com sucesso"

        except Exception as e:
            return f"Ocorreu um erro na inserção de usuarios: {e}"

    def insertUser(self):
        Banco = Banco()
        try:
            c= Banco.conexao.cursor()
            c.execute("UPDATE FROM usuario WHERE(nome, telefone, email, usuario, senha)VALUES(%s,%s,%s,%s,%s)", 
                            (self.nome, self.telefone, self.email, self.usuario, self.senha))
            Banco.conexao.commit()
            c.close()
            return "Usuario atualizado com sucesso"

        except Exception as e:
            return f"Ocorreu um erro na atualização de usuarios: {e}"