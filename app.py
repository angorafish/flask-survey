from flask import Flask, request, render_template, redirect, session, flash
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

responses = []

@app.route('/')
def survey_start():
    """Display the survey start page with the title and instructions."""
    return render_template("start.html", survey=survey)

@app.route('/initialize', methods=['POST'])
def initialize_survey():
    """Initialize survey responses and redirect to the first question."""
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:qid>')
def show_question(qid):
    """Display a survey question based on its sequential ID."""
    responses = session.get('responses', [])
    if len(responses) == len(survey.questions):
        return redirect('/thank-you')
    
    if qid >= len(survey.questions) or len(responses) != qid:
        flash("You're trying to access an invalid question!")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template('question.html', question=question, qid=qid)

@app.route('/answer', methods=["POST"])
def handle_answer():
    """Process the survey answer and either redirect to next question or completion page based on question ID."""
    answer = request.form['answer']
    responses = session.get('responses', [])
    responses.append(answer)
    session['responses'] = responses

    qid = int(request.form['qid'])
    if qid + 1 < len(survey.questions):
        return redirect(f"/questions/{qid + 1}")
    else:
        return redirect("/thank-you")
    
@app.route('/thank-you')
def thank_you():
    """Display thank-you page upon survey completion."""
    responses = session.get('responses', [])
    if len(responses) != len(survey.questions):
        return redirect(f'/questions/{len(responses)}')
    return render_template('thank_you.html')