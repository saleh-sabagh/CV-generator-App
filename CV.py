import sys
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable,Table, TableStyle
from reportlab.lib.pagesizes import A4
import os
import re
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton,QLineEdit, QTextEdit, QSpinBox,QVBoxLayout, QHBoxLayout, QMessageBox,QDialog)


def setup_database():
    conn = sqlite3.connect("resume_data.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        email TEXT,
        adress TEXT,
        university TEXT,
        major TEXT,
        graduation_year TEXT,
        job TEXT,
        company TEXT,
        start_date TEXT,
        finish_date TEXT,
        tasks TEXT,
        skills TEXT,
        certificates TEXT
    )
    """)
    
    conn.commit()
    conn.close()


def save_user_data(name ,phone,email ,adress ,university, major ,graduation_year ,job ,company ,start_date ,finish_date ,tasks,skills ,certificates):
    conn = sqlite3.connect("resume_data.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO user_data (name ,phone,email ,adress ,university, major ,graduation_year ,job ,company ,start_date ,finish_date ,tasks,skills ,certificates)
    VALUES (?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?)
    """, (name ,phone,email ,adress ,university, major ,graduation_year ,job ,company ,start_date ,finish_date ,tasks,skills ,certificates))
    
    conn.commit()
    conn.close()
   


