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
    def GetFree(self) -> Page:
        i = 0
        while i < (len(self.storage)):
            if self.storage[i].freeze > 0:
                i+=1
                continue
            
            if self.storage[i].referenced:
                self.storage[i].referenced = False
                self.Push(self.storage.pop(i))
            else:
                return self.storage.pop(i)


if __name__ == "__main__":
    line = input().split(',')
    
    pFaults = 0
    fifo = Fifo()
    
    fifo.Push(Page("A"))
    fifo.Push(Page("B"))
    fifo.Push(Page("C"))
    
    i = 0
    while i < len(line): #minden hivatkozásra
        ref = abs(int(line[i]))
        if fifo.Contains(ref):
            print("-", end="")
            fifo.Decrease()
            
        else:
            if not fifo.HasFree() and not fifo.HasReference(): #ha egyáltalán nincs szabad keret a fifoban
                print("*", end="")
                pFaults += 1
                fifo.Decrease()
            else:
                page = fifo.GetFree()
                page.freeze = 3 #visszaállítjuk
                page.value = ref
                fifo.Decrease() #mindent csökkentünk a fifo-ban, de ezt még nem!
                fifo.Push(page)
                pFaults += 1
                print(page.name, end="")
                    
        i+=1
    print(f"\n{pFaults}")
