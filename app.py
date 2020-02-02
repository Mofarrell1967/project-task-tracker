import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'project-task-tracker'
app.config["MONGO_URI"] = 'mongodb+srv://root:Lismara1@myfirstcluster-gpsqs.mongodb.net/project-task-tracker?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def view_tasks():
   return render_template("viewtasks.html", tasks=mongo.db.tasks.find())

@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())

@app.route('/add_task')
def add_task():
    return render_template("addtask.html", projects=mongo.db.projects.find(), staff=mongo.db.staff.find())

@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks')) 

@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_projects =  mongo.db.projects.find()
    return render_template('edittask.html', task=the_task,
                           projects=all_projects)

@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get('task_name'),
        'project_name':request.form.get('project_name'),
        'task_description': request.form.get('task_description'),
        'staff_name': request.form.get('staff_name'),
        'due_date': request.form.get('due_date'),
        'key':request.form.get('key'),
        'external':request.form.get('external'),        
        'billable':request.form.get('billable'),
        'completed':request.form.get('completed')
    })
    return redirect(url_for('get_tasks'))

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))

@app.route('/get_projects')
def get_projects():
    return render_template('projects.html',
                           projects=mongo.db.projects.find())

@app.route('/delete_project/<project_id>')
def delete_project(project_id):
    mongo.db.projects.remove({'_id': ObjectId(project_id)})
    return redirect(url_for('get_projects'))

@app.route('/edit_project/<project_id>')
def edit_project(project_id):
    return render_template('editproject.html',
    project=mongo.db.projects.find_one({'_id': ObjectId(project_id)}))

@app.route('/update_project/<project_id>', methods=['POST'])
def update_project(project_id):
    mongo.db.projects.update(
        {'_id': ObjectId(project_id)},
        {
        'project_name': request.form.get('project_name'),
        'project_description': request.form.get('project_description'),
        'project_owner': request.form.get('project_owner')
        })
    return redirect(url_for('get_projects'))

@app.route('/insert_project', methods=['POST'])
def insert_project():
    projects = mongo.db.projects
    projects.insert_one(request.form.to_dict())
    return redirect(url_for('get_projects'))


@app.route('/add_project')
def add_project():
    return render_template('addproject.html')

@app.route('/get_staff')
def get_staff():
    return render_template("staff.html", staff=mongo.db.staff.find())    

@app.route('/add_staff')
def add_staff():
    return render_template('addstaff.html') 

@app.route('/insert_staff', methods=['POST'])
def insert_staff():
    staff = mongo.db.staff
    staff.insert_one(request.form.to_dict())
    return redirect(url_for('get_staff')) 

@app.route('/update_staff/<staff_id>', methods=["POST"])
def update_staff(staff_id):
    staff = mongo.db.staff
    staff.update( {'_id': ObjectId(staff_id)},
    {
        'staff_name':request.form.get('staff_name'),
        'team':request.form.get('team')
        })
    return redirect(url_for('get_staff')) 

@app.route('/delete_staff/<staff_id>')
def delete_staff(staff_id):
    mongo.db.staff.remove({'_id': ObjectId(staff_id)})
    return redirect(url_for('get_staff'))

@app.route('/edit_staff/<staff_id>')
def edit_staff(staff_id):
    return render_template('editstaff.html',
    staff=mongo.db.staff.find_one({'_id': ObjectId(staff_id)}))

@app.route("/task/<project_id>")
def project_tasker(project_id):
    projecttask=mongo.db.projects.find_one({'_id': ObjectId(project_id)})
    projecttasks=mongo.db.tasks.find({ "project_name" : projecttask["project_name"]})
    return render_template("projecttasks.html", projecttasks=projects)

@app.route("/task/<staff_id>")
def staff_tasker(staff_id):
    stafftask=mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    stafftasks=mongo.db.tasks.find({ "staff_name" : stafftask["staff_name"]})
    return render_template("stafftasks.html", stafftasks=tasks)

 

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)