def load_user_data():
    conn = sqlite3.connect("resume_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_data ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()

    conn.close()
    return data


def validate_data(name ,phone,email ,adress ,university, major ,graduation_year ,job ,company ,start_date ,finish_date ,tasks,skills ,certificates):
    
    if not name or not phone or not email or not adress or not university or not major or not graduation_year or not job or not company or not start_date or not skills or not finish_date or not certificates or not tasks:
        return False, "EMPTY FIELD EXISTS! "

 
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not re.match(email_regex, email):
        return False, "INCORRECT EMAIL FORMAT!"

    
    return True, "ALL THINGS RIGHT!"




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(550,150, 500, 600)
        self.setWindowTitle("RESUME CREATOR")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main=QVBoxLayout()
        
        name_layout=QHBoxLayout()
        number_layout=QHBoxLayout()
        email_layout=QHBoxLayout()
        adress_layout=QHBoxLayout()

        
        sp = QLabel("SPECIFICATION")
        sp.setStyleSheet("font-size: 20px;")
        main.addWidget(sp)
        self.name1=QLineEdit(self)
        self.number1=QLineEdit(self)
        self.email1=QLineEdit(self)
        self.adress1=QTextEdit(self)

       


        name=QLabel("NAME:")
        number=QLabel("PHONE NUMBER:")
        email=QLabel("EMAIL:")
        adress=QLabel("ADRESS")
        
        name_layout.addWidget(name)
        number_layout.addWidget(number)
        email_layout.addWidget(email)
        adress_layout.addWidget(adress)
        
        name_layout.addWidget(self.name1)
        number_layout.addWidget(self.number1)
        email_layout.addWidget(self.email1)
        adress_layout.addWidget(self.adress1)
        
        main.addLayout(name_layout)
        main.addLayout(number_layout)
        main.addLayout(email_layout)
        main.addLayout(adress_layout)
        

        grg_layout=QVBoxLayout()
        uni_layout=QHBoxLayout()
        field_layout=QHBoxLayout()
        gry_layout=QHBoxLayout()
        
        gr = QLabel("EDUCATION")
        gr.setStyleSheet("font-size: 20px;")
        grg_layout.addWidget(gr)

        uni=QLabel("UNIVERSITY:")
        self.uni2=QLineEdit(self)

        
        uni_layout.addWidget(uni)
        uni_layout.addWidget(self.uni2)

        field=QLabel("MAJOR:")
        self.field2=QLineEdit(self)

        field_layout.addWidget(field)
        field_layout.addWidget(self.field2)

        Grn_Year=QLabel("GRADUATION YEAR")
        self.Grn_Year2=QSpinBox(self)
        self.Grn_Year2.setRange(1360, 1403)  
        self.Grn_Year2.setValue(1390)        
    
        gry_layout.addWidget(Grn_Year)
        gry_layout.addWidget(self.Grn_Year2)
        

        grg_layout.addLayout(uni_layout)
        grg_layout.addLayout(field_layout)
        grg_layout.addLayout(gry_layout)
        main.addLayout(grg_layout)

        sbgh = QLabel("WORK EXPERENCE")
        sbgh.setStyleSheet("font-size: 20px;")
        grg_layout.addWidget(sbgh)

        main.addWidget(sbgh)

        l_o1=QHBoxLayout()
        l_o2=QHBoxLayout()
        l_o3=QHBoxLayout()
        l_o4=QHBoxLayout()
        l_o5=QHBoxLayout()

        w1=QLabel("JOB TITLE:")
        self.ww1=QLineEdit(self)
        
        l_o1.addWidget(w1)
        l_o1.addWidget(self.ww1)

        w2=QLabel("COMPANY NAME:")
        self.ww2=QLineEdit(self)
        
        l_o2.addWidget(w2)
        l_o2.addWidget(self.ww2)
        
        w3=QLabel("START JOB FROM:")
        self.spin_day = QSpinBox(self)
        self.spin_day.setRange(1, 31) 
        self.spin_day.setValue(1)  
        self.spin_day.setPrefix("DAY:")

        
        self.spin_month = QSpinBox(self)
        self.spin_month.setRange(1, 12)  
        self.spin_month.setValue(1)  
        self.spin_month.setPrefix("MONTH:")

       
        self.spin_year = QSpinBox(self)
        self.spin_year.setRange(1350, 2100)  
        self.spin_year.setValue(1400)  
        self.spin_year.setPrefix("YEAR:")

        l_o3.addWidget(w3)
        l_o3.addWidget(self.spin_year)
        l_o3.addWidget(self.spin_month)
        l_o3.addWidget(self.spin_day)

        w4=QLabel("FINISH JOB AT:")
        self.spin2_day = QSpinBox(self)
        self.spin2_day.setRange(1, 31)  
        self.spin2_day.setValue(1)  
        self.spin2_day.setPrefix("DAY:")

        
        self.spin2_month = QSpinBox(self)
        self.spin2_month.setRange(1, 12)  
        self.spin2_month.setValue(1)  
        self.spin2_month.setPrefix("MONTH:")

        
        self.spin2_year = QSpinBox(self)
        self.spin2_year.setRange(1360, 2100)  
        self.spin2_year.setValue(1400)  
        self.spin2_year.setPrefix("YEAR:")

        l_o5.addWidget(w4)
        l_o5.addWidget(self.spin2_year)
        l_o5.addWidget(self.spin2_month)
        l_o5.addWidget(self.spin2_day)
        
        
        w5=QLabel("TASKS:")
        self.ww5=QTextEdit(self)
        l_o4.addWidget(w5)
        l_o4.addWidget(self.ww5)

        layout1=QHBoxLayout()
        self.save_button1=QPushButton("TEMPORARY SAVE",self)
        self.save_button2=QPushButton("SAVE AND CONTINUE",self)
        self.save_button1.clicked.connect(self.save_data)
        self.save_button2.clicked.connect(self.save_final_data)

        skill_l=QHBoxLayout()
        s_label=QLabel("EXPERIENCES:")
        self.s_edit=QTextEdit(self)
        c_labbel=QLabel("CERTIFICATES:")
        self.c_edit=QTextEdit(self)

        skill_l.addWidget(s_label)
        skill_l.addWidget(self.s_edit)
        
        skill_l.addWidget(c_labbel)
        skill_l.addWidget(self.c_edit)
        
        

        layout1.addWidget(self.save_button1)
        layout1.addWidget(self.save_button2)

        main.addLayout(l_o1)
        main.addLayout(l_o2)
        main.addLayout(l_o3)
        main.addLayout(l_o5)
        main.addLayout(l_o4)

        main.addLayout(skill_l)
        main.addLayout(layout1)

        central_widget.setLayout(main)
        self.load_data()

    def load_data(self):
        data = load_user_data()

        if data:
            self.name1.setText(data[1])
            self.number1.setText(data[2])
            self.email1.setText(data[3])
            self.adress1.setText(data[4])
            self.uni2.setText(data[5])
            self.field2.setText(data[6])
            self.Grn_Year2.setValue(int(data[7]))
            self.ww1.setText(data[8])
            self.ww2.setText(data[9])

            start_job=data[10]
            year, month, day = map(int, start_job.split('-'))
            self.spin_year.setValue(year)
            self.spin_month.setValue(month)
            self.spin_day.setValue(day)
            
            finish_job=data[11]
            year2, month2, day2 = map(int, finish_job.split('-'))
            self.spin_year.setValue(year2)
            self.spin_month.setValue(month2)
            self.spin_day.setValue(day2)
            self.ww5.setText(data[12])
            self.s_edit.setText(data[13])
            self.c_edit.setText(data[14])
            

    def save_data(self):
        
        name=self.name1.text()
        phone= self.number1.text()
        email= self.email1.text()
        adress=self.adress1.toPlainText()
        university= self.uni2.text()
        major= self.field2.text()
        graduation_year= str(self.Grn_Year2.value())
        job= self.ww1.text()
        company= self.ww2.text()

        day = self.spin_day.value()        
        month = self.spin_month.value()    
        year = self.spin_year.value()      
        start_date = f"{year}-{month:02d}-{day:02d}"  

        day2 = self.spin2_day.value()        
        month2 = self.spin2_month.value()   
        year2 = self.spin2_year.value()      
        finish_date = f"{year2}-{month2:02d}-{day2:02d}"  
        tasks=self.ww5.toPlainText()
        skills=self.s_edit.toPlainText()
        certificates=self.c_edit.toPlainText()

        
        
        save_user_data(name ,phone,email ,adress ,university, major ,graduation_year ,job ,company ,start_date ,finish_date ,tasks,skills ,certificates)

        QMessageBox.information(self, "SAVED" ,"INFORMATION SAVED!")


    def save_final_data(self):
        
        name=self.name1.text()
        phone= self.number1.text()
        email= self.email1.text()
        adress=self.adress1.toPlainText()
        university= self.uni2.text()
        major= self.field2.text()
        graduation_year= str(self.Grn_Year2.value())
        job= self.ww1.text()
        company= self.ww2.text()

        day = self.spin_day.value()       
        month = self.spin_month.value()    
        year = self.spin_year.value()      
        start_date = f"{year}-{month:02d}-{day:02d}"  

        day2 = self.spin2_day.value()        
        month2 = self.spin2_month.value()   
        year2 = self.spin2_year.value()    
        finish_date = f"{year2}-{month2:02d}-{day2:02d}"  
        tasks=self.ww5.toPlainText()
        skills=self.s_edit.toPlainText()
        certificates=self.c_edit.toPlainText()


       
        valid, message = validate_data(name ,phone,email ,adress ,university, major ,graduation_year ,job ,company ,start_date ,finish_date ,tasks ,skills ,certificates)

        if valid:
           
            save_user_data(name ,phone,email ,adress ,university, major ,graduation_year ,job ,company ,start_date ,finish_date ,tasks,skills ,certificates)
            QMessageBox.information(self, "FINAL SAVE", "INFORMATION SAVED!")
            pdf_app = PDFApp()
            pdf_app.exec()
        else:
            QMessageBox.warning(self, "ERROR", message)

   
class PDFApp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Choose template!")
        self.setGeometry(600, 300, 400, 200)
        
        
        layout = QVBoxLayout()
        self.template1_btn = QPushButton("TEMPLATE1")
        self.template2_btn = QPushButton("TEMPLATE2")
        self.template3_btn = QPushButton("TEMPLATE3")
        layout.addWidget(self.template1_btn)
        layout.addWidget(self.template2_btn)
        layout.addWidget(self.template3_btn)
        self.setLayout(layout)
        
        
        self.template1_btn.clicked.connect(self.generate_template1)
        self.template2_btn.clicked.connect(self.generate_template2)
        self.template3_btn.clicked.connect(self.generate_template3)
    
    def fetch_data(self):
        conn = sqlite3.connect("resume_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_data ORDER BY id DESC LIMIT 1")
        data = cursor.fetchone()
        conn.close()
        return data

    def save_pdf(self, filename, content_func):
       
        filepath = os.path.join(os.getcwd(), filename)
        c = canvas.Canvas(filepath, pagesize=letter)
        content_func(c)
        c.save()

        
        QMessageBox.information(self, "CREATED", f"{filename} CREATED!")
        os.startfile(filepath)

    def generate_template1(self):
        data = self.fetch_data()
        
        person_info = {
        "name": data[1],
        "phone": data[2],
        "email": data[3],
        "address": data[4],
        "university": data[5],
        "major": data[6],
        "graduation_year": data[7],
        "job": data[8],
        "company": data[9],
        "start_date": data[10],
        "finish_date": data[11],
        "task": data[12],
        "skills": data[13],
        "certificates": data[14]
}
        
        
        doc = SimpleDocTemplate(f"{data[1]}_Resume1.pdf", pagesize=letter)
        elements = []


        styles = getSampleStyleSheet()
        heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.darkblue,
        alignment=1,  
)
        contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=2  
)
        section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.blue
)


        elements.append(Paragraph(f"<b><i>{person_info['name']}</i></b>", heading_style))
        elements.append(Spacer(1, 6))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        elements.append(Spacer(1, 12))


        contact_info = f"""
            <b>Name:</b> {person_info['name']}<br/>
            <b>Phone:</b> {person_info['phone']}<br/>
            <b>Email:</b> {person_info['email']}<br/>
            <b>Address:</b> {person_info['address']}
        """
        elements.append(Paragraph(contact_info, contact_style))
        elements.append(Spacer(1, 12))


        elements.append(Paragraph("Education", section_heading_style))
        elements.append(Paragraph(f"<b>University:</b> {person_info['university']}", styles['Normal']))
        elements.append(Paragraph(f"<b>Major:</b> {person_info['major']}", styles['Normal']))
        elements.append(Paragraph(f"<b>Graduation Year:</b> {person_info['graduation_year']}", styles['Normal']))
        elements.append(Spacer(1, 12))


        elements.append(Paragraph("Work Experience", section_heading_style))
        elements.append(Paragraph(f"<b>Job Title:</b> {person_info['job']}", styles['Normal']))
        elements.append(Paragraph(f"<b>Company:</b> {person_info['company']}", styles['Normal']))
        elements.append(Paragraph(f"<b>Start Date:</b> {person_info['start_date']}", styles['Normal']))
        elements.append(Paragraph(f"<b>Finish Date:</b> {person_info['finish_date']}", styles['Normal']))
        elements.append(Paragraph(f"<b>Task:</b> {person_info["task"]}", styles['Normal']))
        elements.append(Spacer(1, 12))


        elements.append(Paragraph("Skills", section_heading_style))
        elements.append(Paragraph(f"{person_info['skills']}", styles['Normal']))
        elements.append(Spacer(1, 12))


        elements.append(Paragraph("Certificates", section_heading_style))
        elements.append(Paragraph(f"{person_info['certificates']}", styles['Normal']))
        elements.append(Spacer(1, 12))


        doc.build(elements)

        QMessageBox.information(self, "CREATED", f"{data[1]}_Resume1.pdf CREATED!")
        os.startfile(f"{data[1]}_Resume1.pdf ")
      

    def generate_template2(self):
        data = self.fetch_data()
        
        person_info = {
        "name": data[1],
        "phone": data[2],
        "email": data[3],
        "address": data[4],
        "university": data[5],
        "major": data[6],
        "graduation_year": data[7],
        "job": data[8],
        "company": data[9],
        "start_date": data[10],
        "finish_date": data[11],
        "task": data[12],
        "skills": data[13],
        "certificates": data[14]
}

        doc = SimpleDocTemplate(f"{data[1]}_Resume2.pdf", pagesize=letter)
        elements = []

    
        styles = getSampleStyleSheet()
        name_style = ParagraphStyle(
        'Name',
        parent=styles['Heading1'],
        fontSize=24,  
        textColor=colors.darkblue,
        alignment=1,  
        spaceAfter=10
    )
        small_contact_style = ParagraphStyle(
            'SmallContact',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey
    )
        large_info_style = ParagraphStyle(
            'LargeInfo',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.darkblue
    )
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.darkblue,
            spaceBefore=10,
            spaceAfter=10
    )
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ])
        
        elements.append(Paragraph(person_info.get('name', 'N/A'), name_style))
        elements.append(Spacer(1, 12))   

    
        contact_info = f"""
        <b>Email:</b> {person_info.get('email', 'N/A')}<br/>
        <b>Phone:</b> {person_info.get('phone', 'N/A')}<br/>
        <b>Address:</b> {person_info.get('address', 'N/A')}
    """
        elements.append(Paragraph(contact_info, small_contact_style))
        elements.append(Spacer(1, 12))

   
        education_data = f"""
        <b>University:</b> {person_info.get('university', 'N/A')}<br/>
        <b>Major:</b> {person_info.get('major', 'N/A')}<br/>
        <b>Graduation Year:</b> {person_info.get('graduation_year', 'N/A')}
    """
        skills_data = f"""
        <b>Skills:</b><br/>
        {person_info.get('skills', 'N/A')}
    """
        columns_data = [[Paragraph(education_data, large_info_style), Paragraph(skills_data, large_info_style)]]
        elements.append(Table(columns_data, colWidths=[270, 270], hAlign='LEFT'))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Work Experience", subtitle_style))
        work_data = [
            ["Job Title", "Company", "Start Date", "Finish Date"],
            [
                person_info.get('job', 'N/A'),
                person_info.get('company', 'N/A'),
                person_info.get('start_date', 'N/A'),
                person_info.get('finish_date', 'N/A'),
            ]
    ]
        table = Table(work_data, colWidths=[130, 130, 100, 100])
        table.setStyle(table_style)
        elements.append(table)
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"<b>Task:</b> {person_info['task']}", styles['Normal']))
    
        elements.append(Paragraph("certificates", subtitle_style))
        elements.append(Paragraph(person_info.get("certificates", 'No certificates provided'), styles['Normal']))
        elements.append(Spacer(1, 12))

   
        doc.build(elements)
        QMessageBox.information(self, "CREATED", f"{data[1]}_Resume2.pdf CREATED!")
        os.startfile(f"{data[1]}_Resume2.pdf ")
      
    def generate_template3(self):
        data = self.fetch_data()
        
        person_info = {
        "name": data[1],
        "phone": data[2],
        "email": data[3],
        "address": data[4],
        "university": data[5],
        "major": data[6],
        "graduation_year": data[7],
        "job": data[8],
        "company": data[9],
        "start_date": data[10],
        "finish_date": data[11],
        "task": data[12],
        "skills": data[13],
        "certificates": data[14]
}

        doc = SimpleDocTemplate(f"{data[1]}_Resume3.pdf", pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        header_style = ParagraphStyle(
        'Header',
        parent=styles['Heading1'],
        fontSize=26,  
        textColor=colors.darkblue,
        alignment=0,  
        spaceAfter=20
)
        section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.white,
            backColor=colors.darkblue,
            alignment=0,  
            spaceBefore=10,
            spaceAfter=5,
            leftIndent=5,
    )
        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=5
    )

    
        elements.append(Paragraph(person_info.get('name', 'N/A'), header_style))
        elements.append(HRFlowable(width="100%", color=colors.darkblue))
        elements.append(Spacer(1, 20))

        contact_info = f"""
        <b>Email:</b> {person_info.get('email', 'N/A')} &nbsp;&nbsp;
        <b>Phone:</b> {person_info.get('phone', 'N/A')} &nbsp;&nbsp;
        <b>Address:</b> {person_info.get('address', 'N/A')}
    """
        elements.append(Paragraph(contact_info, body_style))
        elements.append(HRFlowable(width="100%", color=colors.grey))
        elements.append(Spacer(1, 10))

   
        elements.append(Paragraph("Education", section_title_style))
        education_data = f"""
        <b>University:</b> {person_info.get('university', 'N/A')}<br/>
        <b>Major:</b> {person_info.get('major', 'N/A')}<br/>
        <b>Graduation Year:</b> {person_info.get('graduation_year', 'N/A')}
    """
        elements.append(Paragraph(education_data, body_style))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("Skills", section_title_style))
        skills_data = person_info.get('skills', 'N/A').replace(',', ', ')
        elements.append(Paragraph(skills_data, body_style))
        elements.append(Spacer(1, 10))

  
        elements.append(Paragraph("Work Experience", section_title_style))
        work_data = [
            ["Job Title", "Company", "Start Date", "Finish Date"],
            [
            person_info.get('job', 'N/A'),
            person_info.get('company', 'N/A'),
            person_info.get('start_date', 'N/A'),
            person_info.get('finish_date', 'N/A'),
            ]
    ]
        table = Table(work_data, colWidths=[150, 150, 100, 100])
        table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
        elements.append(table)
   

        elements.append(Spacer(1, 10))
        task_text = person_info.get('task', 'No tasks provided.')
        elements.append(Paragraph(f"<b>Task:</b> {task_text}", body_style))
        elements.append(Spacer(1, 10))

   
 
        elements.append(Paragraph("Certificates", section_title_style))
        elements.append(Paragraph(person_info.get('certificates', 'No certificates provided'), body_style))
        elements.append(Spacer(1, 10))

   
        doc.build(elements)
        QMessageBox.information(self, "CREATED", f"{data[1]}_Resume3.pdf CREATED!")
        os.startfile(f"{data[1]}_Resume3.pdf ")

setup_database()
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

