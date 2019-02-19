import csv
import pydot
import tkinter as tk
from tkinter import *
import scanner
from tkinter import messagebox
import os
dirpath = os.getcwd()
os.environ["PATH"] += os.pathsep + dirpath + os.pathsep + 'graphviz-2.38\\release\\bin'




def readTokensFromCSVfile():
    with open(file) as fh:
        x = csv.reader(fh, delimiter=',')
        for y in x:
            Tokens.append(y)

def stmtSeq():
    global listOfEdges,listOfSubGraphes,listOfNodes,token
    subGraph=[]
    t = statement()
    p = t
    while token[0]!= 'EOF' and token[0] != 'end' and token[0] != 'else' and token[0]!='until':
        match(';')
        q = statement()
        if t== -1:
            t= p =q
        else:
            subGraph.append(p)
            subGraph.append(q)
            listOfEdges.append([p,q])
            p=q

    listOfSubGraphes.append(subGraph)
    return t

def statement():
    global listOfEdges, listOfSubGraphes, listOfNodes,token
    t=-1
    if token[0] == 'if':
        t = if_stmt()
    elif token[0] == 'repeat':
        t =repeat_stmt()
    elif token[1] == 'Identifier':
        t = assign_stmt()
    elif token[0] == 'read' or token[0] == 'Read':
       t = read_stmt()
    elif token[0] =='write':
        t = write_stmt()
    else:
        syntaxError("Unexpected token "+token[0])
        token = getToken()
    return t

def if_stmt():
    global Counter,token,listOfNodes,listOfEdges
    t= Counter
    listOfNodes.append(' IF')
    Counter += 1
    match('if')
    e = exp()
    listOfEdges.append([t,e])
    match('then')
    stmt_seq = stmtSeq()
    listOfEdges.append([t,stmt_seq])
    if token[0] =='else':
        match('else')
        stmt_seq = stmtSeq()
        listOfEdges.append([t, stmt_seq])
    match('end')
    return t
def repeat_stmt():
    global Counter,token,listOfNodes,listOfEdges
    t = Counter
    listOfNodes.append(' Repeat')
    Counter += 1
    match('repeat')
    stat_seq = stmtSeq()
    listOfEdges.append([t,stat_seq])
    match('until')
    e = exp()
    listOfEdges.append([t,e])
    return t
def assign_stmt():
    global Counter,token,listOfNodes,listOfEdges
    t = Counter
    if token[1]=='Identifier':
        listOfNodes.append(' Assign\n'+token[0])
    Counter += 1
    match(token[0])
    match(':=')
    e = exp()
    listOfEdges.append([t,e])
    return t

def read_stmt():
    global  Counter,token,listOfNodes,listOfEdges
    t = Counter
    match('read')
    if token[1] == 'Identifier':
        listOfNodes.append(' Read\n'+token[0])
    Counter += 1
    match(token[0])
    return t
def write_stmt():
    global Counter,token,listOfNodes,listOfEdges
    t = Counter
    listOfNodes.append(' Write')
    Counter += 1
    match('write')
    e = exp()
    listOfEdges.append([t,e])
    return t
def exp():
    global Counter,token,listOfNodes,listOfEdges
    t = simple_exp()
    if token[0]=='<' or token[0]=='=':
        p = Counter
        listOfNodes.append(token[0])
        Counter +=1
        listOfEdges.append([p,t])
        t=p
        match(token[0])
        e = simple_exp()
        listOfEdges.append([t,e])
    return t
def simple_exp():
    global Counter,token,listOfNodes,listOfEdges
    t = term()
    while token[0] == '+' or token[0]=='-':
        p = Counter
        listOfNodes.append(token[0])
        Counter += 1
        listOfEdges.append([p,t])
        t= p
        match(token[0])
        x = term()
        listOfEdges.append([t,x])
    return t
def term():
    global Counter,token,listOfNodes,listOfEdges
    t = factor()
    while token[0]=="*" or token[0] =='/':
        p = Counter
        listOfNodes.append(token[0])
        Counter +=1
        listOfEdges.append([p,t])
        t = p
        match(token[0])
        f = factor()
        listOfEdges.append([p,f])
    return t
