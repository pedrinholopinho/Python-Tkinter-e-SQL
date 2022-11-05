import os
import tkinter.messagebox as Messagebox
from tkinter import *

import feedparser
import mysql.connector

conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = ''
)
#sql
cursor = conexao.cursor()

cursor.execute('create database if not exists cadastro')

cursor.execute('use cadastro')

cursor.execute("create table if not exists times(id int primary key,nome_time varchar(20),link varchar (255))")

cursor.execute("create table if not exists cadastro(usuario varchar(20) primary key, senha varchar(20))")

cursor.execute("show columns from cadastro like 'time';")

#if not cursor.fetchall():
  #  cursor.execute("ALTER TABLE 'cadastro' ADD 'time_id' INT NOT NULL AFTER 'senha';")
    #conexao.commit()
    #cursor.execute("ALTER TABLE 'cadastro' ADD CONSTRAINT 'time_fk' FOREIGN KEY ('time_id') REFERENCES 'times'('id') ON DELETE NO ACTION ON UPDATE NO ACTION;")
    #conexao.commit()



# tkinter

master = Tk()
master.title('Bem-vindo!')
master.geometry('400x300')
master.configure(bg='steelblue')
# master.wm_attributes('-transparentcolor', 'grey')
# master.iconbitmap('ico.ico')
# master.wm_attributes("-transparentcolor", 'grey')
master.resizable(width=1, height=1)

# Grid
master.grid_columnconfigure(0,weight=1)
master.grid_columnconfigure(1,weight=1)

master.grid_rowconfigure(0, weight=0)
master.grid_rowconfigure(1, weight=0)
master.grid_rowconfigure(2, weight=0)
master.grid_rowconfigure(3, weight=0)
master.grid_rowconfigure(4, weight=0)
master.grid_rowconfigure(5, weight=1)

#funçao
def salvar():
    salvar

def nova_janela():
    nova_janela = Tk()
    nova_janela.title("Notícias")
    
    nova_janela.geometry('400x300')
    
    master.destroy()

    time_escolhido=StringVar(nova_janela)
    time_escolhido.set('Botafogo')
    op_times=OptionMenu(nova_janela,time_escolhido,'Vasco','Flamengo','Botafogo','Bangu','Fluminense','América')
    op_times.pack()

    save=Button(nova_janela,text='Salvar',command=salvar)
    save.pack()
    
    li_times=Listbox(nova_janela)
    li_times.pack(fill=BOTH)

  
    d = feedparser.parse('https://www.mg.superesportes.com.br/rss/noticias/futebol/botafogo/rss.xml')
    print("Título    >>",d['feed']['title'])
    print("Descrição >>",d.feed.subtitle)
    for entry in d.entries:     
     print("Notícia >>",entry.link)


    
    
def cadastrar():
    usuario=en_usuario.get()
    senha=en_senha.get()

    if not len(usuario) or not len(senha):
        Messagebox.showerror('erro','Complete todos os campos.')    
        return 
    cursor.execute("insert ignore into cadastro (usuario,senha) values ('%s' , '%s')" %(usuario,senha) )
    conexao.commit()
    Messagebox.showinfo('Informação','Cadastro concluido!')

def entrar():
    usuario=en_usuario.get()
    senha=en_senha.get()

    if not len(usuario) or not len(senha):
        Messagebox.showerror('erro','Complete todos os campos.')    
        return 
    cursor.execute("select * from cadastro where usuario = '%s' and senha = '%s' " %(usuario,senha) )
    retorno=cursor.fetchall()
    if len (retorno)>0:
       nova_janela()
    else:
        Messagebox.showerror('Error','login incorreto')
    
    
   
#criando labels

label_usuario = Label(master, bd=2, justify=CENTER, text="Usuário", bg='steelblue', fg='white')
label_usuario.grid(row=0, column=0, sticky='ew', columnspan=2)

#criando caixa de entrada
en_usuario = Entry(master, bd=2, justify=CENTER)
en_usuario.grid(row=1, column=0, columnspan=2, ipadx=30)

label_senha = Label(master, bd=2, justify=CENTER, text="Senha", bg='steelblue', fg='white')
label_senha.grid(row=2, column=0, sticky='ew', columnspan=2)

en_senha = Entry(master, bd=2, justify=CENTER,show="*",)
en_senha.grid(row=3, column=0, columnspan=2, ipadx=30)

#criação do botao
btn_entrar = Button(master, command=entrar, text="Entrar")
btn_entrar.grid(row=4, column=0, sticky='e', rowspan=2, padx=10)

btn_cadastrar = Button(master,command=cadastrar,text="Cadastrar")
btn_cadastrar.grid(row=4, column=1, sticky='e', rowspan=2, padx=10)
master.mainloop()
