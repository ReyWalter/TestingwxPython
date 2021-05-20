from TestwxPython import HelloFrame as hf
import wx

if __name__ == '__main__':

    app = wx.App()

    frm = hf(None, title='Hello World')
    frm.Show()
    print('test')
    app.MainLoop()