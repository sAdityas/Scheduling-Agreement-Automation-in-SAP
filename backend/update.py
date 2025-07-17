import time

def update(session, delv_date, qty):
    try:
        # Focus on the schedule line count field
        session.findById("wnd[0]/usr/txtRM06E-ETNR2").setFocus()
        last_row_text = session.findById("wnd[0]/usr/txtRM06E-ETNR2").text.strip()

        updated = False
        total_rows = int(last_row_text) if last_row_text.isdigit() else 0

        for r in range(total_rows):
            try:
                # Try to get the delivery date field
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

            print(f"Checking row {r}: {date} vs {delv_date}")
            if date == delv_date:
                print(f"✅ Updating row {r} with quantity {qty}")
                session.findById(f"wnd[0]/usr/tblSAPMM06ETC_1117/txtEKET-MENGE[2,{r}]").text = qty

                # Confirm & Save
                session.findById("wnd[0]").sendVKey(0)
                time.sleep(0.5)
                session.findById("wnd[0]/tbar[0]/btn[11]").press()  # Save
                session.findById("wnd[1]/tbar[0]/btn[0]").press()
                try:
                    
                    session.findById("wnd[1]/usr/btnSPOP-OPTION1").press()
                except:
                    pass
                updated = True
                break  # Stop after successful update

        if not updated:
            print("⚠️ No matching delivery date found.")
        return updated

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
