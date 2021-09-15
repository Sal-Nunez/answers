from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.answer import Answer
from flask_app.models.question import Question

@app.route('/answer_question', methods=['POST'])
def new_answer():
    Answer.new_answer(request.form)
    id = request.form['question_id']
    return redirect(f'/questions/{id}')

@app.route('/delete_answer', methods=['POST'])
def delete_answer():
    question = Question.select(data={'question_id':request.form['question_id']})
    if (session['id']) == (question.user_id):
        print ("**************************",session['id'],"***", request.form['user_id'])
        flash("DO NOT TRY TO DELETE ANSWER THAT ISN'T YOURS")
        return redirect(f'/questions/{question.id}')
    else:
        Answer.delete_answer(request.form)
        return redirect(f'/questions/{question.id}')

@app.route('/best_answer', methods=['POST'])
def best_answer_route():
    question_id = request.form['question_id']
    Question.best_answer(request.form)
    return redirect (f'/questions/{question_id}')