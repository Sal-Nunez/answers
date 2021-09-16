from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.answer import Answer
from flask_app.models.question import Question
from flask_app.models.vote import Vote

@app.route("/new_question")
def new_question():
    uuid = session['id']
    id = {'id': uuid}
    if not 'id' in session:
        return redirect('/')
    elif uuid > 0:
        data = {
            'user': User.select(id)
        }
        return render_template('new_question.html', **data)

@app.route("/create_question", methods=['POST'])
def create_question():
    id = session['id']
    if not 'id' in session:
        return redirect('/')
    elif id > 0:
        Question.new_question(request.form)
        return redirect('/questions')

@app.route('/questions/<int:id>')
def display_question(id):
    user_id = {'id': session['id']}
    data = {
        'user': User.select(user_id),
        'question': Question.select({'id': id}),
        'answers': Answer.answers_with_votes()
    }
    return render_template('question.html', **data)

@app.route('/questions/<int:id>/edit')
def edit_question_show(id):
    question = Question.select(data={'id': id})
    if not 'id' in session:
        return redirect('/')
    elif session['id'] != question.user_id:
        flash('STOP TRYING TO EDIT A QUESTION THAT ISN\'T YOURS')
        return redirect('/')
    else:
        data = {
            'question': Question.select(data={'id': id}),
            'user': User.select(data={'id': session['id']})
        }
        return render_template('new_question.html', **data)

@app.route('/edit_question', methods=['POST'])
def edit_question():
    if not 'id' in session:
        return redirect('/')
    elif session['id'] > 0:
        Question.edit_question(request.form)
        return redirect('/questions')

@app.route('/delete_question', methods=['POST'])
def delete_question():
    id = request.form['id']
    question = Question.select(data={'id': id})
    if not 'id' in session:
        return redirect('/')
    elif session['id'] != question.user_id:
        session.pop('id')
        flash('STOP TRYING TO DELETE A QUESTION THAT ISN\'T YOURS')
    else:
        Question.delete(data={'id':id})
        return redirect('/')