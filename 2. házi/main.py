class Page:
    def __init__(self, name: str) -> None:
        self.name = name
        self.value: int = None
        self.freeze = 0
        self.frozen = False
        
        
    def __str__(self) -> str:
        return f"{self.name} - {self.value}"

class Fifo:
    def __init__(self) -> None:
        self.storage = []
    def Push(self, p: Page) -> None:
        self.storage.insert(0,p)
    def PushFront(self, p: Page) -> None:
        self.storage.append(p)
    def Pop(self) -> Page:
        return self.storage.pop(len(self.storage)-1)
    def Contains(self, value: int) -> bool:
        for x in self.storage:
            if x.value == value:
                return True
        return False
    def HasFree(self) -> bool: #avagy a fifoban van szabad keret (valahol)
        # print("HasFree in")
        for x in self.storage:
            # print(f"{x.name} - {x.freeze}")
            if x.freeze == 0:
                # print("HasFree out and TRUE")
                return True
        # print("HasFree out and FALSE")
        return False
    def Decrease(self):
        for x in self.storage:
            if x.freeze > 0:
                x.freeze -= 1
            if x.freeze == 0:
                x.frozen = False


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
        #print(f"i={i} | ref={ref} -> ", end="")
        if fifo.Contains(ref):
            print("-", end="")
            fifo.Decrease()
        else:
            if not fifo.HasFree(): #ha egyáltalán nincs szabad keret a fifoban
                print("*", end="")
                pFaults += 1
                fifo.Decrease()
            else:
                page = fifo.Pop()
                while page.freeze > 0: #azaz a kivett lap még fagyasztott
                    fifo.Push(page)
                    page = fifo.Pop()
                    fifo.Decrease()
                page.freeze = 3 #visszaállítjuk
                page.frozen = True
                page.value = ref
                fifo.Decrease() #minden csökkentünk a fifo-ban, de ezt még nem!
                fifo.Push(page)
                pFaults += 1
                print(page.name, end="")
                # if page.frozen and page.freeze > 0: #ha a vizsgált keret még fagyasztva van, akkor visszaküldjük
                #     page.freeze -= 1
                #     fifo.Push(page)
                #     i -= 1 #a hivatkozást még nem dobjuk ki!
                # else: #avagy ha szabad a vizsgált keret
                    
        i+=1

            # if fifo.HasNoFree():
            #     print("*", end="")
            # else:
            #     page = fifo.Pop()
            #     if page.frozen and page.freeze > 0: #ha a FIFO elején még fagyasztva van a keret
            #         page.freeze -= 1
            #         fifo.Push(page)
            #     else: #TODO: a frozen tul-t állítsuk át néha (de hogy?)
            #         page.freeze = 3 #visszaállítás
            #         page.frozen = True
            #         page.value = ref
            #         fifo.Push(page)
            #         pFaults += 1
            #         print(page.name, end="")
    print(f"\n{pFaults}")
    
