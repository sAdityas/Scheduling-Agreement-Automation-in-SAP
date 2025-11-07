import time
import sys

def update(session):
    try:
        # Focus on the schedule line count field
        session.findById("wnd[0]/usr/txtRM06E-ETNR2").setFocus()
        last_row_text = session.findById("wnd[0]/usr/txtRM06E-ETNR2").text.strip() or 0
        updated = False

        for r in range(1,int(last_row_text)):
            try:
                # Try to get the delivery date field
                sch = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/txtEKET-MENGE[2,{r}]")
                schqty = sch.text.strip()
                time.sleep(1)
                print(schqty)
                date_field = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/ctxtRM06E-EEIND[1,{r}]")
                date = date_field.text.strip()
            except:
                # If not visible, bring row to view
                index = session.findById("wnd[0]/usr/txtRM06E-ETNR1")
                index.text = str(r)
                session.findById("wnd[0]").sendVKey(0)
                time.sleep(0.3)
                try:
                    date = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/ctxtRM06E-EEIND[1,0]").text.strip()
                except:
                    continue  # If still not visible, skip

                r = 0  # Reset row index after navigation
            finally:
                
                sys.exit()
            if date and date != "":
                
                GRN = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/txtEKET-WEMNG[13,{r}]")
                upqty = GRN.text
                if upqty:
                    session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/txtEKET-MENGE[2,{r}]").text = upqty

                    # Confirm & Save
                    session.findById("wnd[0]").sendVKey(0)
                    time.sleep(0.5)
                    session.findById("wnd[0]").sendVKey(0)
                    time.sleep(0.5)
                    session.findById("wnd[0]").sendVKey(0)
                    time.sleep(0.5)
                    updated = True
                    return {
                        'updated' : updated,
                        'Qty' : upqty,
                        'Date' : date,
                    }


        if not updated:
            print("⚠️ No matching delivery date found.")
        return { 
            "result" : "⚠️ Np material Difference"   
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
