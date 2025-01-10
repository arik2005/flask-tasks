from flask import Flask, render_template, request
import io
import sys

app = Flask(__name__)

# Список задач
tasks = [
    {
        "title": "print() деген не?",
        "explanation": """Python бағдарламалау тілінде `print()` — бұл экранға (немесе терминалға) мәтін, сан немесе басқа мәліметтерді шығару үшін қолданылатын функция. 
Қарапайым қолдану: жай ғана `print()` ішіне көрсету керек деректерді жазыңыз.""",
        "hint": """Мысалы: 
print("Сәлем, Әлем!")
Мәтінді қос тырнақшаға алып жазу керек.""",
        "expected_output": "Сәлем, Әлем!",
    },
    {
        "title": "Мәтін шығару",
        "explanation": "Экранға 'Сәлем, Әлем!' мәтінін шығарыңыз.",
        "hint": "Мысалы: print('Сәлем, Әлем!')",
        "expected_output": "Сәлем, Әлем!",
    },
    {
        "title": "Сан шығару",
        "explanation": "Экранға 2025 санын шығарыңыз.",
        "hint": "Мысалы: print(2025)",
        "expected_output": "2025",
    },
    {
        "title": "Екі санның қосындысын шығару",
        "explanation": "Экранға 15 пен 25 сандарының қосындысын шығарыңыз.",
        "hint": "Мысалы: print(15 + 25)",
        "expected_output": "40",
    },
    {
        "title": "Айырманы шығару",
        "explanation": "45 пен 20 сандарының айырмасын есептеп, экранға шығарыңыз.",
        "hint": "Мысалы: print(45 - 20)",
        "expected_output": "25",
    },
    {
        "title": "Көбейтінді шығару",
        "explanation": "6 мен 8 сандарының көбейтіндісін табыңыз.",
        "hint": "Мысалы: print(6 * 8)",
        "expected_output": "48",
    },
    {
        "title": "Бөлінді шығару",
        "explanation": "40-ты 8-ге бөліп, нәтижесін экранға шығарыңыз.",
        "hint": "Мысалы: print(40 / 8)",
        "expected_output": "5.0",
    },
    {
        "title": "Айнымалы мәнін шығару",
        "explanation": "Айнымалыны `x` деп құрыңыз және оған 100 мәнін беріп, оны экранға шығарыңыз.",
        "hint": "Мысалы: x = 100; print(x)",
        "expected_output": "100",
    },
    {
        "title": "Мәтін мен санды бірге шығару",
        "explanation": "'Жыл: 2025' деп экранға шығарыңыз.",
        "hint": "Мысалы: print('Жыл:', 2025)",
        "expected_output": "Жыл: 2025",
    },
    {
        "title": "Санның квадратын шығару",
        "explanation": "5 санының квадратын есептеп, экранға шығарыңыз.",
        "hint": "Мысалы: print(5 ** 2)",
        "expected_output": "25",
    },
]

# Главная страница
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks, score=0, current_task=0, message="")

# Обработка задач
@app.route('/task', methods=['POST'])
def task():
    current_task = int(request.form['current_task'])
    user_code = request.form['user_code']
    score = int(request.form['score'])

    try:
        # Перехват вывода print
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        # Выполнение кода ученика
        exec(user_code, globals())

        # Читаем вывод пользователя
        sys.stdout = old_stdout
        output = buffer.getvalue().strip()

        # Проверяем результат
        if str(output) == str(tasks[current_task]["expected_output"]):
            score += 1
            message = "✅ Дұрыс! Келесі тапсырмаға көшуге болады."
            current_task += 1  # Переход к следующей задаче
        else:
            message = f"❌ Қате. Дұрыс жауап: {tasks[current_task]['expected_output']}."
    except Exception as e:
        sys.stdout = old_stdout
        message = f"❌ Қате: {e}"

    # Если задач больше нет, показываем результат
    if current_task >= len(tasks):
        return render_template('result.html', score=score, total=len(tasks))
    else:
        return render_template('index.html', tasks=tasks, score=score, current_task=current_task, message=message)

# Запуск приложения
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
