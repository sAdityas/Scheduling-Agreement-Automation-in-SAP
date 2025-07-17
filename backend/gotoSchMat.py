import time

# Global cache to avoid redundant lookups
material_item_cache = {}


def gotoMat(session, material):
    material = material.upper()
    max_rows = 20  # Safety cap

    print(f"In Material Screen: {material}")

    # ✅ Step 0: Check cache first
    if material in material_item_cache:
        cached_item = material_item_cache[material]
        session.findById("wnd[0]/usr/txtRM06E-EBELP").text = cached_item
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(0.3)
        try:
            session.findById("wnd[0]/usr/tblSAPMM06ETC_0222/ctxtEKPO-EMATN[1,0]").setFocus()
            session.findById("wnd[0]").sendVKey(2)
            return True
        except:
            pass  # Fallback if cache leads to failure

    # 🔢 Step 1: Count valid rows with item numbers
    valid_rows = 0
    for row in range(max_rows):
        try:
            field = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_0222/ctxtRM06E-EVRTP[0,{row}]")
            value = field.text.strip()
            if not value or value == "_____":
                break
            valid_rows += 1
        except:
            break

    # 🔍 Step 2: Check visible rows
    for row in range(valid_rows):
        try:
            mat_field = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_0222/ctxtEKPO-EMATN[1,{row}]")
            item_field = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_0222/ctxtRM06E-EVRTP[0,{row}]")

            if mat_field.text.strip().upper() == material:
                item_number = item_field.text.strip()
                
                material_item_cache[material] = item_number  # ✅ Cache it
                mat_field.setFocus()
                session.findById("wnd[0]").sendVKey(2)
                return True
        except:
            continue

    # 🔁 Step 3: EBELP loop
    row = 0
    while True:
        try:
            mat_field = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_0222/ctxtEKPO-EMATN[1,{row}]")
            item_field = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_0222/ctxtRM06E-EVRTP[0,{row}]")

            sap_material = mat_field.text.strip().upper()
            sap_item = item_field.text.strip()

            if sap_material == material:
                material_item_cache[material] = sap_item  # ✅ Cache it
                mat_field.setFocus()
                session.findById("wnd[0]").sendVKey(2)
                return True

            # Move to next EBELP
            next_item_field = session.findById(f"wnd[0]/usr/tblSAPMM06ETC_0222/ctxtRM06E-EVRTP[0,{row + 1}]")
            next_item_value = next_item_field.text.strip()

            if not next_item_value or not str(sap_item).isdigit():
                break

            next_item = str(int(sap_item) + 10).zfill(5)
            session.findById("wnd[0]/usr/txtRM06E-EBELP").text = next_item
            session.findById("wnd[0]").sendVKey(0)
            time.sleep(0.3)
            row = 0  # Reset row scan after navigation
        except:
            break

    return False
