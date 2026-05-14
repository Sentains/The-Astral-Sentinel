from flask import Flask, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html', title="Заготовка")

@app.route('/training/<prof>')
def training_of_fly(prof):
    params = {'prof': prof, 'title': 'Тренинг'}
    return render_template('training_of_fly.html', **params)

@app.route('/list_prof/<list>')
def list_prof(list):
    professions = ['инженер-исследователь',
                   'пилот',
                   'строитель',
                   'экзобиолог',
                   'врач',
                   'инженер по терраформированию',
                   'климатолог',
                   'специалист по радиационной защите',
                   'астрогеолог',
                   'гляциолог',
                   'инженер жизнеобеспечения',
                   'метеоролог',
                   'оператор марсохода',
                   'киберинженер',
                   'штурман',
                   'пилот дронов',
                   ]
    return render_template('list_of_professions.html', professions=professions, type_list=list)


if __name__ == "__main__":
    app.run(port=8080, host='127.0.0.1')