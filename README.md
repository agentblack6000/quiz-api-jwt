# Quiz API

## Project Overview

Implements a Quiz API using the Django REST framework with token authentication

## Functionality

1. New students can be registered
2. A student can be promoted to a teacher from the admin panel
3. Teachers can make quizzes
4. Teachers can add questions and answer choices to quizzes, set options as correct
5. Teachers can view the list of students
6. Students can view questions
7. Admins can do everything

## Usage

New users have to be registered as students using the ```register/``` endpoint. This creates a record in the database and adds the user to the ```student``` group.

The user can then login using the ```login/``` endpoint.

Students can access ```quiz-list/```, ```display-quiz/```, and ```questions/```.

A "student" can promoted to a teacher via the admin panel, which adds the user to the ```teacher``` group.

Admins can access all the views.

Teachers can view the student list, add questions and answer choices, and create quizzes.
