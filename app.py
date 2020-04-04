from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Jedi(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200), nullable=False)
  date_added = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<Jedi %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    jedi_name = request.form['name']
    new_jedi = Jedi(name=jedi_name)

    try:
      db.session.add(new_jedi)
      db.session.commit()
      return redirect('/')
    except:
      return 'There was a problem adding the jedi suggested by you.'

  else:
    jedis = Jedi.query.order_by(Jedi.date_added).all()
    return render_template('index.html', jedis=jedis)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
  jedi = Jedi.query.get_or_404(id)

  if request.method == 'POST':
    jedi.name = request.form['name']

    try:
      db.session.commit()
      return redirect('/')
    except:
      return 'There was a problem updating this jedi.'

  else:
    return render_template('update.html', jedi=jedi)


@app.route('/delete/<int:id>')
def delete(id):
  jedi_to_delete = Jedi.query.get_or_404(id)

  try:
    db.session.delete(jedi_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return 'There was a problem deleting this jedi.'

if __name__ == "__main__":
  app.run(debug=True)
