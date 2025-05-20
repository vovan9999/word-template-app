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
        job_title = request.form['job_title']

        # === Обробка ПІБ: отримуємо short_name ===
        parts = name.strip().split()
        if len(parts) >= 3:
            lastname = parts[0]
            initials = f"{parts[1][0]}.{parts[2][0]}."
            short_name = f"{lastname} {initials}"
        else:
            short_name = name  # fallback якщо щось не так

        # Завантаження шаблону
        doc = DocxTemplate(template_name)
        context = {
            'name': name,
            'position': position,
            'number': number,
            'date': date,
            'short_name': short_name,
            'job_title': job_title,
            }
        doc.render(context)

        # Створення тимчасового .docx
        temp_docx = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
        doc.save(temp_docx.name)

        return send_file(temp_docx.name, as_attachment=True, download_name="zayava_na_vidpustky.docx")

    return render_template('form.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)