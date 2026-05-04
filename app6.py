import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import calendar

# -------------------- CONFIG --------------------
st.set_page_config(page_title="D'tale Learning Center", layout="wide")

# -------------------- UI DESIGN --------------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: white;
    }
    .main-card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 15px;
    }
    h1, h2, h3 {
        color: #f1f5f9;
    }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "registrations.csv"
RECEIPT_FOLDER = "receipts"
os.makedirs(RECEIPT_FOLDER, exist_ok=True)

# -------------------- SESSION --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "student_logged_in" not in st.session_state:
    st.session_state.student_logged_in = False

# -------------------- ADMIN --------------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Arabinda@1234"

# -------------------- DATA INIT --------------------
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        "Reg ID","Name","DOB","Gender","Phone","Email","Address",
        "Class","Institution","Board",
        "Course","Mode","Batch",
        "Guardian Name","Guardian Phone","Relation",
        "Fee Submitted","Amount","Payment Mode","Transaction ID","Payment Date",
        "Username","Password",
        "Fee Month"
    ])
    df.to_csv(DATA_FILE, index=False)

# -------------------- REG ID --------------------
COUNTER_FILE = "counter.txt"

if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("1")

def generate_reg_id():
    with open(COUNTER_FILE, "r") as f:
        num = int(f.read().strip())

    reg_id = f"DL-2026-{str(num).zfill(3)}"

    with open(COUNTER_FILE, "w") as f:
        f.write(str(num + 1))

    return reg_id

# -------------------- NAME --------------------
def get_first_name(full_name):
    return full_name.strip().split(" ")[0]

# -------------------- PDF --------------------
def generate_pdf(data):
    filename = f"{data['Reg ID']}.pdf"
    filepath = f"{RECEIPT_FOLDER}/{filename}"

    doc = SimpleDocTemplate(filepath, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("<b>D’TALE LEARNING CENTER</b>", styles['Title']))
    content.append(Paragraph("Computer Science Department", styles['Normal']))
    content.append(Paragraph("Registration Receipt (FY 2026–27)", styles['Heading2']))
    content.append(Spacer(1, 15))

    # ---------------- WELCOME LETTER (MERGED FINAL VERSION) ----------------
    student_name = data["Name"]
    student_class = data["Class"]

    first_name = student_name.strip().split()[0]

    welcome_text = f"""
    Dear {student_name},<br/><br/>

    Welcome to D'tale Learning Center.<br/><br/>

    We are pleased to have you enrolled in {student_class}. Your registration has been successfully completed. We are committed to supporting your learning journey and helping you achieve your academic goals.<br/><br/>

    Your login credentials are as follows:<br/>
    User ID: {first_name}<br/>
    Password: {first_name}@007<br/><br/>

    We look forward to a productive and successful learning experience with you.<br/><br/>

    Warm regards,<br/>
    D'tale Learning Center
    """

    content.append(Paragraph(welcome_text, styles['Normal']))
    content.append(Spacer(1, 15))

    # ---------------- STUDENT TABLE ----------------
    table_data = [
        ["Registration ID", data["Reg ID"]],
        ["Name", data["Name"]],
        ["Class", data["Class"]],
        ["Course", data["Course"]],
        ["Phone", data["Phone"]],
        ["Mode", data["Mode"]],
        ["Batch", data["Batch"]],
    ]

    table = Table(table_data, colWidths=[160, 300])
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (0,-1), colors.lightgrey),
    ]))

    content.append(table)
    content.append(Spacer(1, 15))

    # ---------------- PAYMENT TABLE ----------------
    fee_data = [
        ["Description", "Details"],
        ["Registration Fee", data["Amount"]],
        ["Payment Mode", data["Payment Mode"]],
        ["Transaction ID", data["Transaction ID"]],
        ["Status", data["Fee Submitted"]],
        ["Fee Month", data["Fee Month"]]
    ]

    fee_table = Table(fee_data, colWidths=[250, 210])
    fee_table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ]))

    content.append(fee_table)
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Date: {datetime.now().strftime('%d-%m-%Y')}", styles['Normal']))
    content.append(Spacer(1, 30))

    doc.build(content)
    return filepath

# -------------------- HEADER --------------------
st.title("D’TALE LEARNING CENTER")
st.caption("Computer Science Department • Student Registration (FY 2026–27)")
st.divider()

# -------------------- FORM --------------------
st.markdown('<div class="main-card">', unsafe_allow_html=True)

name = st.text_input("Full Name")
dob = st.date_input("Date of Birth", min_value=date(1900, 1, 1), max_value=date.today())
gender = st.selectbox("Gender", ["Male","Female","Other"])
phone = st.text_input("Phone")
email = st.text_input("Email")
address = st.text_area("Address")

student_class = st.selectbox("Class / Course", [
    "Class 6","Class 7","Class 8","Class 9","Class 10",
    "Class 11","Class 12",
    "BCA - 1st Year","BCA - 2nd Year","BCA - 3rd Year","BCA - 4th Year","BCA - 5th Year",
    "Bsc - 1st Year","Bsc - 2nd Year","Bsc - 3rd Year","Bsc - 4th Year","Bsc - 5th Year",
    "MCA - 1st Year","MCA - 2nd Year","MCA - 3rd Year","MCA - 4th Year",
    "B.Tech - 1st Year","B.Tech - 2nd Year","B.Tech - 3rd Year","B.Tech - 4th Year",
    "M.Tech - 1st Year","M.Tech - 2nd Year","M.Tech - 3rd Year","M.Tech - 4th Year",
])

