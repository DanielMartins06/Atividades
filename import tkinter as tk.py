import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from mysql.connector import Error


class SistemaLogin:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Login")
        self.janela.geometry("400x400")
        self.janela.configure(bg="#151e70")

        self.inicializar_login()

    def conectar_banco(self):
        """Conecta ao banco de dados MySQL."""
        try:
            return mysql.connector.connect(
                host='localhost',
                user='seu_usuario',  # Substitua pelo seu usuário
                password='sua_senha',  # Substitua pela sua senha
                database='empresa'  # Substitua pelo nome do seu banco de dados
            )
        except Error as e:
            messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco: {e}")
            return None

    def registrar_usuario(self, usuario, senha, tipo):
        """Registra um novo usuário no banco de dados."""
        try:
            conexao = self.conectar_banco()
            if not conexao:
                return False

            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO usuarios (usuario, senha, tipo) VALUES (%s, %s, %s)",
                (usuario, senha, tipo)
            )
            conexao.commit()
            conexao.close()
            return True
        except Error:
            messagebox.showerror("Erro", "Erro ao registrar usuário.")
            return False

    def autenticar_login(self, usuario, senha):
        """Valida o login e retorna o tipo de usuário."""
        try:
            conexao = self.conectar_banco()
            if not conexao:
                return None

            cursor = conexao.cursor()
            cursor.execute("SELECT tipo, id FROM usuarios WHERE usuario = %s AND senha = %s", (usuario, senha))
            resultado = cursor.fetchone()
            conexao.close()

            return resultado if resultado else None
        except Error:
            messagebox.showerror("Erro", "Erro ao autenticar.")
            return None

    def inicializar_login(self):
        """Cria a janela de login."""
        frame_login = tk.Frame(self.janela, bg="#e1e2e8", width=300, height=250)
        frame_login.place(relx=0.5, rely=0.5, anchor="center")

        logo = tk.Label(self.janela, text="LOGO EMPRESA", bg="#151e70", fg="white", font=("Arial", 18, "bold"))
        logo.pack(pady=10)

        titulo = tk.Label(frame_login, text="Login", bg="#e1e2e8", font=("Arial", 14, "bold"))
        titulo.place(x=20, y=10)

        tk.Label(frame_login, text="Usuário:", bg="#e1e2e8").place(x=20, y=60)
        self.entrada_usuario = tk.Entry(frame_login)
        self.entrada_usuario.place(x=100, y=60, width=150)

        tk.Label(frame_login, text="Senha:", bg="#e1e2e8").place(x=20, y=100)
        self.entrada_senha = tk.Entry(frame_login, show="*")
        self.entrada_senha.place(x=100, y=100, width=150)

        botao_login = tk.Button(frame_login, text="Login", bg="#151e70", fg="white", command=self.processar_login)
        botao_login.place(x=20, y=160, width=120)

        botao_registrar = tk.Button(frame_login, text="Registrar", bg="#151e70", fg="white", command=self.abrir_tela_registro)
        botao_registrar.place(x=150, y=160, width=120)

    def abrir_tela_registro(self):
        """Abre uma nova janela para registrar um usuário."""
        janela_registro = tk.Toplevel()
        janela_registro.title("Registrar Usuário")
        janela_registro.geometry("300x300")

        tk.Label(janela_registro, text="Usuário:").pack(pady=5)
        entrada_usuario_registro = tk.Entry(janela_registro)
        entrada_usuario_registro.pack(pady=5)

        tk.Label(janela_registro, text="Senha:").pack(pady=5)
        entrada_senha_registro = tk.Entry(janela_registro, show="*")
        entrada_senha_registro.pack(pady=5)

        tk.Label(janela_registro, text="Tipo de Usuário:").pack(pady=5)
        tipo_usuario_var = tk.StringVar(value="cliente")
        tk.Radiobutton(janela_registro, text="Funcionário", variable=tipo_usuario_var, value="funcionario").pack()
        tk.Radiobutton(janela_registro, text="Cliente", variable=tipo_usuario_var, value="cliente").pack()

        def processar_registro():
            usuario = entrada_usuario_registro.get()
            senha = entrada_senha_registro.get()
            tipo = tipo_usuario_var.get()

            if not usuario or not senha:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return

            if self.registrar_usuario(usuario, senha, tipo):
                messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
                janela_registro.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao registrar o usuário.")

        tk.Button(janela_registro, text="Registrar", command=processar_registro).pack(pady=20)

    def processar_login(self):
        """Processa os dados inseridos na tela de login."""
        usuario = self.entrada_usuario.get()
        senha = self.entrada_senha.get()

        usuario_info = self.autenticar_login(usuario, senha)
        if usuario_info:
            self.abrir_menu(usuario_info[0], usuario_info[1])
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    def abrir_menu(self, tipo_usuario, id_usuario):
        """Abre o menu principal baseado no tipo de usuário."""
        self.janela.destroy()
        if tipo_usuario == "funcionario":
            self.criar_menu_funcionario()
        elif tipo_usuario == "cliente":
            self.criar_menu_cliente(id_usuario)

    def criar_menu_funcionario(self):
        """Cria a janela principal para funcionários."""
        janela_menu = tk.Tk()
        janela_menu.title("Menu Funcionário")
        janela_menu.geometry("800x600")

        frame_esquerdo = tk.Frame(janela_menu, bg="#e1e2e8", width=200)
        frame_esquerdo.pack(side="left", fill="y")

        botoes = [
            ("Funcionários", "funcionarios"),
            ("Clientes", "clientes"),
            ("Produtos", "produtos"),
            ("Pedidos", "pedidos"),
            ("Transportadoras", "transportadoras"),
            ("Fornecedores", "fornecedores"),
        ]

        for texto, tabela in botoes:
            botao = tk.Button(frame_esquerdo, text=texto, command=lambda t=tabela: self.visualizar_tabela(t))
            botao.pack()

    def visualizar_tabela(self, tabela):
        """Exibe uma tabela de dados do banco de dados na interface gráfica."""
        conexao = self.conectar_banco()
        if not conexao:
            return

        cursor = conexao.cursor()
        cursor.execute(f"SELECT * FROM {tabela}")
        dados = cursor.fetchall()
        conexao.close()

        janela_tabela = tk.Toplevel()
        janela_tabela.title(f"Visualizar {tabela.capitalize()}")
        janela_tabela.geometry("600x400")

        treeview = ttk.Treeview(janela_tabela)
        treeview.pack(fill="both", expand=True)

        colunas = [desc[0] for desc in cursor.description]
        treeview["columns"] = colunas

        for coluna in colunas:
            treeview.heading(coluna, text=coluna)
            treeview.column(coluna, width=100)

        for linha in dados:
            treeview.insert("", "end", values=linha)

    def criar_menu_cliente(self, id_cliente):
        """Cria a janela principal para clientes."""
        janela_menu = tk.Tk()
        janela_menu.title("Menu Cliente")
        janela_menu.geometry("400x300")

        frame_cliente = tk.Frame(janela_menu)
        frame_cliente.pack(fill="both", expand=True)

        botao_visualizar_produtos = tk.Button(
            frame_cliente, 
            text="Visualizar Produtos", 
            command=self.visualizar_produtos_cliente
        )
        botao_visualizar_produtos.pack(pady=20)

        botao_alterar_info = tk.Button(
            frame_cliente, 
            text="Alterar Informações", 
            command=lambda: self.abrir_tela_alterar_info(id_cliente)
        )
        botao_alterar_info.pack(pady=20)

        janela_menu.mainloop()

    def visualizar_produtos_cliente(self):
        """Exibe os produtos para o cliente."""
        conexao = self.conectar_banco()
        if not conexao:
            return

        cursor = conexao.cursor()
        cursor.execute("SELECT nome, preco FROM produtos")
        produtos = cursor.fetchall()
        conexao.close()

        janela_produtos = tk.Toplevel()
        janela_produtos.title("Produtos Disponíveis")
        janela_produtos.geometry("600x400")

        treeview = ttk.Treeview(janela_produtos)
        treeview.pack(fill="both", expand=True)

        treeview["columns"] = ["Produto", "Preço"]
        treeview.heading("Produto", text="Produto")
        treeview.heading("Preço", text="Preço")
        treeview.column("Produto", width=250)
        treeview.column("Preço", width=100)

        for produto in produtos:
            treeview.insert("", "end", values=produto)

    def abrir_tela_alterar_info(self, id_cliente):
        """Abre a tela para o cliente alterar suas informações."""
        janela_alterar = tk.Toplevel()
        janela_alterar.title("Alterar Informações")
        janela_alterar.geometry("300x300")

        tk.Label(janela_alterar, text="Novo Nome:").pack(pady=5)
        entrada_nome = tk.Entry(janela_alterar)
        entrada_nome.pack(pady=5)

        tk.Label(janela_alterar, text="Nova Senha:").pack(pady=5)
        entrada_senha = tk.Entry(janela_alterar, show="*")
        entrada_senha.pack(pady=5)

        def processar_alteracao():
            nome = entrada_nome.get()
            senha = entrada_senha.get()

            conexao = self.conectar_banco()
            if not conexao:
                return

            cursor = conexao.cursor()
            if nome:
                cursor.execute("UPDATE clientes SET nome = %s WHERE id = %s", (nome, id_cliente))
            if senha:
                cursor.execute("UPDATE usuarios SET senha = %s WHERE id = %s", (senha, id_cliente))
            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Informações alteradas com sucesso!")
            janela_alterar.destroy()

        tk.Button(janela_alterar, text="Alterar", command=processar_alteracao).pack(pady=20)

    def run(self):
        """Inicia a interface gráfica."""
        self.janela.mainloop()


# Criar uma instância do sistema e executar
if __name__ == "__main__":
    sistema = SistemaLogin()
    sistema.run()
