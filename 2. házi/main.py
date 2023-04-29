test = False
def index(arr, elem) -> int:
    for i in range(len(arr)):
        if arr[i] == elem:
            return i
    return -1
class Page:
    def __init__(self, name: str):
        self.name = name
        self.value: int = None
        self.freeze = 0
        self.frozen = False
        self.referenced = False
        
        
    def __str__(self) -> str:
        string = f"{self.name}{self.value}({self.freeze})"
        if self.referenced:
            string += "'"
        return string

class Fifo:
    def __init__(self) :
        self.storage = [] #<----[A | B | C]
    def Push(self, p: Page) :
        self.storage.append(p)
    def PushFront(self, p: Page) :
        self.storage.insert(len(self.storage)-1,p)
    def Pop(self) -> Page:
        return self.storage.pop(0)
    def Contains(self, value: int) -> bool:
        for x in self.storage:
            if x.value == value:
                if test:
                    print(f"\n\t{value} -> FIFO: | {self.Get(2)} | {self.Get(1)} | {self.Get(0)}\t{x.name}'\t", end="")
                # temp = self.storage.pop(index(self.storage, x))
                # temp.frozen = True
                # temp.freeze = 3
                # self.Push(temp)
                x.referenced = True
                return True
        return False
    def HasFree(self) -> bool: #avagy a fifoban van szabad keret (valahol)
        for x in self.storage:
            if x.freeze == 0:
                return True
        return False
    def HasReference(self) -> bool:
        for x in self.storage:
            if x.referenced:
                return True
        return False
    def Decrease(self):
        for x in self.storage:
            if x.freeze > 0:
                x.freeze -= 1
            if x.freeze == 0:
                x.frozen = False
    def PushBack(self, p: Page) :
        temp = self.storage.pop(index(self.storage, p))
        self.Push(temp)
    def Unlock(self, ref: int) : #első hivatkozás után feloldja a keretet
        for p in self.storage:
            if p.value == ref:
                p.frozen = False
                p.freeze = 0
    def top(self) -> Page:
        return self.storage[len(self.storage)-1]
    
    def Get(self, n: int): #TEST
        return self.storage[n]
    
    def GetFree(self) -> Page:
        i = 0
        while i < (len(self.storage)):
            if test:
                print(f"\n\t\ti={i}, Actual: {self.storage[i]}", end="")
            if self.storage[i].freeze > 0:
                if test:
                    print(f"\n\t\tSkipped {self.storage[i]}", end="")
                i+=1
                continue
                #self.Push(self.storage.pop(i)) #NEM JÓ A ROTÁLÁS
            
            if self.storage[i].referenced:
                if test:
                    print(f"\n\t  -> FIFO: | {fifo.Get(2)} | {fifo.Get(1)} | {fifo.Get(0)}\t{self.storage[i]}!!\t", end="")
                self.storage[i].referenced = False
                #self.Decrease()
                self.Push(self.storage.pop(i))
                if test:
                    print(f"\n\t\t  -> FIFO: | {fifo.Get(2)} | {fifo.Get(1)} | {fifo.Get(0)}\t", end="")
                #i-=1
            else:
                return self.storage.pop(i)
            #i+=1


if __name__ == "__main__":
    #line = input().split(',') #1,2,3,-1,5,-1
    line = input()
    line = line.split(',')
    
    pFaults = 0
    fifo = Fifo()
    
    fifo.Push(Page("A"))
    fifo.Push(Page("B"))
    fifo.Push(Page("C"))
    
    i = 0
    while i < len(line): #minden hivatkozásra
        ref = abs(int(line[i]))
        if fifo.Contains(ref):
            print("-", end="" if not test else "\n")
            fifo.Decrease()
            # temp = fifo.Pop()
            # fifo.Push(temp)
            
        else:
            if not fifo.HasFree() and not fifo.HasReference(): #ha egyáltalán nincs szabad keret a fifoban
                print("*", end="" if not test else "\n")
                pFaults += 1
                fifo.Decrease()
            else:
                # page = fifo.Pop()
                # while page.freeze > 0: #azaz a kivett lap még fagyasztott #TODO: lehet ez nem jó.  Lehet úgy kell, hogy a fifo elején lévő (fagyasztott) keret maradjon ott, de csökkenjen, a szabadot meg kivesszük
                #     fifo.Push(page)
                #     page = fifo.Pop()
                #     fifo.Decrease()
                # if page.freeze > 0:
                #     page = fifo.GetNotFrozen()
                
                page = fifo.GetFree()

                page.freeze = 3 #visszaállítjuk
                page.value = ref
                fifo.Decrease() #mindent csökkentünk a fifo-ban, de ezt még nem!
                fifo.Push(page)
                pFaults += 1
                print(page.name, end="" if not test else "\n")
                    
        i+=1
    print(f"\n{pFaults}")
    


# done = False
# while not done:
#     print("?")
#     page = fifo.top()
#     if not page.referenced and not page.freeze>0:
#         done = True
#         break
#     if page.referenced:
#         page.referenced = False
#         fifo.Push(fifo.Pop()) #de nincs Decrease!
#         page = fifo.top()
#     if page.freeze > 0:
#         #page.freeze -= 1
#         #fifo.Push(fifo.Pop()) #TODO: ide kell a magic!
#         for i in range(len(fifo.storage)-1):
#             if fifo.storage[i].freeze == 0:
#                 page = fifo.storage.pop(i)
#                 fifo.Decrease()
#                 done = True
#                 break
