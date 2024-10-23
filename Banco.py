import mysql.connector

class Banco():
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "root",
            database = "danielmartins_db"
        )
        self.create.Table()

    def createTable(self):
        c = self.conexao.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Usuario (id_usuario INT AUTO_INCREMENT PRIMARY KEY,   
            nome TEXT ,
            telefone TEXT ,
            email TEXT ,
            usuario TEXT ,
            senha TEXT )''')
        self.conexao.commit()
        c.close()