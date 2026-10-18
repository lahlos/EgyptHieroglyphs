from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Буква → иероглиф + название (какой звук передаёт)
HIEROGLYPHS = {
    'А': {'glyph': '𓄿', 'name': 'Алеф (орёл)'},
    'Б': {'glyph': '𓃀', 'name': 'Бэт (нога)'},
    'В': {'glyph': '𓅱', 'name': 'Вав (птенец)'},
    'Г': {'glyph': '𓎼', 'name': 'Гим (тростник)'},
    'Д': {'glyph': '𓂧', 'name': 'Далет (рука)'},
    'Е': {'glyph': '𓇋', 'name': 'Йод (тростник)'},
    'Ё': {'glyph': '𓇋', 'name': 'Йод'},
    'Ж': {'glyph': '𓆓', 'name': 'Джабал (змея)'},
    'З': {'glyph': '𓊃', 'name': 'Зайин (засов)'},
    'И': {'glyph': '𓇋', 'name': 'Йод'},
    'Й': {'glyph': '𓇋', 'name': 'Йод'},
    'К': {'glyph': '𓎡', 'name': 'Каф (ладонь)'},
    'Л': {'glyph': '𓃭', 'name': 'Ламед (лев)'},
    'М': {'glyph': '𓅓', 'name': 'Мим (сова)'},
    'Н': {'glyph': '𓈖', 'name': 'Нун (вода)'},
    'О': {'glyph': '𓍯', 'name': 'Айин (глаз)'},
    'П': {'glyph': '𓊪', 'name': 'Пэ (стул)'},
    'Р': {'glyph': '𓂋', 'name': 'Реш (рот)'},
    'С': {'glyph': '𓋴', 'name': 'Самех (опора)'},
    'Т': {'glyph': '𓏏', 'name': 'Тав (хлеб)'},
    'У': {'glyph': '𓅱', 'name': 'Вав'},
    'Ф': {'glyph': '𓆑', 'name': 'Фе (рогатая змея)'},
    'Х': {'glyph': '𓐍', 'name': 'Хет (плеть)'},
    'Ц': {'glyph': '𓈎', 'name': 'Коф (игла)'},
    'Ч': {'glyph': '𓏤', 'name': 'Знак единицы'},
    'Ш': {'glyph': '𓈙', 'name': 'Шин (озеро)'},
    'Щ': {'glyph': '𓈙', 'name': 'Шин'},
    'Ъ': {'glyph': '𓏤', 'name': 'Разделитель'},
    'Ы': {'glyph': '𓇋', 'name': 'Йод'},
    'Ь': {'glyph': '𓏤', 'name': 'Разделитель'},
    'Э': {'glyph': '𓇋', 'name': 'Йод'},
    'Ю': {'glyph': '𓇋𓅱', 'name': 'Йод + Вав'},
    'Я': {'glyph': '𓇋𓄿', 'name': 'Йод + Алеф'},
}

# Вопросы викторины
QUIZ = [
    {
        'question': 'Что такое иероглиф?',
        'options': [
            'Буква современного алфавита',
            'Рисунок-знак, передающий слово, звук или понятие',
            'Цифра для счёта',
            'Музыкальная нота'
        ],
        'correct': 1
    },
    {
        'question': 'Сколько примерно иероглифов использовали древние египтяне?',
        'options': ['33', '200', 'более 700', '10000'],
        'correct': 2
    },
    {
        'question': 'Что чаще всего служило материалом для письма в Древнем Египте?',
        'options': ['Бумага', 'Пергамент', 'Папирус', 'Глина'],
        'correct': 2
    },
    {
        'question': 'Кто расшифровал египетские иероглифы в 1822 году?',
        'options': ['Исаак Ньютон', 'Жан-Франсуа Шампольон', 'Говард Картер', 'Геродот'],
        'correct': 1
    },
    {
        'question': 'Как называется камень, который помог расшифровать иероглифы?',
        'options': ['Розеттский', 'Лунный', 'Солнечный', 'Нил'],
        'correct': 0
    },
    {
        'question': 'Что означает иероглиф 𓂀 (глаз Гора)?',
        'options': ['Смерть', 'Защиту, здоровье, царскую власть', 'Воду', 'Солнце'],
        'correct': 1
    },
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    name = data.get('name', '').upper().strip()

    if not name:
        return jsonify({'error': 'Введи имя'}), 400

    result = []
    for ch in name:
        if ch == ' ':
            continue
        info = HIEROGLYPHS.get(ch)
        if info:
            result.append({
                'letter': ch,
                'glyph': info['glyph'],
                'name': info['name']
            })
        else:
            result.append({
                'letter': ch,
                'glyph': '◻',
                'name': 'неизвестно'
            })

    return jsonify({'result': result})


@app.route('/dictionary')
def dictionary():
    """Отдаёт весь словарь для отображения на странице"""
    items = [
        {'letter': k, 'glyph': v['glyph'], 'name': v['name']}
        for k, v in HIEROGLYPHS.items()
    ]
    return jsonify({'items': items})


@app.route('/quiz')
def quiz():
    """Отдаёт вопросы викторины (без правильных ответов)"""
    safe = [
        {'question': q['question'], 'options': q['options']}
        for q in QUIZ
    ]
    return jsonify({'questions': safe})


@app.route('/quiz/check', methods=['POST'])
def quiz_check():
    """Проверяет ответ на вопрос"""
    data = request.get_json()
    idx = data.get('index')
    answer = data.get('answer')

    if idx is None or answer is None:
        return jsonify({'error': 'bad request'}), 400

    correct = QUIZ[idx]['correct']
    return jsonify({'correct': correct == answer, 'right': correct})


if __name__ == '__main__':
    app.run(debug=True)