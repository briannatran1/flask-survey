from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get('/')
def show_survey_start():
    """Shows survey title, instructions, and start button"""

    return render_template('survey_start.html',
                           title=survey.title,
                           instructions=survey.instructions)


@app.post('/begin')
def show_first_question():
    """Redirects user to first question when clicking button"""

    session["responses"] = []  # do not need to reassign if session is in here

    return redirect('/questions/0')


@app.get('/questions/<int:num>')
def show_questions(num):
    """Shows form of current question with choices"""
    # make var for session['responses]
    responses = session['responses']

    if not responses:
        return redirect('/')

    # accessing questions out of order
    if num > len(session['responses']):
        flash("You're trying to access an invalid question!!!")
        return redirect(f'/questions/{len(responses)}')

    # accessing questions when already completed
    if len(responses) >= len(survey.questions):
        # responses = session['responses']  # need to reassign
        # session['responses'] = responses

        flash("You're trying to access an invalid question!!!")
        return redirect('/completion')

    question = survey.questions[num]

    return render_template('question.html',
                           prompt=question.prompt,
                           choices=question.choices)


@app.post('/answer')
def handle_answer():
    """Handle answer and redirect to next question page"""

    responses = session['responses']
    responses.append(request.form['answer'])
    session['responses'] = responses

    # check if equal
    if len(responses) == len(survey.questions):
        return redirect('/completion')

    return redirect(f'/questions/{len(responses)}')


@app.get('/completion')
def show_completion():
    """Show completion message at end of survey"""
    questions = survey.questions

    return render_template('completion.html',
                           prompts=questions,
                           responses=session['responses'])
