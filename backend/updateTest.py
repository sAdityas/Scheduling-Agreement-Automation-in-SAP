import sys
import time


def update(session):
    try:
        global updated
        updated = False
        last_row = int(session.findById("wnd[0]/usr/txtRM06E-ETNR2").text.strip() or 0)
        print("last_row:", last_row)

        linet = session.findById("wnd[0]/usr/txtRM06E-ETNR1")
        linet.text = str(last_row)
        session.findById("wnd[0]").sendVKey(0)                # SAP table index
        cell = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/txtEKET-MENGE[2,0]")
        grn = session.findById("wnd[0]/usr/tblSAPMM06ETC_1117/txtEKET-WEMNG[13,0]")
        qty = cell.text.strip()
        grnqty = grn.text.strip()
        print(f"Row {last_row}: Schedule qty = {qty}: grnQty = {grnqty}")
        
        if qty != grnqty:
            if grnqty == '' or not grnqty or grnqty == '0' or grnqty == None:
                updated = False
                return {
                'updated' : updated,
                'result' : '⚠️ GRN Qty not found',
                'status' : 'failed'
                }
            qty = grnqty
            cell.text = qty
            session.findById("wnd[0]").sendVKey(0)
            session.findById("wnd[0]").sendVKey(0)
            updated  = True
            return{
                'updated' : updated,
                'status' : 'success',
                'Qty' : qty,
                'GRN' : grnqty,

            }
    except Exception as e:
        try:
            time.sleep(0.3)
            status_bar_text = session.findById("wnd[0]/sbar").Text
            print(f"❌ SAP Error: {status_bar_text}")
            session.findById("wnd[0]/tbar[0]/btn[15]").press()  # Back
            session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()
        except:
            pass
        raise Exception(f"Update Failed: {str(e)}")
    