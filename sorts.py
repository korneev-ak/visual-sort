

def isSorted(values) -> bool:
    for i in range(len(values)-1):
        if values[i]>values[i+1]:
            return False
    return True




def Bubble(App) -> bool:
    myName=App.curFunc
    sortedIndex=len(App.values)
    while not(isSorted(App.values)):
        for i in range(sortedIndex-1):
            print(i)
            if myName!=App.curFunc:return False
            if App.values[i]<App.values[i+1]:

                first=App.values[i]
                App.values[i]=App.values[i+1]
                App.values[i+1]=first
            App.update()
        sortedIndex-=1
    return isSorted(App.values)

def InsertionSort(App) ->bool:
    myName=App.curFunc
    for i in range(1,len(App.values)):
        x=App.values[i]
        j=i
        while(j>0 and App.values[j-1]<x):
            if myName!=App.curFunc:return False
            App.values[j]=App.values[j-1]
            j-=1
            App.update()
        App.values[j]=x
    return isSorted(App.values)

def ShellSort(App):
    interval = len(App.values) // 2
    while interval > 0:
        for i in range(interval, len(App.values)):
            temp = App.values[i]
            j = i
            while j >= interval and App.values[j - interval] > temp:
                App.values[j] = App.values[j - interval]
                j -= interval
            App.values[j] = temp
            App.update()
        interval //= 2
