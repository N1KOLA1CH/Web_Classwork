from flask import Flask, url_for, request, redirect

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return 'И на Марсе будут яблони цвести!'


@app.route('/promotion')
def promotion():
    sp = [
        'Человечество вырастает из детства.',
        'Человечеству мала одна планета.',
        'Мы сделаем обитаемыми безжизненные пока планеты.',
        'И начнем с Марса!',
        'Присоединяйся!'
    ]
    return '</br>'.join(sp)


@app.route('/image_mars')
def image_mars():
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>Привет, Марс!</title>
                  </head>
                  <body>
                    <h1>Жди нас, Марс!</h1>
                    <img src="{url_for('static', filename='img/mars.jpg')}"
                     alt="здесь должна была быть картинка, но не нашлась">
                    <div>Вот она какая, красная планета.</div>
                  </body>
                </html>'''


@app.route('/promotion_image')
def promotion_image():
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet" 
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                    <title>Колонизация</title>
                  </head>
                  <body>
                    <h1 class="red-title">Жди нас, Марс!</h1>
                    <img src="{url_for('static', filename='img/mars.jpg')}" 
                     alt="здесь должна была быть картинка, но не нашлась">
                    <div class="alert alert-dark" role="alert">Человечество вырастает из детства.</div>
                    <div class="alert alert-success" role="alert">Человечеству мала одна планета.</div>
                    <div class="alert alert-secondary" role="alert">Мы сделаем обитаемыми безжизненные пока планеты.</div>
                    <div class="alert alert-warning" role="alert">И начнем с Марса!</div>
                    <div class="alert alert-danger" role="alert">Присоединяйся!</div>
                  </body>
                </html>'''


@app.route('/astronaut_selection', methods=['POST', 'GET'])
def astronaut_selection():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Отбор астронавтов</title>
                          </head>
                          <body>
                            <h1 align="center">Анкета претендента</h1>
                            <h4 align="center">на участие в миссии</h4>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="text" class="form-control" placeholder="Введите фамилию" name="surname">
                                    <input type="text" class="form-control" placeholder="Введите имя" name="name">
                                    <br>
                                    <input type="email" class="form-control" placeholder="Введите адрес почты" name="email">

                                    <div class="form-group">
                                        <label for="eduSelect">Какое у Вас образование?</label>
                                        <select class="form-control" id="eduSelect" name="education">
                                          <option>Начальное</option>
                                          <option>Среднее</option>
                                          <option>Высшее</option>
                                        </select>
                                     </div>

                                    <div class="form-group">
                                        <label>Какие у Вас есть профессии?</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" name="job" id="job1">
                                          <label class="form-check-label" for="job1">Инженер-исследователь</label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" name="job" id="job2">
                                          <label class="form-check-label" for="job2">Инженер-строитель</label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" name="job" id="job3">
                                          <label class="form-check-label" for="job3">Пилот</label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" name="job" id="job4">
                                          <label class="form-check-label" for="job4">Метеоролог</label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" name="job" id="job5">
                                          <label class="form-check-label" for="job5">Инженер по жизнеобеспечению</label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" name="job" id="job6">
                                          <label class="form-check-label" for="job6">Инженер по радиационной защите</label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" name="job" id="job7">
                                          <label class="form-check-label" for="job7">Врач</label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" name="job" id="job8">
                                          <label class="form-check-label" for="job8">Экзобиолог</label>
                                        </div>
                                    </div>

                                    <div class="form-group">
                                        <label>Укажите пол</label>
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
                                        <label for="motivation">Почему Вы хотите принять участие в миссии?</label>
                                        <textarea class="form-control" id="motivation" rows="3" name="motivation"></textarea>
                                    </div>

                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>

                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="stay" name="stay">
                                        <label class="form-check-label" for="stay">Готовы остаться на Марсе?</label>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        return 'Форма отправлена'


