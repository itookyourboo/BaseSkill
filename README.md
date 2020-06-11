# BaseSkill
Фреймворк для разработки навыков Алисы на Python<br>
❗️ Адаптирован под хостинг PythonAnyWhere ❗️

## А как он в плане...?
Вот пример навыка, реализованного на данном фреймворке<br>
GitHub - https://github.com/itookyourboo/animal-names<br>
Алиса - https://dialogs.yandex.ru/store/skills/9a733c88-imya-dlya-pitom

## Как использовать
Создаём папку test_skill, в которой будут храниться все файлы вашего навыка

### states.py
Содержит enum-класс, в котором прописаны состояния/уровни/комнаты (как хотите, так и называйте)

### strings.py
Содержит все строковые ресурсы, чтобы избавиться от хардкода в главном файле

### main.py (пример):

#### Паспорт навыка
```python
class TestSkill(BaseSkill):
    name = 'test_skill'
    command_handler = handler
```

#### Обработка команд
```python
handler = CommandHandler()

# Приветственное сообщение
@handler.hello_command
def hello(req, res, session):
    res.text = 'Привет'
    session['state'] = State.MENU
    
# Обработка токенов
# Есть заготовленные команды
@handler.command(words=['да', 'ага'], states=State.MENU)
def yes(req, res, session):
    res.text = 'Вы ответили положительно'
    session['state'] = State.PLAY
    
# Обработка пользовательского ввода
# Когда нет заготовленных команд
@handler.undefined_command(states=State.PLAY)
def play(req, res, session):
    if YOUR_WORD in req.tokens:
        res.text = 'Молодец!'
    else:
        res.text = 'Подумай ещё'
```

#### flask_app.py
Здесь импортируем все наши навыки и кладём их в SKILLS
```
from test_skill import TestSkill
from another_skill import AnotherSkill
...

SKILLS = [TestSkill(), AnotherSkill(), ...]
```
