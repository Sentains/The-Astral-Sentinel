from flask import Flask, url_for, request

app = Flask(__name__)


@app.route('/')
def main():
    return "Миссия Колонизация Марса"


@app.route('/index')
def index():
    return "И на Марсе будут яблони цвести!"


@app.route('/promotion')
def promotion():
    return (
        "Человечество вырастает из детства.<br>"
        "Человечеству мала одна планета.<br>"
        "Мы сделаем обитаемыми безжизненные пока планеты.<br>"
        "И начнем с Марса!<br>"
        "Присоединяйся!"
    )


@app.route('/image_mars')
def image_mars():
    mars_img_url = url_for('static', filename='img/mars.png')
    return f'''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Привет, Марс!</title>
      </head>
      <body>
        <h1>Жди нас, Марс!</h1>
        <img src="{mars_img_url}" alt="здесь должна была быть картинка, но не нашлась">
        <p>Вот она какая, красная планета.</p>
      </body>
    </html>
    '''


@app.route('/promotion_image')
def promotion_image():
    mars_img_url = url_for('static', filename='img/mars.png')
    return f'''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewpoint" content="width-device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
        crossorigin="anonymous">
        <link rel="stylesheet" type="text/css" href="{url_for(
        'static', filename='css/style.css')}" />
        <title>Колонизация</title>
      </head>
      <body>
        <h1>Жди нас, Марс!</h1>
        <img src="{mars_img_url}" alt="здесь должна была быть картинка, но не нашлась">
        <div class="alert alert-dark" role="alert">
        Человечество вырастает из детства.
        </div>
        <div class="alert alert-success" role="alert">
        Человечеству мала одна планета.
        </div>
        <div class="alert alert-dark" role="alert">
        Мы сделаем обитаемыми безжизненные пока планеты.
        </div>
        <div class="alert alert-warning" role="alert">
        И начнем с Марса!
        </div>
        <div class="alert alert-danger" role="alert">
        Присоединяйся!
        </div>
      </body>
    </html>
    '''


@app.route('/astronaut_selection', methods=['POST', 'GET'])
def astronaut_selection():
    if request.method == 'GET':
        return f'''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link rel="stylesheet"
            href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
            integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
            crossorigin="anonymous">
            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
            <title>Отбор астронавтов</title>
          </head>
          <body>
            <h1>Анкета претендента</h1>
            <h3>на участие в миссии</h3>
            <form class="login_form" method="post">
            	<input type="text" class="form-control" id="surname" placeholder="Введите фамилию" name="surname">
                <input type="text" class="form-control" id="name" placeholder="Введите имя" name="name">
                <label for="classSelect"></label>
                <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                <div class="form-group">
                	<label for="classSelect">Какое у Вас образование?</label>
                    <select class="form-control" id="education" name="education">
                      <option>Начальное</option>
                      <option>Среднее</option>
                      <option>Высшее</option>
                    </select>
                </div>
                <label for="classSelect"></label>
                <label for="classSelect">Какие у Вас есть профессии?</label>
                <div class="form-group form-check">
                    <input type="checkbox" class="form-check-input" id="acceptRules1" name="ing_iss" />
                    <label class="form-check-label" for="acceptRules1">Инженер-исследователь</label>
                </div>
                <div class="form-group form-check">
                    <input type="checkbox" class="form-check-input" id="acceptRules2" name="ing_str" />
                    <label class="form-check-label" for="acceptRules2">Инженер-строитель</label>
                </div>
                <div class="form-group form-check">
                    <input type="checkbox" class="form-check-input" id="acceptRules3" name="pil" />
                    <label class="form-check-label" for="acceptRules3">Пилот</label>
                </div>
                <div class="form-group form-check">
                    <input type="checkbox" class="form-check-input" id="acceptRules4" name="met" />
                    <label class="form-check-label" for="acceptRules4">Метеоролог</label>
                </div>
                <div class="form-group form-check">
                    <input type="checkbox" class="form-check-input" id="acceptRules5" name="ing_alive" />
                    <label class="form-check-label" for="acceptRules5">Инженер по жизнеобеспечению</label>
                </div>
                <div class="form-group form-check">
                    <input type="checkbox" class="form-check-input" id="acceptRules6" name="ing_radiac" />
                    <label class="form-check-label" for="acceptRules6">Инженер по радиоционной защите</label>
                </div>
                <div class="form-group form-check">
                    <input type="checkbox" class="form-check-input" id="acceptRules7" name="doctor" />
                    <label class="form-check-label" for="acceptRules7">Врач</label>
                </div>
                <div class="form-group form-check">
                    <input type="checkbox" class="form-check-input" id="acceptRules8" name="exobiologer" />
                    <label class="form-check-label" for="acceptRules8">Экзобиолог</label>
                </div>
                <label for="classSelect"></label>
                <div class="form-group">
                    <label for="form-check">Укажите пол</label>
                    <div class="form-check">
                      <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                      <label class="form-check-label" for="male">Мужской</label>
                    </div>
                    <div class="form-check">
                      <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                      <label class="form-check-label" for="female">Женский</label>
                    </div>
                </div>
                <div class="form-group">
                    <label for="about">Почему вы хотите принять участие в миссии?</label>
                    <textarea class="form-control" id="answer" rows="3" name="answer"></textarea>
                </div>
                <div class="form-group">
                    <label for="photo">Приложите фотографию</label>
                    <input type="file" class="form-control-file" id="photo" name="file">
                </div>
                <div class="form-group form-check">
                    <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                    <label class="form-check-label" for="acceptRules">Готовы ли остаться на Марсе?</label>
                </div>
                <button type="submit" class="btn btn-primary">Отправить</button>
            </form>
          </body>
        </html>
        '''
    elif request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        email = request.form['email']
        education = request.form['education']
        sex = request.form['sex']
        answer = request.form['answer']
        accept = 'Да' if 'accept' in request.form else 'Нет'

        return f'''
            Полученные данные:
            - Фамилия: {surname}
            - Имя: {name}
            - Email: {email}
            - Образование: {education}
            - Пол: {sex}
            - Причина участия: {answer}
            - Готовность остаться на Марсе: {accept}
            '''


