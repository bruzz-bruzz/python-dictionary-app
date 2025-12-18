from tkinter import *
import requests
import json
from tkinter import font

def addWord():
    selWord = ''
    mArr,exArr = [],[]
    def getWord():
        global selWord,mArr,exArr
        
        selWord = wordEnt.get()
        res = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{selWord}')
        data = res.json()
        word,meaning,example = data[0]['word'], data[0]['meanings'][0]['definitions'][0]['definition'], data[0]['meanings'][0]['definitions'][0]
        mArr,exArr = [],[]
        for x in range(len(data[0]['meanings'][0]['definitions'])):
            mArr.append(data[0]['meanings'][0]['definitions'][x]['definition'])
            if 'example' in data[0]['meanings'][0]['definitions'][x].keys():
                exArr.append(data[0]['meanings'][0]['definitions'][x]['example'])
            else:
                exArr.append(None)
        print(word,meaning,exArr[0])
        print(mArr,exArr)
        status.config(text='done fetching')
    def saveWord():
        global selWord,mArr,exArr
        with open('a.json','r+') as f:
            data = json.load(f)
            data['words'].append(selWord)
            data['definitions'].append(mArr)
            data['examples'].append(exArr)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
    def changeStatus(event):
        status.config(text='')
    addWindow = Tk()
    addWindow.title('Add Word')
    addWindow.geometry('300x300+25+25')
    wordEnt = Entry(addWindow)
    wordEnt.pack()
    confirm = Button(addWindow,text='get',command=getWord)
    confirm.pack()
    save = Button(addWindow,text='save', command=saveWord)
    save.pack()
    status = Label(addWindow,text='')
    status.pack()
    wordEnt.bind('<KeyRelease>',changeStatus)
    addWindow.mainloop()
def fetchWord():
    word,definition, example = '','',''
    def getWord():
        global word,definition,example
        
        with open('a.json','r') as f:
            data = json.load(f)
            if getEnt.get() in data['words']:
                idx = data['words'].index(getEnt.get())
                word,definition,example = data['words'][idx], data['definitions'][idx], data['examples'][idx]
                mTxt,exTxt = '',''
                for x in range(len(definition)):
                    mTxt += str(x+1) + '. ' + str(definition[x]) + '\n' + 'Example: ' + str(example[x]) + '\n'
                
                mLbl.config(text=mTxt)
                statusLbl.config(text=f'successfully fetched data for {getEnt.get()}')
            else:
                mLbl.config(text='')
                statusLbl.config(text=f'{getEnt.get()} not in list.')
         
    fetchWindow = Tk()
    fetchWindow.title('Get Word')
    fetchWindow.geometry('300x500+25+25')
    getEnt = Entry(fetchWindow)
    getEnt.pack()
    confirm = Button(fetchWindow,text='get',command=getWord)
    confirm.pack()
    Label(fetchWindow,text='Definitions: ').pack()
    mLbl = Label(fetchWindow,text='',wraplength=280)
    mLbl.pack()
    statusLbl = Label(fetchWindow,text='')
    statusLbl.pack()
    fetchWindow.mainloop()
def listAll():

    def loadWords():
        global words
        with open('a.json','r') as f:
            data = json.load(f)
            words = data['words']
            wordList = data['words']
            txt = ''
            for x in words:
                txt += x + '\n'
            txtLabel.delete('1.0',END)
            txtLabel.insert('1.0',txt)

        
    def searchWord(event):
        res = searchEnt.get() in words
        print(words)
        if res == False:
            searchRes.config(text=f'{searchEnt.get()} is not in the list.')
        else:
            searchRes.config(text=f'{searchEnt.get()} is in the list.')

    listAllWindow = Tk()
    listAllWindow.title('Word List')
    listAllWindow.geometry('300x600+25+25')
    cf = font.Font(family='Lucida Console',size=12)
    searchEnt = Entry(listAllWindow)
    searchEnt.pack()
    searchRes = Label(listAllWindow,text='')
    searchRes.pack()
    txtLabel = Text(listAllWindow,wrap='word',font=cf)
    txtLabel.pack()
    searchEnt.bind('<KeyRelease>',searchWord)
    loadWords()
    listAllWindow.mainloop()
def deleteWord():
    wordsArr,definitionsArr, examplesArr = [],[],[]
    with open('a.json','r') as f:
        data = json.load(f)
        wordsArr = data['words']
        definitionsArr = data['definitions']
        examplesArr = data['examples']
        
    def initDel():

        word = delEnt.get()
        if word in wordsArr:
            idx = wordsArr.index(word)
            wordsArr.pop(idx)
            definitionsArr.pop(idx)
            examplesArr.pop(idx)
            statusLbl.config(text=f'{word} has been deleted.')
            with open('a.json','r+') as f:
                data = json.load(f)
                data['words'] = wordsArr
                data['definitions'] = definitionsArr
                data['examples'] = examplesArr
                f.seek(0)
                json.dump(data,f,indent=4)
                f.truncate()
        else:
            statusLbl.config(text=f'{word} not in list.')
            print(f'{word} not in list')
    delWin = Tk()
    delWin.geometry('200x100+250+250')
    delWin.title('Delete Word')
    delEnt = Entry(delWin)
    delEnt.pack()
    confirm = Button(delWin,text='confirm',command=initDel)
    confirm.pack()
    statusLbl = Label(delWin,text='')
    statusLbl.pack()
    delWin.mainloop()
mainWin = Tk()
mainWin.title('Main Window')
mainWin.geometry('200x200+125+125')
add = Button(mainWin, text='Add Word',command=addWord)
add.pack()
fetch = Button(mainWin,text='Fetch Word',command=fetchWord)
fetch.pack()
showAll = Button(mainWin,text='List Words', command= listAll)
showAll.pack()
delete = Button(mainWin,text='Delete Word',command=deleteWord)
delete.pack()
mainWin.mainloop()
