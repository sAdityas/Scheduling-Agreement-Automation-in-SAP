import time
import sys
from scheduleMaterialWhileLoop import schMatWhile

def schMat(session, Date_Type, Delv_Date, SchQty, material):
    try:
        # Get number of currently filled schedule lines
       
        row = schMatWhile(session)
        last_row_text = session.findById("wnd[0]/usr/txtRM06E-ETNR2").text.strip()
        # sys.exit()
        # Insert into the next available schedule line
        insert_row_index = 1  # table index always starts from 0
        insert_row_number = str(int(last_row_text) + 1)
        r = 1
        noGrn = []
        
        session.findById("wnd[0]/usr/txtRM06E-ETNR1").text = str(int(insert_row_number) - 1)
        session.findById("wnd[0]").sendVKey(0)
        last_row_grn = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/txtEKET-WEMNG[13,{0}]").text.strip()
        if not last_row_grn or last_row_grn == '':
            return {
                "success": False,
                "error": "GRN Qty not found"
            }    


        cellSchQty = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/txtEKET-MENGE[2,{0}]")
        cellSchQty.setFocus()
        cellSchQty.text.strip()       
        cellGrnQty = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/txtEKET-WEMNG[13,{0}]")
        print(f"Row {1} Sch Qty: {cellGrnQty}")
        cellGrnQty.setFocus()
        cellSchQty.text = cellGrnQty.text.strip()

    # If GRN quantity present, update schedule qty for this row
        if len(noGrn) > 0:
            session.findById("wnd[0]/tbar[0]/okcd").text = "/n"
            session.findById('wnd[0]').sendVKey(0)

        # sys.exit()
        #     return res
        session.findById("wnd[0]/usr/txtRM06E-ETNR1").text = str(int(insert_row_number) - 1)
        session.findById("wnd[0]").sendVKey(0)  # Load new row
        print("Inserting at row index:", insert_row_index)
        # sys.exit()
        # Input values
        session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/ctxtRM06E-LPEIN[0,{insert_row_index}]").text = Date_Type
        session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/ctxtRM06E-EEIND[1,{insert_row_index}]").text = Delv_Date
        session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/txtEKET-MENGE[2,{insert_row_index}]").text = SchQty
        session.findById("wnd[0]").sendVKey(0)
        session.findById("wnd[0]").sendVKey(0)
        # sys.exit()

        # Save
        session.findById("wnd[0]/tbar[0]/btn[11]").press()  
        session.findById("wnd[1]/tbar[0]/btn[0]").press()  # Info popup
        session.findById("wnd[1]/usr/btnSPOP-OPTION1").press()
        print(cellGrnQty.text.strip())
        return {
            "success": True,
            "grnQty": cellGrnQty.text.strip()
        }


    except Exception as e:
        print(e)
        # Clean rollback
        try:
            time.sleep(0.3)
            status_bar_text = session.findById("wnd[0]/sbar").Text
            session.findById("wnd[0]/tbar[0]/btn[15]").press()  # Back
            session.findById("wnd[1]/usr/btnSPOP-OPTION2").setFocus()
            session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()

        except:
            if not status_bar_text:
                status_bar_text = "Material Blocked, Deleted or Unknown Error"
        raise Exception(status_bar_text)
