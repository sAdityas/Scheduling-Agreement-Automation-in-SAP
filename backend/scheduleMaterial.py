import time

def schMat(session, Date_Type, Delv_Date, SchQty):
    try:
        # Get number of currently filled schedule lines
        session.findById("wnd[0]/usr/txtRM06E-ETNR2").setFocus()
        last_row_text = session.findById("wnd[0]/usr/txtRM06E-ETNR2").text.strip()

        # Insert into the next available schedule line
        insert_row_index = 1  # table index always starts from 0
        insert_row_number = str(int(last_row_text) + 1)

        session.findById("wnd[0]/usr/txtRM06E-ETNR1").text = str(int(insert_row_number) - 1)
        session.findById("wnd[0]").sendVKey(0)  # Load new row

        # Input values
        session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/ctxtRM06E-LPEIN[0,{insert_row_index}]").text = Date_Type
        session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/ctxtRM06E-EEIND[1,{insert_row_index}]").text = Delv_Date
        session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/txtEKET-MENGE[2,{insert_row_index}]").text = SchQty
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(0.2)
        session.findById("wnd[0]").sendVKey(0)   

        # Save
        session.findById("wnd[0]/tbar[0]/btn[11]").press()
        time.sleep(0.3)
        session.findById("wnd[1]/tbar[0]/btn[0]").press()  # Info popup
        session.findById("wnd[1]/usr/btnSPOP-OPTION1").press()
        return True

    except Exception as e:
        
        # Clean rollback
        try:
            time.sleep(0.3)
            status_bar_text = session.findById("wnd[0]/sbar").Text
            print(status_bar_text)
            session.findById("wnd[0]/tbar[0]/btn[15]").press()  # Back
            session.findById("wnd[1]/usr/btnSPOP-OPTION2").setFocus()
            session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()

        except:
            if not status_bar_text:
                status_bar_text = "Material Blocked, Deleted or Unknown Error"
        raise Exception(status_bar_text)

