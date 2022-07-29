from collections import defaultdict
from flask import Flask, render_template, request, redirect
from uuid import uuid4
from db import VoteDB

app = Flask(__name__)
db = VoteDB()
# topics = dict({
#     'abc123': {
#         'name': 'Hotel for holiday',
#         'data': {
#             'Hotel A': 0,
#             'Hotel B': 1,
#         }
#     },
# })


@app.route('/')
def index():
    topics = db.get_topic_names()
    print(topics)
    return render_template('index.html', topics=topics)


@app.route('/addTopic', methods=['POST'])
def add_new_topic():
    name = request.form.get('name')
    db.add_topic(topic_name=name)
    return redirect('/')


@app.route('/newTopic')
def new_topic():
    return render_template('newTopic.html')


@app.route('/topic/<topic_id>')
def get_topic_page(topic_id):
    topic_data, topic_name = db.get_topic(topic_id)
    return render_template('topic.html', topic_id=topic_id, topic=topic_data, topic_name=topic_name)


@app.route('/topic/<topic_id>/newChoice', methods=['POST'])
def vote_for_topic(topic_id):
    choice_name = request.form.get('choice_name')
    db.add_choice(choice_name=choice_name, topic_id=topic_id)
    return redirect(f'/topic/{topic_id}')


@app.route('/topic/<topic_id>/vote', methods=['POST'])
def vote_topic(topic_id):
    choice_id = request.form.get('choice')
    db.vote(choice_id=choice_id, topic_id=topic_id)
    return redirect(f'/topic/{topic_id}')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