@app.route('/choice/<planet_name>')
def choice(planet_name):
    types_of_alert = ['alert-success', 'alert-dark', 'alert-danger', 'alert-warning']
    planets_description = {
        'марс': [
            ('Эта планета близка к Земле', 1),
            ('На ней много ресурсов', 2),
            ('На ней есть вода и атмосфера', 3),
            ('На есть небольшое магнитное поле', 4),
            ('Наконец, она просто красива!', 1)
        ],
        'земля': [
            ('Это наша родная планета', 1),
            ('Здесь есть жизнь', 2),
            ('Имеет богатую флору и фауну', 1),
            ('Обладает атмосферой, подходящей для человека', 3),
            ('Земля — единственная известная планета с водой в жидком состоянии', 4)
        ],
        'венера': [
            ('Это самая горячая планета', 1),
            ('Имеет очень плотную атмосферу', 2),
            ('Поверхность покрыта вулканами', 3),
            ('Венера вращается в обратную сторону', 2),
            ('На Венере постоянно тёмно и жарко', 4)
        ],
        'юпитер': [
            ('Это газовый гигант', 1),
            ('Обладает самой сильной гравитацией среди планет', 2),
            ('Имеет множество спутников, включая Ганимед', 3),
            ('На Юпитере постоянно штормы, подобные Большому красному пятну', 4),
            ('Юпитер — самая большая планета в нашей солнечной системе', 1)
        ],
        'сатурн': [
            ('Известен своими великолепными кольцами', 1),
            ('Это газовый гигант', 4),
            ('Имеет множество спутников, включая Титан', 3),
            ('Планета очень холодная и ветреная', 2),
            ('Сатурн — шестая планета от Солнца', 1)
        ],
        'меркурий': [
            ('Самая близкая к Солнцу планета', 1),
            ('Очень горячая днем и очень холодная ночью', 2),
            ('На поверхности много кратеров', 4),
            ('Меркурий очень маленький и плотный', 2),
            ('На Меркурии почти нет атмосферы', 3)
        ],
        'нептун': [
            ('Это самая дальняя планета в нашей системе', 1),
            ('Обладает очень холодной атмосферой', 2),
            ('Имеет сильные ветры и штормы', 3),
            ('Есть спутник Тритон, покрытый гейзами', 4),
            ('Нептун — ледяной гигант', 1)
        ],
    }

    if planet_name.lower() not in planets_description:
        return f'<h2>По вашему выбору ({planet_name}) ничего не нашлось</h2>'
    description = planets_description[planet_name.lower()]
    styles = list(map(lambda x: types_of_alert[x[1] - 1], description))
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet" 
                    href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" 
                    integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" 
                    crossorigin="anonymous">
                    <title>Варианты выбора</title>
                  </head>
                  <body>
                    <h1>Моё предложение: {planet_name}</h1>
                    <div class="alert {styles[0]}" role="alert">
                      <h5>{description[0][0]}</h5>
                    </div>
                    <div class="alert {styles[1]}" role="alert">
                      <h5>{description[1][0]}</h5>
                    </div>
                    <div class="alert {styles[2]}" role="alert">
                      <h5>{description[2][0]}</h5>
                    </div>
                    <div class="alert {styles[3]}" role="alert">
                      <h5>{description[3][0]}</h5>
                    </div>
                    <div class="alert {styles[4]}" role="alert">
                      <h5>{description[4][0]}</h5>
                    </div>
                  </body>
                </html>'''


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def results(nickname, level, rating):
    return f'''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewpoint" content="width-device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
        crossorigin="anonymous">
        <title>Результаты</title>
      </head>
      <body>
        <h1>Результаты отбора</h1>
        <h2>Претендента на участие в миссии {nickname}:</h2>
        <div class="alert alert-success" role="alert">
          <h2>Поздравляем! Ваш рейтинг после {level} этапа отбора</h2>
        </div>
        <h2>составляет {rating}!</h2>
        <div class="alert alert-warning" role="alert">
          <h1>Желаем удачи!</h1>
        </div>
      </body>
    </html>
    '''


if __name__ == "__main__":
    app.run(port=8080, host='127.0.0.1')