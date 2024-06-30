from flask import Flask, render_template, request, redirect, url_for, session
import os
import PyPDF2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {}

def split_pdf(input_pdf, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf = PyPDF2.PdfFileReader(input_pdf)
    for page_num in range(pdf.getNumPages()):
        output = PyPDF2.PdfFileWriter()
        output.addPage(pdf.getPage(page_num))
        with open(os.path.join(output_dir, f'page_{page_num + 1}.pdf'), 'wb') as output_stream:
            output.write(output_stream)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        clocking_number = request.form['clocking_number']
        cell_number = request.form['cell_number']
        users[clocking_number] = cell_number
        with open('users.txt', 'a') as f:
            f.write(f'{clocking_number},{cell_number}\n')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        clocking_number = request.form['clocking_number']
        cell_number = request.form['cell_number']
        if clocking_number in users and users[clocking_number] == cell_number:
            session['clocking_number'] = clocking_number
            return redirect(url_for('timesheet'))
    return render_template('login.html')

@app.route('/timesheet')
def timesheet():
    if 'clocking_number' not in session:
        return redirect(url_for('login'))
    clocking_number = session['clocking_number']
    return render_template('timesheet.html', clocking_number=clocking_number)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        pdf_path = os.path.join('uploads', pdf_file.filename)
        pdf_file.save(pdf_path)
        split_pdf(pdf_path, 'output_pages')
    return render_template('admin.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
