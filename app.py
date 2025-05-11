from tkinter import Tk
from gui import FaultInjectorApp

def main():
    root = Tk()
    app = FaultInjectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