institution = st.text_input("School / College")
board = st.text_input("Board / University")

course = st.text_input("Course Name")
mode = st.selectbox("Mode", ["Offline","Online"])
batch = st.selectbox("Batch", ["Morning","Afternoon","Evening"])

guardian_name = st.text_input("Guardian Name")
guardian_phone = st.text_input("Guardian Phone")
relation = st.text_input("Relation")

fee_submitted = st.radio("Registration Fee Submitted", ["Yes","No"])
amount = st.text_input("Amount")

txn_id = ""
payment_mode = "Cash"
payment_date = date.today()
current_month = datetime.now().strftime("%B %Y")

if fee_submitted == "No":
    payment_mode = st.selectbox("Payment Mode", ["Cash", "UPI"])

    if payment_mode == "UPI":
        st.info("Scan QR to pay")
        qr_path = os.path.join(os.getcwd(), "qr.jpeg")
        if os.path.exists(qr_path):
            st.image(qr_path, width=220)
        txn_id = st.text_input("Enter UPI Transaction ID")
    else:
        txn_id = st.text_input("Transaction ID")

    payment_date = st.date_input("Payment Date", value=date.today())

submit = st.button("Submit")

st.markdown('</div>', unsafe_allow_html=True)

# -------------------- SUBMIT --------------------
if submit:
    reg_id = generate_reg_id()

    first_name = get_first_name(name)
    username = first_name
    password = f"{first_name}@007"

    record = {
        "Reg ID": reg_id,
        "Name": name,
        "DOB": dob,
        "Gender": gender,
        "Phone": phone,
        "Email": email,
        "Address": address,
        "Class": student_class,
        "Institution": institution,
        "Board": board,
        "Course": course,
        "Mode": mode,
        "Batch": batch,
        "Guardian Name": guardian_name,
        "Guardian Phone": guardian_phone,
        "Relation": relation,
        "Fee Submitted": fee_submitted,
        "Amount": amount,
        "Payment Mode": payment_mode,
        "Transaction ID": txn_id,
        "Payment Date": payment_date,
        "Username": username,
        "Password": password,
        "Fee Month": current_month
    }

    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    pdf_path = generate_pdf(record)

    st.success(f"Submitted Successfully! Your ID: {reg_id}")
    st.info(f"Login → {username} / {password}")

    with open(pdf_path, "rb") as f:
        st.download_button("Download Receipt", f, file_name=f"{reg_id}.pdf")

# -------------------- STUDENT LOGIN --------------------
st.sidebar.title("Student Login")

df = pd.read_csv(DATA_FILE)

if not st.session_state.student_logged_in:
    s_user = st.sidebar.text_input("Student Username")
    s_pass = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login as Student"):
        match = df[(df["Username"] == s_user) & (df["Password"] == s_pass)]

        if not match.empty:
            st.session_state.student_logged_in = True
            st.session_state.student_user = s_user
            st.sidebar.success("Student Logged In")
        else:
            st.sidebar.error("Invalid Student Credentials")
else:
    st.sidebar.success("Student Active")

# -------------------- DASHBOARD --------------------
if st.session_state.student_logged_in:
    st.subheader("Student Dashboard")

    student_data = df[df["Username"] == st.session_state.student_user]

    if not student_data.empty:
        latest = student_data.iloc[-1]
        status = "PAID" if latest["Fee Submitted"] == "Yes" else "DUE"

        st.markdown(f"### Fee Status: {status}")
        st.dataframe(student_data)


# -------------------- ADMIN --------------------
st.sidebar.title("Admin Login")

if not st.session_state.logged_in:
    username = st.sidebar.text_input("Admin Username")
    password = st.sidebar.text_input("Admin Password", type="password")

    if st.sidebar.button("Login Admin"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.sidebar.success("Admin Logged In")
        else:
            st.sidebar.error("Invalid credentials")
else:
    st.sidebar.success("Admin Active")

# -------------------- ADMIN PANEL CONTROLS --------------------
if st.session_state.logged_in:

    show_data = st.sidebar.checkbox("Show All Students")

    if show_data:
        st.subheader("All Student Records")
        st.dataframe(df, use_container_width=True)

        st.download_button(
            "Download Data",
            df.to_csv(index=False),
            "students_data.csv",
            "text/csv"
        )

        st.divider()

        # ---------------- DELETE SECTION ----------------
        st.subheader("Delete Student Record")

        reg_id_to_delete = st.text_input("Enter Registration ID to Delete")
        confirm_delete = st.checkbox("I confirm deletion")

        if st.button("Delete Record"):
            if confirm_delete:
                if reg_id_to_delete in df["Reg ID"].values:
                    df = df[df["Reg ID"] != reg_id_to_delete]
                    df.to_csv(DATA_FILE, index=False)
                    st.success(f"Record {reg_id_to_delete} deleted successfully")
                else:
                    st.error("Registration ID not found")
            else:
                st.warning("Please confirm deletion first")
