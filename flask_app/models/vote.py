from flask_app.config.mysqlconnection import connectToMySQL

class Vote:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.answer_id = data['answer_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all_votes(cls):
        query = "SELECT * FROM votes join answers on votes.answer_id = answers.id join questions on answers.question_id = questions.id"
        results = connectToMySQL('answers').query_db(query)
        votes = []
        for vote in results:
            votes.append(cls(vote))
        return votes

    @classmethod
    def vote(cls, data):
        query = "INSERT INTO votes (user_id, answer_id) VALUES (%(user_id)s, %(answer_id)s)"
        return connectToMySQL('answers').query_db(query, data)

    @classmethod
    def vote_validation(cls, data):
        is_valid = True
        query = "SELECT * FROM votes join answers on votes.answer_id = answers.id join questions on answers.question_id = questions.id WHERE votes.user_id = %(user_id)s and questions.id = %(id)s group by questions.id"
        results = connectToMySQL('answers').query_db(query, data)
        if results:
            is_valid = False
        return is_valid
    