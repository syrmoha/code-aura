    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    game_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    scores = db.relationship('UserGameScore', backref='game', lazy=True)

class UserGameScore(db.Model):
    __tablename__ = 'user_game_scores'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), primary_key=True)
    score = db.Column(db.Integer)
    played_at = db.Column(db.DateTime, default=datetime.utcnow)

class AITool(db.Model):
    __tablename__ = 'ai_tools'
    
