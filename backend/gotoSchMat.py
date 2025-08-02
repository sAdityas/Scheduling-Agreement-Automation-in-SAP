import time

# Global cache: { MATERIAL → ITEM_NUMBER }
material_item_cache = {}


def build_material_item_cache(session):
    """
    Collect all materials + EBELP (item numbers) from the SAP screen
    and store them in material_item_cache.
    """
    collected_map = {}
    seen_items = set()

    while True:
        row = 0
        found_valid_row = False  # ✅ detect if new valid row was found

        while True:
            try:
                mat_field = session.findById(
                    f"wnd[0]/usr/tblSAPMM06ETC_0222/ctxtEKPO-EMATN[1,{row}]"
                )
                item_field = session.findById(
                    f"wnd[0]/usr/tblSAPMM06ETC_0222/ctxtRM06E-EVRTP[0,{row}]"
                )
            except:
                break  # no more rows on screen

            try:
                material = mat_field.text.strip().upper().lstrip("0")  # normalize
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
                    break  # invalid entry

                seen_items.add(item_number)
                found_valid_row = True
                collected_map[material] = item_number

            except:
                pass

            row += 1

        # ✅ Stop if no new rows processed
        if not found_valid_row:
            break

        # 🔁 Move to next EBELP using next visible row
        try:
            next_item_field = session.findById(
                f"wnd[0]/usr/tblSAPMM06ETC_0222/ctxtRM06E-EVRTP[0,{row}]"
            )
            next_item_value = next_item_field.text.strip()

            if not next_item_value or not next_item_value.isdigit():
                break  # no more navigation possible

            session.findById("wnd[0]/usr/txtRM06E-EBELP").text = next_item_value
            session.findById("wnd[0]").sendVKey(0)
        except:
            break

    # Save results globally
    material_item_cache.update(collected_map)
    print(f"✅ Built material cache with {len(material_item_cache)} entries.{material_item_cache}")


def gotoMat(session, material):
    """
    Go to the SAP line item for a given MATERIAL.
    Uses cached EBELP if available, otherwise builds cache.
    """
    material = material.upper().lstrip("0")  # normalize like cache
    print(f"In Material Screen: {material}")

    # ✅ Step 1: Ensure cache is built
    if not material_item_cache:
        build_material_item_cache(session)

    # ✅ Step 2: Lookup in cache
    if material in material_item_cache:
        item_number = material_item_cache[material]
        session.findById("wnd[0]/usr/txtRM06E-EBELP").text = item_number
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(0.3)
        try:
            session.findById(
                "wnd[0]/usr/tblSAPMM06ETC_0222/ctxtEKPO-EMATN[1,0]"
            ).setFocus()
            session.findById("wnd[0]").sendVKey(2)
            return True
        except:
            pass

    print(f"❌ Material {material} not found in cache!")
    return False
