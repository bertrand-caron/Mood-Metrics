# Tanda Hackathon (Brisbane, 2017) - Team MoodMetrics

## Team Members

* Christopher Ayling
* Bertrand Caron
* Krishore Subramaniam
* Lucas Wickham

## Stack

* Amazon EC2 Instance (t2.micro, Ubuntu 14.04)
* [Flask](http://flask.pocoo.org) Web App (Python3)
* SQLite3 Database
* [Tanda Webhooks](https://my.tanda.co/api/v2/documentation#webhooks)
* [Kairos API](https://www.kairos.com/docs/)
* Front-end: Bootstrap (v4.0) + Plotly grapphing library

## Installation

* Register an API account with Kairos and add your API App ID and Key to `facial.py`.
* Run the web server with `make serve`

## Usage

* On every clock-in event of one of your Tanda employee, the Kairos API will analyse the employee's mood and return a satisfaction score which can be tracked over time.
* The `/plot` displays the evolution of the satisfaction score of employee with `id=447893`.
