from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_restful import Resource, Api, reqparse
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'
api = Api(app)

questions = [
    {
        'id':1,
        'question': 'What is the capital of France?',
        'choices': ['Paris', 'London', 'Berlin', 'Rome'],
        'answer': 'Paris'
    },
    {
        'id':2,
        'question': 'What is 2+2?',
        'choices': ['3','4','5','6'],
        'answer': '4'
    },
    {
        'id':3,
        'question': 'What is the largest planet in our solar system?',
        'choices': ['Earth', 'Mars', 'Jupiter', 'Saturn'],
        'answer': 'Jupiter'
    }
]
#curl -X POST -H "Content-Type: application/json" -d "{\"question\" : \"1+1\", \"choices\" : [\"1\", \"2\", \"3\", \"4\"], \"answer\" : \"2\"}" http://127.0.0.1:5000/api/quizzes
#curl -X PUT -H "Content-Type: application/json" -d "{\"question\" : \"1+1\", \"choices\" : [\"1\", \"2\", \"3\", \"4\"], \"answer\" : \"2\"}" http://127.0.0.1:5000/api/quizzes/1
parser = reqparse.RequestParser()
parser.add_argument('question', type = str, required = True, help = 'Question cannot be blank')
parser.add_argument('choices', type = str, action = 'append', required = True, help = 'Choices cannot be blank')
parser.add_argument('answer', type = str, required = True, help = 'Answer cannot be blank')

class QuizList(Resource):
    def get(self):
        return jsonify(questions)
    
    def post(self):
        args = parser.parse_args()
        id = 1
        if (len(questions) > 0):
            id = questions[-1]['id'] + 1
        

        questionObj = {
            'id' : id,
            'question': args['question'],
            'choices': args['choices'],
            'answer' : args['answer']
        }
        questions.append(questionObj)
        return questionObj, 201

class Quiz(Resource):
    
    def get(self, quiz_id):
        global questions
        for questionObj in questions:
            if quiz_id == questionObj['id']:
                return questionObj
        return {'message': 'Quiz not found'}, 404

    def put(self, quiz_id):
        global questions
        args = parser.parse_args()
        for questionObj in questions:
            if quiz_id == questionObj['id']:
                questionObj['question'] = args["question"]
                questionObj['choices'] = args['choices']
                questionObj['answer'] = args['answer']
                return questionObj
        return{'message': 'Quiz not found'}, 404
        
    
    def delete(self, quiz_id):
        global questions
        for questionObj in questions:
            if quiz_id == questionObj['id']:
                questions.remove(questionObj)
        return {'message': ' Quiz deleted', 'code':200}, 200



@app.route('/quiz')
def quiz2():
    session['score'] = 0
    session['question_index'] = 0
    return redirect(url_for('question'))

@app.route('/question')
def question():
    if session['question_index'] >= len(questions):
        return redirect(url_for('result'))
    
    question_data = questions[session['question_index']]
    choices = question_data['choices']
    random.shuffle(choices)
    return render_template('quiz.html', question = question_data['question'], choices = choices)
@app.route('/answer', methods = ['POST'])
def answer():
    selected_choice = request.form['choice']
    question_data = questions[session['question_index']]

    if selected_choice == question_data['answer']:
        session['score'] = session['score'] + 1
    
    session['question_index'] = session['question_index'] + 1
  
    return redirect(url_for('question'))

@app.route('/result')
def result():
    score = session.get('score', 0)
    return render_template('result.html', score = score, total=len(questions))


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/admin')
def admin():
    return render_template('admin.html', questions = questions)

api.add_resource(QuizList, '/api/quizzes')
api.add_resource(Quiz, '/api/quizzes/<int:quiz_id>')

if __name__ == '__main__':
    app.run(debug = True)