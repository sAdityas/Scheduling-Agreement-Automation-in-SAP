import time
from gotoCode import gotoCode
from enterScheduleNumber import enterSchN

def getExcelData(session, aggrNumber):
    gotoCode(session)
    enterSchN(session, aggrNumber)

    collected_data = []
    seen_items = set()

    while True:
        row = 0
        found_valid_row = False  # ✅ Flag to detect if at least one new valid row was processed

        while True:
            try:
                mat_field = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_0222/ctxtEKPO-EMATN[1,{row}]")
                item_field = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_0222/ctxtRM06E-EVRTP[0,{row}]")
                short_text = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_0222/txtEKPO-TXZ01[2,{row}]")
                target_qty = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_0222/txtEKPO-KTMNG[3,{row}]")
                unit_entry = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_0222/ctxtEKPO-MEINS[4,{row}]")
                open_qty = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_0222/txtRM06E-OKTMN[5,{row}]")
            except:
                break  # ❌ No more rows available — exit inner loop

            try:
                material = mat_field.text.strip().upper()
                item_number = item_field.text.strip().zfill(5)
                if (
                    not material 
                    or not item_number 
                    or item_number in seen_items 
                    or "_" in material 
                    or "_" in item_number 
                    or all(c in "_-" for c in material)
                    or all(c in "_-" for c in item_number)
                ):
                    break

                print(item_number)
                seen_items.add(item_number)
                found_valid_row = True  # ✅ Mark that we got a valid row

                collected_data.append({
                    "Material": material,
                    "Short Text": short_text.text.strip(),
                    "Target Qty": target_qty.text.strip(),
                    "Unit of Entry": unit_entry.text.strip(),
                    "Open Qty": open_qty.text.strip()
                })
                print(collected_data)    
            except:
                found_valid_row = False

            row += 1

        # ✅ No new valid row on screen, exit
        if not found_valid_row:
            break

        # Move to next EBELP item range
        try:
            last_item = max(seen_items)
            next_item = str(int(last_item) + 10).zfill(5)
            session.findById("wnd[0]/usr/txtRM06E-EBELP").text = next_item
            session.findById("wnd[0]").sendVKey(0)
        except:
            break  # If screen navigation fails
    return collected_data
