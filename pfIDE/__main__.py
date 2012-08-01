from editor.gui.main import IDE

if __name__ == '__main__':
    app = IDE(False)
    app.reactor.run()
    #app.MainLoop()
