from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.answer import Answer
from flask_app.models.question import Question
from flask_app.models.vote import Vote

@app.route("/vote", methods=["POST"])
def vote():
    id = request.form['question_id']
    if not Vote.vote_validation(request.form):
        flash ("Already Voted", "vote")
        return redirect(f'/questions/{id}')
    Vote.vote(request.form)
    return redirect(f'/questions/{id}')