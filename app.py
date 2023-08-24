from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get('/')
def show_survey_start():
    """Shows survey title, instructions, and start button"""

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
    question = survey.questions[num]

    return render_template('question.html',
                           prompt=question.prompt,
                           choices=question.choices)


@app.post('/answer')
def handle_answer():
    """Handle answer and redirect to next question page"""
    responses.append(request.form['answer'])

    if len(responses) > len(survey.questions) - 1:
        return redirect('/completion')

    return redirect(f'/questions/{len(responses)}')


@app.get('/completion')
def show_completion():
    """Show completion message at end of survey"""
    questions = survey.questions

    return render_template('completion.html',
                           prompts=questions,
                           responses=responses)
