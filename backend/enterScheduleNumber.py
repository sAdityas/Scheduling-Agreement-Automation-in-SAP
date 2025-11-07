from sapConnection import connection


def enterSchN(session, aggrNumber):
    try:
        session.findById("wnd[0]/usr/ctxtRM06E-EVRTN").text = aggrNumber
        session.findById("wnd[0]").sendVKey (0)
    except:
        raise Exception("Cannot enter Agreement Number")