import sys

# 📦 Important Packages
from sapConnection import connection 
from gotoCode import gotoCode
from enterScheduleNumber import enterSchN
from scheduleMaterial import schMat
from gotoSchMat import gotoMat
from getExcel import getExcelData
from update import update


# 🌐 Flask Libraries
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import traceback

# 🌍 CORS Setup
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔁 Type Conversion Helper
def convert_types(obj):
    if isinstance(obj, dict):
        return {k: convert_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_types(i) for i in obj]
    elif isinstance(obj, (np.integer, )):
        return int(obj)
    elif isinstance(obj, (np.floating, )):
        return float(obj)
    else:
        return obj

# 🚀 Main Scheduling Route
@app.route("/main", methods=["POST"])
def main():
    results = []
    uploaded_file = request.files.get("file")
    
    if uploaded_file is None:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [col.strip() for col in df.columns]
    except Exception as e:
        return jsonify({"error": f"Error reading Excel/CSV: {e}"}), 400

    required_columns = [
        'Material',
        'Date Type',
        'Delivery Date',
        'Scheduled Quantity',
    ]

    for col in required_columns:
        if col not in df.columns:
            return jsonify({"error": f"Missing column in Excel: {col}"}), 400

    try:
        session = connection()
    except Exception as e:
        return jsonify({'error': f'Unable to connect to SAP: {str(e)}'}), 500

    if session is not None:
        gotoCode(session)
        data = request.form
        aggrNumber = str(data.get("aggrNumber"))

        enterSchN(session, aggrNumber)

        for _, row_data in df.iterrows():
            def safe_get(col):
                val = row_data.get(col, "-")
                if pd.isna(val) or str(val).strip() == "":
                    return None
                return str(val).strip()

            material = safe_get('Material')
            date_type = safe_get('Date Type')
            delivery_date = safe_get('Delivery Date')
            scheduled_quantity = safe_get('Scheduled Quantity')
            # ✅ SKIP ROW if ANY of these is NA/empty
            if not all([material, date_type, delivery_date, scheduled_quantity]):
                continue

            item_results = {
                "material": material,
                'date_type': date_type,
                'delivery_date': delivery_date,
                'scheduled_quantity': scheduled_quantity,
                'updated' : None,
                'error': None,
                'status': None
            }
            print(item_results['material'])
            try:
                gotoCode(session)
                enterSchN(session, aggrNumber)
                goto_result = gotoMat(session,material)
                if not goto_result:
                    item_results["error"] = "Material not found in SAP"
                    item_results["status"] = "Skipped"
                    results.append(item_results)
                    continue

                Updated = schMat(session, date_type, delivery_date, scheduled_quantity, material)
                print(f"Updated Res: {Updated}")
                if Updated:
                    item_results["error"] = Updated
                    item_results["status"] = "failed"
                else:
                    item_results["status"] = "success"
                    item_results["error"] = None   
                    item_results["updated"] = Updated

            except Exception as e:
                item_results["error"] = f"Exception: {str(e)}"
                item_results["status"] = "failed"

            results.append(item_results)
    # 🌐 Final Status Check
    final_status = "success"
    for r in results:
        if r.get("status") == "failed":
            final_status = "Partial Failure"
            break
        elif r.get("status") == "Skipped" and final_status != "Partial Failure":
            final_status = "Completed with Skips"

    return jsonify({
        "results": convert_types(results),
        "status": final_status
    }), 200 


# 📥 Route to Extract Excel Data from SAP
@app.route("/getExcel", methods=["POST"])
def get_excel_route():
    try:
        data = request.form
        aggrNumber = str(data.get("aggrNumber", "")).strip()

        if not aggrNumber:
            return jsonify({"error": "Agreement number is required"}), 400

        session = connection()
        if not session:
            return jsonify({"error": "SAP session not established"}), 500

        results = getExcelData(session, aggrNumber)

        if not results:
            return jsonify({
                "error": f"No material data found for Agreement Number {aggrNumber}"
            }), 404

        return jsonify({
            "results": results,
            "status": "Completed"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

# @app.route("/update", methods=["POST"])
# def updates():
#     results = []
#     uploaded_file = request.files.get("file")
#     if uploaded_file is None:
#         return jsonify({"error": "No file uploaded"}), 400

#     try:
#         df = pd.read_csv(uploaded_file)
#         df.columns = [col.strip() for col in df.columns]
#     except Exception as e:
#         return jsonify({"error": f"Error reading Excel/CSV: {e}"}), 400

#     required_columns = ['Material', 'Delivery Date', 'Scheduled Quantity']
#     for col in required_columns:
#         if col not in df.columns:
#             return jsonify({"error": f"Missing column in Excel: {col}"}), 400

#     aggrNumber = str(request.form.get("aggrNumber", "")).strip()
#     if not aggrNumber:
#         return jsonify({"error": "Agreement number missing"}), 400

#     try:
#         session = connection()
#         gotoCode(session)
#         enterSchN(session, aggrNumber)
#         for _, row in df.iterrows():
#             material = str(row['Material']).strip()
#             delv_date = str(row['Delivery Date']).strip().zfill(7)
#             print(delv_date)
#             qty = str(row['Scheduled Quantity']).strip()

#             try:
#                 gotoCode(session)
#                 enterSchN(session, aggrNumber)
                
#                 gotoMat(session,material)
#                 result = update(session)
#                 results.append({"material": material,  "status": "Updated", "result": result})
#             except Exception as e:
#                 results.append({"material": material, "status": "Failed", "error": str(e)})

#         return jsonify({"results": results, "status": "Update Completed"}), 200
#     except Exception as e:
#         return jsonify({
#             "error": str(e),
#             "traceback": traceback.format_exc()
#         }), 500

    

# ▶️ Run the Flask App
if __name__ == "__main__":
    app.run(debug=True, port=5050, host='0.0.0.0', use_reloader=False)
