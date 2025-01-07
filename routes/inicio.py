from flask import Flask, render_template, request, redirect, session, flash, Blueprint, session

index_bp = Blueprint ('index', __name__)

@index_bp.route('/index')
def index():

   return render_template("index.html")
