from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import question


class Answer:
    def __init__(self, data):
        self.id = data['id']
        self.answer = data['answer']
        self.user_id = data['user_id']
        self.question_id = data['question_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.username = data['username']
        self.votes = data['votes']

    @classmethod
    def select(cls, data=None):
        if data:
            query = "SELECT * FROM answers left join votes on answers.id = votes.user_id join users on users.id = answers.user_id WHERE answers.id = %(id)s"
            results = connectToMySQL('answers').query_db(query, data)
            answer = cls(results[0])
            answer.votes = 0
            for vote in results:
                answer.votes += 1
            return answer
        else:
            query = "SELECT * FROM answers join users on users.id = answers.user_id"
            results = connectToMySQL('answers').query_db(query)
            answers = []
            for user in results:
                answers.append(cls(user))
            return answers

    @classmethod
    def answered_questions(cls):
        query = "SELECT *, SUM(CASE WHEN votes.answer_id = answers.id then 1 else 0 end) as votes FROM answers join questions on answers.question_id = questions.id join users on questions.user_id = users.id join votes on votes.answer_id = answers.id group by questions.id"
        results = connectToMySQL('answers').query_db(query)
        if results:
            answer = cls(results[0])
            answer.questions = []
            for question1 in results:
                if question1['question']:
                    data = {
                        'id': question1['questions.id'],
                        'question': question1['question'],
                        'description': question1['description'],
                        'created_at': question1['questions.created_at'],
                        'updated_at': question1['questions.updated_at'],
                        'user_id': question1['questions.user_id'],
                        'username': question1['username'],
                        'best_answer_id': question1['best_answer_id']
                    }
                    answer.questions.append(question.Question(data))
                else:
                    break
            return answer
        else:
            return None

    
    @classmethod
    def one_question_answers(cls, data):
        query = "SELECT *, SUM(CASE WHEN votes.answer_id = answers.id then 1 else 0 end) as votes FROM answers left join votes on answers.id = votes.answer_id WHERE question_id = %(question_id)s"
        results = connectToMySQL('answers').query_db(query, data)
        answers = []
        for answer in results:
            answers.append(cls(answer))
        return answers
    
    @classmethod
    def answers_with_votes(cls):
        query = "SELECT *, SUM(CASE WHEN votes.answer_id = answers.id then 1 else 0 end) as votes FROM answers left join votes on answers.id = votes.answer_id join users on users.id = answers.user_id group by answers.id"
        results = connectToMySQL('answers').query_db(query)
        answers = []
        for answer in results:
            answers.append(cls(answer))
        return answers

    @classmethod
    def new_answer(cls, data):
        query = "INSERT INTO answers (answer, user_id, question_id) VALUES (%(answer)s, %(user_id)s, %(question_id)s)"
        return connectToMySQL('answers').query_db(query, data)

    @classmethod
    def delete_answer(cls, data):
        query = "DELETE FROM answers where answers.id = %(id)s"
        return connectToMySQL('answers').query_db(query, data)