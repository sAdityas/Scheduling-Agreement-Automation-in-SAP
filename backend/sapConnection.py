import win32com.client
import pythoncom

def connection():
    try:
        pythoncom.CoInitialize()
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        application = SapGuiAuto.GetScriptingEngine
        session = application.Children(0).Children(0)

        return session
    except:
        raise Exception(f'SAP not logged in')