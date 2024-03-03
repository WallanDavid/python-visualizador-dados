import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class DataVisualizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualização de Dados")

        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.tipo_grafico_var = tk.StringVar(value="barra")

        # Botão para atualizar o gráfico
        self.btn_atualizar = ttk.Button(self.frame, text="Atualizar Gráfico", command=self.atualizar_grafico)
        self.btn_atualizar.grid(row=0, column=0, pady=10)

        # Combobox para escolher o tipo de gráfico
        self.combobox_tipo_grafico = ttk.Combobox(self.frame, values=["barra", "dispersao"], state="readonly", textvariable=self.tipo_grafico_var)
        self.combobox_tipo_grafico.grid(row=0, column=1, padx=10, pady=10)
        self.combobox_tipo_grafico.bind("<<ComboboxSelected>>", self.atualizar_grafico)

        # Inicializa um gráfico vazio
        self.figura = Figure(figsize=(6, 4), tight_layout=True)
        self.grafico = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)

        # Adiciona barra de rolagem
        self.scrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.get_tk_widget().xview)
        self.scrollbar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        self.canvas.get_tk_widget().configure(xscrollcommand=self.scrollbar.set)

        # Outros controles
        self.btn_salvar = ttk.Button(self.frame, text="Salvar Gráfico", command=self.salvar_grafico)
        self.btn_salvar.grid(row=3, column=0, pady=10)

        self.btn_limpar = ttk.Button(self.frame, text="Limpar Gráfico", command=self.limpar_grafico)
        self.btn_limpar.grid(row=3, column=1, pady=10)

        # Outras variáveis
        self.cores = ['skyblue', 'salmon', 'lightgreen', 'gold', 'orchid']

    def criar_dados_aleatorios(self):
        # Cria dados aleatórios para o gráfico
        categorias = ['A', 'B', 'C', 'D', 'E']
        valores = np.random.randint(1, 10, size=len(categorias))
        return categorias, valores

    def atualizar_grafico(self, event=None):
        # Limpa o gráfico antes de atualizar
        self.grafico.clear()

        # Cria dados aleatórios
        categorias, valores = self.criar_dados_aleatorios()

        # Plota o gráfico com base no tipo selecionado
        if self.tipo_grafico_var.get() == "barra":
            self.grafico.bar(categorias, valores, color=self.escolher_cores())
        elif self.tipo_grafico_var.get() == "dispersao":
            estilo_linha = self.escolher_estilo_linha()
            self.grafico.scatter(categorias, valores, color=self.escolher_cores(), marker='o', label='Pontos', linestyle=estilo_linha)

        # Adiciona legenda
        self.grafico.legend()

        # Adiciona título dinâmico
        tipo_grafico = "Gráfico de Barras" if self.tipo_grafico_var.get() == "barra" else "Gráfico de Dispersão"
        self.grafico.set_title(f'{tipo_grafico} Aleatório')
        self.grafico.set_xlabel('Categorias')
        self.grafico.set_ylabel('Valores')

        # Atualiza o canvas
        self.canvas.draw()

    def escolher_cores(self):
        cor, _ = colorchooser.askcolor(title="Escolha uma Cor")
        return cor

    def escolher_estilo_linha(self):
        estilo_linha_var = tk.StringVar(value="-")
        estilo_linha_menu = ttk.Combobox(self.frame, values=["-", "--", "-.", ":"], state="readonly", textvariable=estilo_linha_var)
        estilo_linha_menu.grid(row=0, column=2, padx=10, pady=10)
        estilo_linha_menu.set("-")  # Padrão
        return estilo_linha_var.get()

    def salvar_grafico(self):
        nome_arquivo = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Arquivos PNG", "*.png")])
        if nome_arquivo:
            self.figura.savefig(nome_arquivo)

    def limpar_grafico(self):
        self.grafico.clear()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizationApp(root)
    root.mainloop()
