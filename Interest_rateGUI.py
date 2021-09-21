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

# Selected paths work only on my computers

path_lnx='~/Rami/Interest_rates/Interest_rates.xlsx'
path_windows=r'C:\Users\ramie\Downloads\korot.xlsx'

#lnx_stocks='~/Rami/Interest_rates\Kuvaaja_{0}.png'.format(i)
#save_fig_windows=r'C:\Users\ramie\Projects\Kuvaaja

# Reading csv as pandas dataframe and modifying it a litle. 



data=pd.read_excel('Interest_rates.xlsx',header=4,index_col='Period')
mod=data.iloc[:-2]
red=mod.iloc[::-1]

# Changing column titles.

column_titles=['Eonia','Euribor 1kk','Euribor 3kk','Euribor 6kk','Euribor 12kk']
red.columns=column_titles

# Defining a function to graph plots.
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


# List of stocks to plot

def get_name(osake_list):
    company_names=[]
    for name in osake_list:
        osake=yf.Ticker(name)
        company_name=osake.info['longName']
        company_names.append(company_name)
    return(company_names)

colours=['r','g','b','k','c','y','m','teal','sienna']
osakkeet=['ORTHEX.HE','WRT1V.HE','TYRES.HE','UPM.HE','METSB.HE','SHOT.ST','ZIGN.ST','OUT1V.HE','FIA1S.HE']


# Functions to download stock prices and plot graphs

def open_stock(Osake):
    osake=pdr.DataReader(Osake,'yahoo',start,end)
    hinta=osake['Adj Close']
    return(hinta)
    
stock_names=get_name(osakkeet)
my_stocks=open_stock(osakkeet)

def kuvaaja(Osake):
    title=[t for t in stock_names if t == Osake]
    plt.figure(figsize=(12,7))
    plt.plot(my_stocks[Osake])
    plt.xlabel('Aika',fontsize=14)
    plt.xticks(rotation=20)
    plt.title(f'{title}',fontsize=18)
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

def select_stock():
    selected_stock=drop_stocks.get()
    return(selected_stock)


def select_rate():
    selected_rate=variable.get()
    return(selected_rate)


drop_stocks=tk.StringVar(root)
drop_stocks.set('Stocks')
w=tk.OptionMenu(root,drop_stocks,*osakkeet)
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