@app.route('/choice/<planet_name>')
def choice(planet_name):
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet"
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                    crossorigin="anonymous">
                    <title>Варианты выбора</title>
                  </head>
                  <body>
                    <h1>Мое предложение: {planet_name}</h1>
                    <h3>Эта планета близка к Земле;</h3>
                    <div class="alert alert-success" role="alert">
                      На ней много необходимых ресурсов;
                    </div>
                    <div class="alert alert-secondary" role="alert">
                      На ней есть вода и атмосфера;
                    </div>
                    <div class="alert alert-warning" role="alert">
                      На ней есть небольшое магнитное поле;
                    </div>
                    <div class="alert alert-danger" role="alert">
                      Наконец, она просто красива!
                    </div>
                  </body>
                </html>'''


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def results(nickname, level, rating):
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
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
                      <h4>Поздравляем! Ваш рейтинг после {level} этапа отбора</h4>
                    </div>
                    <h4>составляет {rating}!</h4>
                    <div class="alert alert-warning" role="alert">
                      <h4>Желаем удачи!</h4>
                    </div>
                  </body>
                </html>'''


@app.route('/load_photo', methods=['POST', 'GET'])
def load_photo():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang='en'>
                          <head>
                            <meta charset='utf-8'>
                            <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>
                            <link rel='stylesheet'
                            href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css'>
                            <link rel='stylesheet' type='text/css' href='{url_for('static', filename='css/style.css')}' />
                            <title>Отбор астронавтов</title>
                          </head>
                          <body>
                            <h1 align='center'>Загрузка фотографии</h1>
                            <h4 align='center'>для участия в миссии</h4>
                            <div class='container'>
                                <form class='load_form' method='post' enctype='multipart/form-data'>
                                    <div class='form-group'>
                                        <label for='photo'>Приложите фотографию</label>
                                        <input type='file' class='form-control-file' id='photo' name='file'>
                                    </div>
                                    <img src='{url_for('static', filename='img/photo.png')}' alt='Фото' style='max-width: 100%; margin-top: 10px;'>
                                    <br>
                                    <button type='submit' class='btn btn-primary mt-3'>Отправить</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        f = request.files['file']
        if f:
            f.save('static/img/photo.png')
        return redirect(url_for('load_photo'))


@app.route('/carousel')
def carousel():
    return f'''<!doctype html>
                <html lang='en'>
                  <head>
                    <meta charset='utf-8'>
                    <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>
                    <link rel='stylesheet'
                    href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css'
                    integrity='sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1'
                    crossorigin='anonymous'>
                    <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js' 
                    integrity='sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW' 
                    crossorigin='anonymous'></script>
                    <link rel='stylesheet' type='text/css' href='{url_for('static', filename='css/style.css')}' />
                    <title>Пейзажи Марса</title>
                  </head>
                  <body>
                    <h1 align='center'>Пейзажи Марса</h1>
                    <div id='carouselExampleIndicators' class='carousel slide' data-bs-ride='carousel'>
                      <div class='carousel-indicators'>
                        <button type='button' data-bs-target='#carouselExampleIndicators' data-bs-slide-to='0' class='active' aria-current='true' aria-label='Slide 1'></button>
                        <button type='button' data-bs-target='#carouselExampleIndicators' data-bs-slide-to='1' aria-label='Slide 2'></button>
                        <button type='button' data-bs-target='#carouselExampleIndicators' data-bs-slide-to='2' aria-label='Slide 3'></button>
                      </div>
                      <div class='carousel-inner'>
                        <div class='carousel-item active'>
                          <img src='{url_for('static', filename='img/mars1.jpg')}' class='d-block w-100' alt='Mars 1'>
                        </div>
                        <div class='carousel-item'>
                          <img src='{url_for('static', filename='img/mars2.jpg')}' class='d-block w-100' alt='Mars 2'>
                        </div>
                        <div class='carousel-item'>
                          <img src='{url_for('static', filename='img/mars3.jpg')}' class='d-block w-100' alt='Mars 3'>
                        </div>
                      </div>
                      <button class='carousel-control-prev' type='button' data-bs-target='#carouselExampleIndicators' data-bs-slide='prev'>
                        <span class='carousel-control-prev-icon' aria-hidden='true'></span>
                        <span class='visually-hidden'>Previous</span>
                      </button>
                      <button class='carousel-control-next' type='button' data-bs-target='#carouselExampleIndicators' data-bs-slide='next'>
                        <span class='carousel-control-next-icon' aria-hidden='true'></span>
                        <span class='visually-hidden'>Next</span>
                      </button>
                    </div>
                  </body>
                </html>'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
