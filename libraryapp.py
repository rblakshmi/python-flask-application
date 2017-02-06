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
    userbookList = []
    def __init__(self):
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
        User.userBookList.append(Book)

class ManageBook:
    bookList = []
    def register(self,category,title,author,date,genre,synopsis):
        book = Book()
        book.setCategory(category)
        book.setTitle(title)
        book.setAuthor(author)
        book.setDate(date)
        book.setGenre(genre)
        book.setSynopsis(synopsis)
        self.bookList.append(book)
    def DisplayData(self,category,genre):
        book = Book()
        if (category == None and genre == None):
            return ManageBook.bookList
        elif(genre == None):
            book = Book()
            bookCategoryList =[]
            for book  in ManageBook.bookList:
                if(book.getCategory() == category):
                    bookCategoryList.append(book)
            return bookCategoryList
        elif(category == None):
            book = Book()
            bookGenreList =[]
            for book in ManageBook.bookList:
                if(book.getGenre == genre):
                    bookGenreList.append(book)
            return bookGenreList
        else:
            book = Book()
            bookBothList = []
            for book in ManageBook.bookList:
                if(book.getCategory == category and book.getGenre == genre):
                    bookBothList.append(book)
            return bookBothList
                


class ManageUser:
    userList = [];
    
    def testUser(self):
        user= User()
        user.setUserName('rb')
        user.setPassWord('111')
        ManageUser.userList.append(user)
    def login(self,username,password):
        user =User()
        for user in ManageUser.userList:
           if(user.getUserName == username and user.getPassWord == password):
               return True
    
        
        
       
                
class Login(Form):
    id = TextField("ID",[validators.DataRequired() ])
    name = TextField("Name", [validators.DataRequired() ])
    submit = SubmitField("send")
    
class Order(Form):
    bookName = TextField("ID",[validators.DataRequired() ])
    userName = TextField(" name" )
    userAddress= TextField("ADDRESS")
    userNo = IntegerField("Phone number")
    submit = SubmitField("send")

class BookDetailForm(Form):
    bookname = TextField("Book name")
    bookCategory = TextField("Title")
    bookAuthor = TextField("Author")
    bookDate = TextField(" Date")
    bookGenre = TextField(" Genre")
    bookSynopsis = TextField(" Synopsis")
    submit = SubmitField("register")
    
class BookDisplay(Form):
    bookCategory = TextField("enter category")
    bookGenre = TextField("enter the genre")
    submit = SubmitField("Submit")
    
class BookListDisplay(Form):
    detail = TextAreaField()
    

@app.route('/',methods =['GET','POST'])
def userLogin():
    form = Login()
    if(request.method == 'POST'):
        if(form.validate() == True):
            manageUser = ManageUser()
            manageUser.testUser()
            username = form.name.data
            password = form.id.data
            if(manageUser.login(username,password) == True):
                flash('valid user')
                if(username == "admin"):
                    return render_template('login.html',form = form)
                else:
                    
                    return render_template('booklist.html',form=BookDetailForm())
            else:
                flash(" invalid")
                return render_template('login.html',form = form)
    elif request.method == 'GET':
         return render_template('login.html',form = form)
         
@app.route('/bookdetails' , methods = ['GET','POST'])
def bookDetails():
    manageBook = ManageBook()
    form = BookDetailForm()
    if(request.method == 'POST'):
        category = form.bookCategory.data
        name = form.bookname.data
        date = form.bookDate.data
        genre = form.bookGenre.data
        synopsis = form.bookSynopsis.data
        manageBook.register(category,name,date,genre,synopsis)
        flash('registerd')
        return render_template('bookdetails.html',form = form)
    elif request.method == 'GET':
        return render_template('bookdisplay.html',form = form)
 
@app.route('/bookdisplay' ,methods = ['GET','POST'])
def bookDisplay():
    form = BookDisplay()
    form2 =BookListDisplay()
    if(request.method == 'GET'):
        category = form.bookCategory.data
        genre = form.bookGenre.data
        managebook = ManageBook()
        text = managebook.DisplayData(category,genre)
        render_template('bookdetaildisplay.html',form = form2,text =text)
 
@app.route('/bookdisplay/booklistdisplay', methods =['GET','POST'])
def booklistdisplay():
    if(request.method == 'GET'):
       render_template('bookdisplaydetail.html', form = BookListDisplay())     

if __name__  == '__main__':
    app.run(debug=True)
       
        
        
       