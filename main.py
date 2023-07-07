import customtkinter
import pyodbc
from tkcalendar import *
from tkinter import *
from tkinter import messagebox


def connection_database(driver='', server='', database='', username='', password='', trusted_connection='no'):

    connection_data = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TRUSTED_CONNECTION={trusted_connection};"

    connection = pyodbc.connect(connection_data)
    cursor = connection.cursor()
    return connection, cursor


connection, cursor = connection_database()

window = customtkinter.CTk()

window.geometry('700x500')
window.title("ModDate")
window.maxsize(width=900, height=550)
window.minsize(width=500, height=300)
window.resizable(width=True, height=True)
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')


def updateDate():
    try:
        cursor.execute(
            '''
				DECLARE @ST_ATUAL VARCHAR(1),  @ST_NOVO VARCHAR(1)     

				SET @ST_NOVO = '1' 

				SET @ST_ATUAL = '8'  

				

				UPDATE ZH6020 SET ZH6_STATUS = @ST_NOVO 

				--SELECT * FROM ZH6020 

				WHERE D_E_L_E_T_ = ''       

				--AND ZH6_DATAFI > '20220101' 

				and ZH6_STATUS = @ST_ATUAL 
			'''
        )
        connection.commit()
        messagebox.showinfo('Sistema', 'Data atualizada com sucesso')
    except pyodbc.DatabaseError:
        messagebox.showerror('Sistema', 'Erro ao tentar atualizar a data ')


def updateDateWithDate():
    try:
        format_date_calendar = ''.join(
            filter(str.isalnum, calendar_text_input.get()))
        mes = format_date_calendar[2:4]
        ano = format_date_calendar[4:]
        dia = format_date_calendar[:2]
        format_date = ano + mes + dia
        cursor.execute(
            f'''
				DECLARE @DT_APO VARCHAR(8), @ST_FILTRO VARCHAR(1) 

				SET @DT_APO = {format_date}

				SET @ST_FILTRO = '1'
				
				UPDATE ZH6020 SET ZH6_DTAPON  =  @DT_APO

				WHERE D_E_L_E_T_ = ''
				
				and ZH6_STATUS = @ST_FILTRO 
			'''
        )
        connection.commit()
        messagebox.showinfo('Sistema', 'Data atualizada com sucesso')
    except pyodbc.DatabaseError:
        messagebox.showerror('Sistema', 'Erro ao tentar atualizar a data ')


def grab_date():
    calendar_text_input.delete(0, END)
    calendar_text_input.insert(0, calendar_input.get_date())
    date_window.destroy()


def pick_date_calendar(event):
    global calendar_input, date_window

    date_window = customtkinter.CTkToplevel(window)
    date_window.geometry("400x250")
    date_window.title('Escolha uma data')
    date_window.grab_set()
    calendar_input = Calendar(
        date_window, selectmode='day', date_pattern='dd/mm/y')
    calendar_input.pack(pady=12)

    submit_button = customtkinter.CTkButton(
        date_window, text='submit', command=grab_date).place(x=135, y=210)


label1 = customtkinter.CTkLabel(window, text='Atualização de Status', font=(
    'arial bold', 20)).place(x=30, y=150)

button1 = customtkinter.CTkButton(
    window, text='Atualizar', command=updateDate)
button1.place(x=260, y=150)

label2 = customtkinter.CTkLabel(
    window, text='Atualização de data', font=('arial bold', 20)).place(x=30, y=300)

calendar_text_input = customtkinter.CTkEntry(window, width=250)
calendar_text_input.place(x=210, y=300)
calendar_text_input.insert(0, 'dia/mês/ano')
calendar_text_input.bind('<1>', pick_date_calendar)

button2 = customtkinter.CTkButton(
    window, text='Atualizar', command=updateDateWithDate)
button2.place(x=470, y=300)

window.mainloop()
