from datetime import datetime
import os
import customtkinter as ctk
from fpdf import FPDF
from num2words import num2words
from tkinter import messagebox

# Inicialização do aplicativo
App = ctk.CTk()
App.title("GERADOR RECIBOS IMOBILIARIA-V1_2024")
App.geometry("420x480")
App.resizable(False, False)
App.iconbitmap("icon.ico")

# Função para limpar os campos de entrada
def limpar_campos():
    entry_nome_pagador.delete(0, 'end')
    entry_cpf_pagador.delete(0, 'end')
    entry_valor.delete(0, 'end')
    entry_referente.delete(0, 'end')
    entry_formaPag.delete(0, 'end')
    entry_data.delete(0, 'end')
    entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
    entry_copias.delete(0, 'end')
    entry_copias.insert(0, '1')  # Valor padrão de 1 cópia

# Função para verificar vírgulas no campo de valor
def verificar_virgula(event):
    valor = entry_valor.get()
    if "," in valor:
        messagebox.showinfo("Atenção", "Use PONTO ( . ) para separação decimal, não VÍRGULA ( , ), Corrigi para Você!.")
        entry_valor.delete(0, 'end')
        entry_valor.insert(0, valor.replace(",", "."))

# Função para gerar o recibo
def gerar_recibo():
    nome_pagador = entry_nome_pagador.get()
    cpf_pagador = entry_cpf_pagador.get()
    valor = entry_valor.get()
    motivo = entry_referente.get()
    pagamento = entry_formaPag.get()
    data = entry_data.get()

    if not nome_pagador or not cpf_pagador or not valor or not motivo or not pagamento or not data:
        messagebox.showwarning("Atenção", "Por favor, Preencha Todos os Campos antes de Gerar o Recibo.")
        return

    valor = float(valor)
    valor_por_extenso = num2words(valor, lang='pt_BR', to='currency')
    cpf_pagador_formatado = f"{cpf_pagador[:3]}.{cpf_pagador[3:6]}.{cpf_pagador[6:9]}-{cpf_pagador[9:]}"
    empresa = "IMOBILIARIA LIDER"
    cnpj = "10.605.092/0001-97"
    local = "PORTO XAVIER - RS"

    pdf = FPDF()
    pdf.add_page()
    pdf.image('logo.png', 90, 8, 33)
    pdf.ln(20)
    pdf.set_font("Arial", size=12)

    texto_incial = 'IMOBILIARIA LIDER CNPJ = 10.605.092/0001-97 www.imobiliariaportoxavier.com.br '
    contato = 'marcelobeutler@gmail.com  Tel (55) 9 8116-9772'
    endereco = 'Rua Tiradentes, 606 CENTRO PORTO XAVIER - RS'
    texto = (f"Pelo presente, eu {empresa}, inscrito no CNPJ sob nº {cnpj}, declaro que RECEBI na data de hoje {data}, "
             f"o valor de R$ {valor:.2f} ({valor_por_extenso}), pela forma de pagamento de {pagamento}, de {nome_pagador}, "
             f"inscrito no CPF sob nº {cpf_pagador_formatado}, referente ao aluguel da: {motivo}.")
    texto_final = 'Sendo expressão de verdade e sem qualquer coação, firmo o presente recibo.'

    pdf.multi_cell(0, 10, txt=texto_incial, align='C')
    pdf.multi_cell(0, 10, txt=contato, align='C')
    pdf.multi_cell(0, 10, txt=endereco, align='C')
    pdf.ln(10)
    pdf.cell(0, 10, txt='Recibo', ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=texto, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=texto_final, align='C')
    pdf.ln(20)
    pdf.multi_cell(0, 10, txt='__________________________________________________', align='C')
    pdf.multi_cell(0, 10, txt=empresa, align='C')
    pdf.cell(0, 10, txt=f"{local}", align='L')
    pdf.cell(0, 10, txt=data, align='R')

    pdf.output("recibo.pdf", 'F')
    print('PDF gerado com sucesso!')

    imprimir_recibo()
    limpar_campos()

def imprimir_recibo():
    try:
        quantidade_copias = int(entry_copias.get())
    except ValueError:
        messagebox.showerror("Erro", "Insira um número válido de cópias.")
        return
    
    if os.path.exists("recibo.pdf"):
        for _ in range(quantidade_copias):
            os.startfile("recibo.pdf", "print")
    else:
        messagebox.showerror("Erro", "Arquivo de recibo não encontrado. Gere o recibo novamente.")

# Criação dos labels e campos de entrada
label_nome_pagador = ctk.CTkLabel(App, text='Nome Pagador')
label_nome_pagador.grid(row=0, column=0, padx=10, pady=10)
entry_nome_pagador = ctk.CTkEntry(App, width=250)
entry_nome_pagador.grid(row=0, column=1, padx=10, pady=10)

label_cpf_pagador = ctk.CTkLabel(App, text='CPF Pagador')
label_cpf_pagador.grid(row=1, column=0, padx=10, pady=10)
entry_cpf_pagador = ctk.CTkEntry(App, width=150)
entry_cpf_pagador.grid(row=1, column=1, padx=10, pady=10)

label_valor = ctk.CTkLabel(App, text='Valor Recibo R$')
label_valor.grid(row=2, column=0, padx=10, pady=10)
entry_valor = ctk.CTkEntry(App, width=150)
entry_valor.grid(row=2, column=1, padx=10, pady=10)
entry_valor.bind("<KeyRelease>", verificar_virgula)

label_referente = ctk.CTkLabel(App, text='Referente ao Aluguel da:')
label_referente.grid(row=3, column=0, padx=10, pady=10)
entry_referente = ctk.CTkEntry(App, width=250)
entry_referente.grid(row=3, column=1, padx=10, pady=10)

label_formaPag = ctk.CTkLabel(App, text='Forma Pagamento em')
label_formaPag.grid(row=4, column=0, padx=10, pady=10)
entry_formaPag = ctk.CTkEntry(App, width=250)
entry_formaPag.grid(row=4, column=1, padx=10, pady=10)

label_data = ctk.CTkLabel(App, text='Data (DD/MM/AAAA)')
label_data.grid(row=5, column=0, padx=10, pady=10)
entry_data = ctk.CTkEntry(App, width=150)
entry_data.grid(row=5, column=1, padx=10, pady=10)
entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))

label_copias = ctk.CTkLabel(App, text='Quantidade de Cópias')
label_copias.grid(row=6, column=0, padx=10, pady=10)
entry_copias = ctk.CTkEntry(App, width=150)
entry_copias.grid(row=6, column=1, padx=10, pady=10)
entry_copias.insert(0, '2')  # Define a quantidade padrão para 1 cópia

# Botões
botao_gerar_recibo = ctk.CTkButton(App, text='GERAR RECIBO', command=gerar_recibo)
botao_gerar_recibo.grid(row=7, column=0, columnspan=2, padx=10, pady=20, ipadx=40)

botao_fechar = ctk.CTkButton(App, text='FECHAR', text_color='purple', command=App.destroy)
botao_fechar.grid(row=8, column=0, columnspan=2, padx=8, pady=10, ipadx=40)

App.mainloop()