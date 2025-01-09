from flask import Flask, render_template, request
import io
import sys

app = Flask(__name__)

# Список задач
tasks = [
    {
        "title": "Айнымалы құру",
        "explanation": "Айнымалыны x деп құрыңыз және оған 15 мәнін беріңіз. Содан кейін оның мәнін шығарыңыз.",
        "hint": "Мысалы: x = 15 және print(x)",
        "expected_output": "15",  # Ожидаемый результат
    },
    {
        "title": "Жолдармен жұмыс",
        "explanation": "name айнымалысын құрыңыз және оған 'Али' мәнін беріңіз. Оның мәнін шығарыңыз.",
        "hint": "name = 'Али' және print(name)",
        "expected_output": "Али",  # Ожидаемый результат
    },
    {
        "title": "Сандарды қосу",
        "explanation": "a және b айнымалыларын құрыңыз, олардың мәндері 10 және 5. Олардың қосындысын шығарыңыз.",
        "hint": "Мысалы: a = 10, b = 5 және print(a + b)",
        "expected_output": "15",
    },
    {
        "title": "Сандарды азайту",
        "explanation": "20 санынан 8 санын азайтыңыз.",
        "hint": "print(20 - 8)",
        "expected_output": "12",
    },
    {
        "title": "Көбейту",
        "explanation": "7 және 6 сандарын көбейтіңіз.",
        "hint": "print(7 * 6)",
        "expected_output": "42",
    },
    {
        "title": "Сандарды бөлу",
        "explanation": "30 санын 5-ке бөліңіз.",
        "hint": "print(30 / 5)",
        "expected_output": "6.0",
    },
    {
        "title": "Қалдықты табу",
        "explanation": "17 санын 3-ке бөлгенде қалдықты табыңыз.",
        "hint": "print(17 % 3)",
        "expected_output": "2",
    },
    {
        "title": "Санның квадраты",
        "explanation": "5 санының квадратын табыңыз.",
        "hint": "print(5 ** 2)",
        "expected_output": "25",
    },
    {
        "title": "Санның кубы",
        "explanation": "3 санының кубын табыңыз.",
        "hint": "print(3 ** 3)",
        "expected_output": "27",
    },
    {
        "title": "Орташа арифметика",
        "explanation": "10, 20 және 30 сандарының орташа арифметикалық мәнін табыңыз.",
        "hint": "print((10 + 20 + 30) / 3)",
        "expected_output": "20.0",
    },
]

# Главная страница
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks, score=0, current_task=0)

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
        else:
            message = f"❌ Қате. Дұрыс жауап: {tasks[current_task]['expected_output']}."
    except Exception as e:
        sys.stdout = old_stdout
        message = f"❌ Қате: {e}"

    # Переход к следующей задаче
    current_task += 1
    if current_task >= len(tasks):
        return render_template('result.html', score=score, total=len(tasks))
    else:
        return render_template('index.html', tasks=tasks, score=score, current_task=current_task, message=message)

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
