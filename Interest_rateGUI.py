import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import pandas_datareader as pdr
import yfinance as yf
from datetime import datetime

start=datetime(2018,1,1)
end=datetime.today()

root = tk.Tk()
root.geometry('1200x850')

Height=800
Width=1000



# Reading xlsx file and modifying it a little. Please check the path so file can be read. 

data=pd.read_excel('Interest_rates.xlsx',header=4,index_col='Period')
mod=data.iloc[:-2]
red=mod.iloc[::-1]

# Changing column titles.

column_titles=['Eonia','Euribor 1kk','Euribor 3kk','Euribor 6kk','Euribor 12kk']
red.columns=column_titles

# Function that helps to select right columns of data.
new=''
def format(entry):
    if entry=='eonia' or entry=='Eonia':
        new='Eonia'
    elif entry=='Euribor 1kk':
        new='Euribor 1kk'
    elif entry=='Euribor 3kk':
        new='Euribor 3kk'
    elif entry=='Euribor 6kk':
        new='Euribor 6kk'
    elif entry=='Euribor 12kk':
        new='Euribor 12kk'
    elif entry=='All':
        new=column_titles
    else:
        print(f'{entry} was not a valid interest rate')
    return(new)

# Defining a function to graph interest rate graphs.

def graph(final):
    test=format(final)   
    fig=plt.figure(figsize=(12,7))
    plt.xlabel('Period',fontsize=16)
    plt.ylabel('Interest rate',fontsize=16)
    if test==column_titles:
        title='Interest rates'
    else:
        title=test
    plt.title(f'{title} 1999-2021',fontsize=16)
    plt.plot(red[test])
    plt.xticks(red.index[::12],rotation=30)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.savefig('Rate.png')
    photo= tk.PhotoImage(file='Rate.png')
    panel=tk.Label(root, image =photo)
    panel.image=photo
    panel.grid(row=15,column=0,columnspan=10)

# A function that converts names to their proper common names. 
def get_name(osake_list):
    company_names=[]
    for name in osake_list:
        osake=yf.Ticker(name)
        company_name=osake.info['longName']
        company_names.append(company_name)
    return(company_names)


# List of stocks to plot
osakkeet=['ORTHEX.HE','WRT1V.HE','TYRES.HE','UPM.HE','METSB.HE','SHOT.ST','ZIGN.ST','OUT1V.HE','FIA1S.HE']


# Functions to download stock.

def open_stock(Osake):
    osake=pdr.DataReader(Osake,'yahoo',start,end)
    hinta=osake['Adj Close']
    return(hinta)
    
stock_names=get_name(osakkeet)
my_stocks=open_stock(osakkeet)

# Creating a dictionary to swap names again for plotting. 
dictionary=dict(zip(osakkeet,stock_names))
print(dictionary)


# Plotting stock price graphs.

def kuvaaja(Osake):
    plt.figure(figsize=(12,7))
    plt.plot(my_stocks[Osake])
    plt.xlabel('Aika',fontsize=14)
    plt.xticks(rotation=20)
    plt.title(f'{convert(Osake)}',fontsize=18)
    plt.ylabel('Hinta',fontsize=14)
    plt.savefig('Kuvaaja.png')
    # plt.figure(figsize=(12,8))
    # plt.xlabel('Aika',fontsize=14)
    # plt.title('All stocks',fontsize=18)
    # plt.ylabel('Hinta',fontsize=14)
    # plt.plot(open_stock(osakkeet))
    # plt.savefig(r'C:\Users\ramie\Projects\Kuvaaja_all.png')
    photo= tk.PhotoImage(file='Kuvaaja.png')
    panel=tk.Label(root, image =photo)
    panel.image=photo
    panel.grid(row=15,column=0,columnspan=10)

# functions to swap names and select names from dropdown menus for plotting.

def select_stock(*args): 
    for i,j in dictionary.items():
        if j==drop_stocks.get():
            return(i)

def convert(name):
    for i,j in dictionary.items():
            if j==drop_stocks.get():
                return(j)

def select_rate():
    selected_rate=variable.get()
    return(selected_rate)

# Tkinter stuff for GUI.

drop_stocks=tk.StringVar(root)
drop_stocks.set('Stocks')
w=tk.OptionMenu(root,drop_stocks,*dictionary.values())
w.grid(row=0,column=0)

stock_button=tk.Button(root, text='Select stocks',command=lambda: kuvaaja(select_stock()))
stock_button.grid(row=1,column=0,columnspan=2,pady=10,padx=10,ipadx=100)


variable=tk.StringVar(root)
variable.set('Interest rate')
w=tk.OptionMenu(root,variable,*column_titles,'All')
w.grid(row=0,column=1)


interest_button=tk.Button(root, text='Select interest rate',command=lambda: graph(select_rate()))
interest_button.grid(row=2,column=0,columnspan=2,pady=10,padx=10,ipadx=100)


closing=tk.Button(root, text="Quit", command=root.destroy)
closing.grid(row=0,column=3)
root.mainloop()
