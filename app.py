from flask import Flask, render_template, request, send_file
from docxtpl import DocxTemplate
import tempfile
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        number = request.form['number']
        date = request.form['date']
        template_name = request.form['template']

        # Завантаження шаблону
        doc = DocxTemplate(template_name)
        context = {'name': name, 'position': position, 'number': number, 'date': date}
        doc.render(context)

        # Створення тимчасового .docx
        temp_docx = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
        doc.save(temp_docx.name)

        return send_file(temp_docx.name, as_attachment=True, download_name="result.docx")

    return render_template('form.html')

if name == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)