from flask import Flask, render_template, request, redirect, url_for, jsonify
from cs50 import SQL

app = Flask(__name__)  #"(__name__)" a special var. in py that means the script is run by the main program


db = SQL("sqlite:///tasks.db")  # connects to database


@app.route('/', methods=['GET', 'POST'])  #main page/route can get information or send information.
def index():
    if request.method == 'POST':  # if user adds new task.
        task_name = request.form.get('name')  #gets the string of the new task from the form.
        if task_name:  # if there is a task  provided.
            #then we can insert data to the database
            db.execute("INSERT INTO Tasks (Title) VALUES (:name)", name=task_name)
            return redirect(url_for('index'))  #redirect to the main route/page


# gets active and completed tasks from the database added a query for isCompleted field
    tasks = db.execute("SELECT * FROM Tasks WHERE isCompleted = 0 ORDER BY Updated DESC")
    completed_tasks = db.execute("SELECT * FROM Tasks WHERE isCompleted = 1 ORDER BY Updated ASC")
    return render_template('index.html', tasks=tasks, completed_tasks=completed_tasks)

#added new route for marking tasks as completed.
@app.route('/complete/<int:task_id>', methods=['PUT'])  #listens for requests to complete a task.
def complete_task(task_id):
    # changes the task's 'isCompleted' to true.
    db.execute("UPDATE Tasks SET isCompleted = 1 WHERE id = :id", id=task_id)
    return jsonify({"success": True})

#added new route for marking tasks as incomplete.
@app.route('/incomplete/<int:task_id>', methods=['PUT'])  #listens for requests to incomplete a task.
def incomplete_task(task_id):
    # changes the task's 'isCompleted' to false.
    db.execute("UPDATE Tasks SET isCompleted = 0 WHERE id = :id", id=task_id)
    return jsonify({"success": True})

#updating a task.
@app.route('/update/<int:task_id>', methods=['PUT'])  # requests to change a task.
def update_task(task_id):
    # get the newly added data .
    updated_data = request.get_json()
    updated_title = updated_data.get('title')

    # If the new title isn't empty, we update the task.
    if updated_title:
        # change the task's title in the database to the new name.
        db.execute("UPDATE Tasks SET Title = :title WHERE id = :id",
                   title=updated_title, id=task_id)
        return jsonify({"success": True})
    return jsonify({"success": False}), 400  # 400 means there was a problem.

# starts our Flask app in debug mode so we can see errors.
if __name__ == "__main__":
    app.run(debug=True)
