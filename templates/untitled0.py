# -*- coding: utf-8 -*-
"""
Created on Sat Feb 04 11:46:09 2017

@author: lakshmi1
"""
from flask import Flask, render_template, url_for,request,flash,redirect
from wtforms import validators,TextField,SubmitField,IntegerField,SelectField,RadioField,TextAreaField
from flask_wtf import Form
import sqlite3
import pandas as pd
import pickle
import os

app = Flask(__name__)
app.secret_key = 'developement'

class Book:
    bookCount = 0
    def __init__(self):
        self.category = None
        self.title = None
        self.author = None
        self.date = None
        self.genre = None
        self.synonpsis = None
    def setCategory(self,category):
        self.category = category
    def setTitle(self,title):
        self.title = title
    def setAuthor(self,author):
        self.author = author
    def setGenre(self,genre):
        self.genre = genre
    def setSynopsis(self,synopsis):
        self.synopsis = synopsis
    def setDate(self,date):
        self.date = date
    def getCategory(self):
        return self.category
    def getTitle(self):
        return self.title
    def getGenre(self):
        return self.genre
    def setBookCount(self):
        self.bookCount =self.bookCount-1
    def __str__(self):
        return(self.category + self.title + self.author + self.date + self.genre)

class User:
    userBookList = list(Book)
    def __inti__(self):
        self.userName = None
        self.passWord = None
        self.address = None
        self.phoneNo = 0
        self.age = 0
    def setUserName(self,userName):
        self.userName = userName
    def setPassWord(self,passWord):
        self.passWord = passWord
    def setAddress(self,address):
        self.address = address
    def setPhoneNo(self,phoneNo):
        self.phoneNo = phoneNo
    def setage(self,age):
        self.age = age
    def getUserName(self):
        return(self.userName)
    def getPassWord(self):
        return(self.passWord)
    def addbook(self,Book):
        list.append(Book)

class ManageBook:
    bookList = list(Book)
    
    def register(self,category,title,author,date,genre,synopsis):
        book = Book()
        book.setCategory(category)
        book.setTitle(title)
        book.setAuthor(author)
        book.setDate(date)
        book.setGenre(genre)
        book.setSynopsis(synopsis)
        self.bookList.append(book)
    def DisplayData(self):
        book = Book()
        for book in self.bookList:
            print(book)

class ManageUser:
    user = User()
    userList = {'rb':'111','nsm':'112'}
    def login(self,username,password):
       if( self.userList.has_key(username)):
            if(self.userList.get(username) == password):
                return True 
                
class Login(Form):
    id = TextField("ID",[validators.DataRequired() ])
    name = TextField("Name", [validators.DataRequired() ])
    submit = SubmitField("send")

@app.route('/',method =['GET','POST'])
def userLogin():
    form = Login()
    if(request.method() == 'POST'):
        if(form.validate() == True):
            manageUser = ManageUser()
            username = form.name.data
            password = form.id.data
            if(manageUser.login(username,password) == True):
                flash("valid user")
                return render_template('Login.html',form = form)
        else:
            flash(" invalid")
            return render_template('Login.html')
    elif request.method == 'GET':
         return render_template('doctor.html', form = form)
    
 
       
        
        
       