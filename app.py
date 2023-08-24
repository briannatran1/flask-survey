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

    session["responses"] = []

    return render_template('survey_start.html',
                           title=survey.title,
                           instructions=survey.instructions)


@app.post('/begin')
def show_first_question():
    """Redirects user to first question when clicking button"""

    return redirect('/questions/0')


@app.get('/questions/<int:num>')
def show_questions(num):
    """Shows form of current question with choices"""
    if num > len(session['responses']):
        flash("You're trying to access an invalid question!!!")
        return redirect(f'/questions/{len(session["responses"])}')

    if len(session['responses']) >= len(survey.questions):
        responses = session['responses']
        session['responses'] = responses

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

    if len(session['responses']) > len(survey.questions) - 1:
        return redirect('/completion')

    return redirect(f'/questions/{len(session["responses"])}')


@app.get('/completion')
def show_completion():
    """Show completion message at end of survey"""
    questions = survey.questions

    return render_template('completion.html',
                           prompts=questions,
                           responses=session['responses'])
