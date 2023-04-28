test = False
def index(arr, elem) -> int:
    for i in range(len(arr)):
        if arr[i] == elem:
            return i
    return -1
class Page:
    def __init__(self, name: str) -> None:
        self.name = name
        self.value: int = None
        self.freeze = 0
        self.frozen = False
        
        
    def __str__(self) -> str:
        return f"{self.name}{self.value}"

class Fifo:
    def __init__(self) -> None:
        self.storage = [] #<----[A | B | C]
    def Push(self, p: Page) -> None:
        self.storage.append(p)
    def PushFront(self, p: Page) -> None:
        self.storage.insert(len(self.storage)-1,p)
    def Pop(self) -> Page:
        return self.storage.pop(0)
    def Contains(self, value: int) -> bool:
        for x in self.storage:
            if x.value == value:
                # temp = self.storage.pop(index(self.storage, x))
                # temp.frozen = True
                # temp.freeze = 3
                # self.Push(temp)
                return True
                # if index(self.storage, x) == 0:
                #     temp = self.storage.pop(index(self.storage, x))
                #     temp.frozen = True
                #     temp.freeze = 3
                #     self.Push(temp)
        return False
    def HasFree(self) -> bool: #avagy a fifoban van szabad keret (valahol)
        for x in self.storage:
            if x.freeze == 0:
                return True
        return False
    def Decrease(self):
        for x in self.storage:
            if x.freeze > 0:
                x.freeze -= 1
            if x.freeze == 0:
                x.frozen = False
    def PushBack(self, p: Page) -> None:
        temp = self.storage.pop(index(self.storage, p))
        self.Push(temp)
    def Unlock(self, ref: int) -> None: #első hivatkozás után feloldja a keretet
        for p in self.storage:
            if p.value == ref:
                p.frozen = False
                p.freeze = 0
    def top(self) -> Page:
        return self.storage[len(self.storage)-1]
    
    def Get(self, n: int): #TEST
        return self.storage[n]


if __name__ == "__main__":
    line = input().split(',') #1,2,3,-1,5,-1
    
    pFaults = 0
    fifo = Fifo()
    
    fifo.Push(Page("A"))
    fifo.Push(Page("B"))
    fifo.Push(Page("C"))
    
    i = 0
    while i < len(line): #minden hivatkozásra
        ref = abs(int(line[i]))
        if test:
            print(f"{ref} -> FIFO: | {fifo.Get(2)} | {fifo.Get(1)} | {fifo.Get(0)}\t", end="")
        if fifo.Contains(ref):
            print("-", end="" if not test else "\n")
            fifo.Decrease()
            temp = fifo.Pop()
            fifo.Push(temp)
            
        else:
            if not fifo.HasFree(): #ha egyáltalán nincs szabad keret a fifoban
                print("*", end="" if not test else "\n")
                pFaults += 1
                fifo.Decrease()
            else:
                page = fifo.Pop()
                while page.freeze > 0: #azaz a kivett lap még fagyasztott #TODO: lehet ez nem jó.  Lehet úgy kell, hogy a fifo elején lévő (fagyasztott) keret maradjon ott, de csökkenjen, a szabadot meg kivesszük
                    fifo.Push(page)
                    page = fifo.Pop()
                    fifo.Decrease()
                # if page.freeze > 0:
                #     page = fifo.GetNotFrozen()
                page.freeze = 3 #visszaállítjuk
                page.frozen = True
                page.value = ref
                fifo.Decrease() #minden csökkentünk a fifo-ban, de ezt még nem!
                fifo.Push(page)
                pFaults += 1
                print(page.name, end="" if not test else "\n")
                    
        i+=1
    print(f"\n{pFaults}")
    
