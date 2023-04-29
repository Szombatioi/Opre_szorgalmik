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
        self.referenced = False
    def __str__(self):
        return self.name

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
        for i in range(len(self.storage)):
            if self.storage[i] == value:
                self.storage[i].referenced = True
                return True
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
    def PushBack(self, p: Page) -> None:
        # temp = self.storage.pop(index(self.storage, p))
        # self.Push(temp)
        self.storage.insert(0,page)
    def GetFree(self) -> Page:
        i=0
        while i < len(self.storage)-1:
            page = self.storage[i]
            if page.freeze == 0 and not page.referenced:
                if page.referenced:
                    self.storage[i].referenced = False
                    #self.Push(self.storage.pop(i))
                else:
                    page = self.storage.pop(i)
                    self.Decrease()
                    return page    
            i+=1
    def top(self) -> Page:
        return self.storage[0]
                


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
        else:
            if not fifo.HasFree(): #ha egyáltalán nincs szabad keret a fifoban
                print("*", end="" if not test else "\n")
                pFaults += 1
                fifo.Decrease()
            else:
                page = fifo.Pop()
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