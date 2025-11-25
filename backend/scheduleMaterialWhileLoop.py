def schMatWhile(session):
    # 1. Find total rows
    row = 0
    try:
        while True:
            session.findById(
                f"wnd[0]/usr/tblSAPMM06ETC_1117/txtEKET-MENGE[2,{row}]"
            ).setFocus()
            row += 1
    except:
        # we hit the first invalid index
            return row
    
