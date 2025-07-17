from sapConnection import connection

def gotoCode(session):
    try:
        session.findById("wnd[0]/tbar[0]/okcd").text = "/nME38"
        session.findById("wnd[0]").sendVKey(0)
    except:
        raise Exception("Error: Cannot locate to Transaction ME38")