def factor():
    global Counter,token,listOfNodes,listOfEdges
    t = -1
    if token[1] =='Number':
        t = Counter
        listOfNodes.append(token[0])
        Counter+=1
        match(token[0])
    elif token[1] == 'Identifier':
        t = Counter
        listOfNodes.append(token[0])
        Counter+=1
        match(token[0])
    elif token[0] == '(':
        match('(')
        t = exp()
        match(')')
    else:
        syntaxError("unexpacted Token "+token[0])
        getToken()
    return t
def match(data):
    global token
    if token[0]== data:
         getToken()
    else:
        syntaxError("unExpected Token "+token[0])

def syntaxError(message):
    print(message)
def getToken():
    global Tokens, token, tokenIndex
    if tokenIndex< len(Tokens):
        token = Tokens[tokenIndex]
        tokenIndex += 1
        if token[1] == 'Comment':
            getToken()
    elif tokenIndex == len(Tokens):
        token = ['EOF','EOF']
    else:
        print("Something wrog")


def nwindow():
    global generatedPhoto
    nwin = Toplevel()
    w, h = top.winfo_screenwidth() - 20, top.winfo_screenheight() - 80
    nwin.geometry("%dx%d+0+0" % (w, h))
    nwin.title("Syntax tree")
    img = PhotoImage(file=str(generatedPhoto)+'.png')
    canvas = Canvas(nwin, width=0, height=0, scrollregion=(0, 0, img.width() + 20, img.height() + 10))
    canvas.create_image(0, 0, anchor=NW, image=img)
    hbar = Scrollbar(canvas, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=canvas.xview)
    vbar = Scrollbar(canvas, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=canvas.yview)
    canvas.config(width=1000, height=1000)
    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas.pack(side=LEFT, expand=True, fill=BOTH)
    nwin.mainloop()
generatedPhoto =0
def callback():
    global  generatedPhoto,Counter,Tokens,token,tokenIndex,listOfNodes,listOfEdges,listOfSubGraphes
    generatedPhoto+=1
    scannerInputFile = open('scannerInput.txt', "w")
    if len(TextArea.get("1.0", "end-1c")) ==0:
        messagebox._show("Please enter Tiny code first")
        return
    scannerInputFile.write(TextArea.get("1.0", END))
    scannerInputFile.flush()
    scannerInputFile.close()
    scanner.Scanner()
    readTokensFromCSVfile()
    getToken()
    t = stmtSeq()
    graph = pydot.Dot(graph_type='graph', fontname="Verdana", ordering='out')  # ,ordering='out'
    for i in range(len(listOfNodes)):
        if listOfNodes[i][0] == ' ':
             node = pydot.Node(name = str(i),label =listOfNodes[i],shape = 'box')
             graph.add_node(node)
        else:
            node = pydot.Node(name=str(i), label=listOfNodes[i])
            graph.add_node(node)
    for i in range(len(listOfSubGraphes)):
        subGraph = pydot.Subgraph(rank = 'same')
        for j in listOfSubGraphes[i]:
            subGraph.add_node(pydot.Node(name = str(j),label = listOfNodes[j]))
        graph.add_subgraph(subGraph)
    for i in (listOfEdges):
        graph.add_edge(pydot.Edge(str(i[0]),str(i[1])))
    graph.write_png(str(generatedPhoto)+'.png')
    Tokens = []
    tokenIndex = 0
    Counter = 0
    listOfNodes = []
    listOfEdges = []
    listOfSubGraphes = []
    nwindow()


file = 'token.txt'
Tokens = []
tokenIndex =0
token = ['adel','mah']

Counter = 0
listOfNodes = []
listOfEdges = []
listOfSubGraphes = []

top = tk.Tk()
w, h = top.winfo_screenwidth()-20, top.winfo_screenheight()-80
top.geometry("%dx%d+0+0" % (w, h))
w = tk.Label(top, text="Enter Tiny Code", font='Helvetica 18 bold')
w.grid(pady = 50)
w.pack()
TextArea = Text()
ScrolledText = Scrollbar(top)
ScrolledText.config(command=TextArea.yview)
TextArea.config(yscrollcommand=ScrolledText.set)
ScrolledText.pack(side=RIGHT)
TextArea.pack()
b = Button(top, text="Scan and Parse", command=callback,height = 5, width = 15,padx =2)
b.pack()
top.mainloop()










