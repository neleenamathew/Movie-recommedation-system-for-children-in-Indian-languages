# -*- coding: utf-8 -*-
"""
Created on Wed May 20 14:38:06 2020

@author: USER
"""

import pandas as pd
import numpy as np
#from distython import HEOM
#Import TfIdfVectorizer from the scikit-learn library
from pandas import DataFrame
from flask import Flask, redirect, url_for, request, render_template
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__, template_folder='C:/Users/USER/Desktop/Web-Scraping-in-R-with-rvest-for-Top-2016-IMDB-Cinemas-master/Movierecommender')
app._static_folder = "C:/Users/USER/Desktop/imdb_scraper/Movierecommender"
@app.route('/begin',methods = ['POST', 'GET'])
def begin():
   if request.method == 'POST':
      user = request.form["art1"]
   if(user=="Recommendation for Children"):
          return render_template('playstore.html')
   else:
          return render_template('login.html')

@app.route('/playstore',methods = ['POST', 'GET'])
def playstore():
    print("inside play store")
    if request.method == 'POST':
        category = request.form['category']
        return redirect(url_for('children',name = category))

@app.route('/children/<name>')
def children(name):
    data=pd.read_csv('C:/Users/USER/Documents/qualitativedata.csv',encoding="ISO-8859-1")
    numerized=data
    num1 = {"Sex and nudity": {"None": 0, "Mild": 0.4,"Moderate": 0.6,"Severe": 1,"Severity":0.2}}
    numerized.replace(num1, inplace=True)
    num2 = {"Violence and Gore": {"None": 0, "Mild": 0.4,"Moderate": 0.6,"Severe": 1,"Severity":0.2}}
    numerized.replace(num2, inplace=True)
    num3 = {"Profanity": {"None": 0, "Mild": 0.4,"Moderate": 0.6,"Severe": 1,"Severity":0.2}}
    numerized.replace(num3, inplace=True)
    num4 = {"Alcohol": {"None": 0, "Mild": 0.4,"Moderate": 0.6,"Severe": 1,"Severity":0.2}}
    numerized.replace(num4, inplace=True)
    num5 = {"Frightening": {"None": 0, "Mild": 0.4,"Moderate": 0.6,"Severe": 1,"Severity":0.2}}
    numerized.replace(num5, inplace=True)
    #num6={"Language":{"Hindi":1,"Tamil":2,"Telugu":3,"Bengali":4,"Malayalam":5,"Punjabi":6}}
    #numerized.replace(num6, inplace=True)

    heomdat=pd.concat([data['Language'],data['Title'],numerized['Sex and nudity'],numerized['Violence and Gore'],numerized['Profanity'],numerized['Alcohol'],numerized['Frightening']],axis=1)

    damn = DataFrame(data,columns=['Language','Title','Sex and nudity','Violence and Gore','Profanity','Alcohol','Frightening'])
    count_column = damn.sum(axis=1)
    damn['count_column'] = count_column

    df = DataFrame(damn,columns=['Language','Title','count_column'])

    df = df.sort_values('count_column', ascending=False)            
    Age = int(name)
    if Age <= 3:
           cond=df[df["count_column"]<=0 ].head(10)
                     
    if Age >= 4 | Age <=5:
           cond=df[df["count_column"]<=1 ].head(10)
         
    if Age >= 6 | Age<=7:
           cond=df[df["count_column"]<=2 ].head(10)  

    if Age >= 8 | Age<=9:
           cond=df[df["count_column"]<=2.5 ].head(10)
           
    if Age >= 10 | Age<=11:
           cond=df[df["count_column"]<=3 ].head(10)

    if Age >= 12 | Age<=13:
           cond=df[df["count_column"]<=4 ].head(10)

    if Age >= 14 | Age<=15:
           cond=df[df["count_column"]<=4.5 ].head(10)
        
    if Age >= 16 | Age<=17:
           cond=df[df["count_column"]<=5 ].head(10)

    print(cond)         
    dataframe=pd.DataFrame(cond, columns=['Language','Title'])
    print(dataframe.head(10))
    return render_template('output_recommend.html', tables=[dataframe.to_html(classes='data')],titles=dataframe.columns.values)

    
#dataframe=pd.DataFrame(cond, columns=['Language','Title','count_column'])
#print(dataframe.head(10))
#return render_template('output_recommend.html',tables=[dataframe.to_html(classes='data')],titles=dataframe.columns.values)


@app.route('/success1/<name>')
def success1(name):
     print("inside success1")
     train=pd.read_csv('C:/Users/USER/Desktop/moviedata.csv',encoding="ISO-8859-1")
     tfidf = TfidfVectorizer(stop_words='english')
     tfidf_matrix = tfidf.fit_transform(train['metadata'])
     tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), index=train.index.tolist())
     cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
# calculate the similartity of this movie with the others in the list
     train = train.reset_index()
     titles = train['title']
     indices = pd.Series(train.index, index=train['title'])
     def recommend(title):
         idx = indices[title]
         sim_scores = list(enumerate(cosine_similarities[idx]))
         sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
         sim_scores = sim_scores[1:31]
         movie_indices = [i[0] for i in sim_scores]
         return titles.iloc[movie_indices]
     names1 = recommend(name).head(6)
     names2 = names1.to_frame(name='title')
     return render_template('output_recommend.html', tables=[names2.to_html(classes='data')], titles=names2.columns.values)

@app.route('/login',methods = ['POST', 'GET'])
def login():
   print("inside login")
   if request.method == 'POST':
       user = request.form['movie']
       return redirect(url_for('success1',name = user))
   
    
    
   
    
if __name__ == '__main__':
   app.run()
   
# <div style="background-image:url('https://i.pinimg.com/564x/1b/65/4d/1b654dac004716a7f8b908a7886c9e4a.jpg');" class="bg">
#  <div style="background-image:url('https://i.pinimg.com/564x/6a/7c/a8/6a7ca8ac5da0e06aae9c9b988ee20878.jpg');" class="bg">
#<p><center><input style="font-size:25px; font-family:Arial" type="submit" name = "art1" value="Recommendation for Adults"></input></center></p>
 #</div>
  #<div class="column">   
  #<p><center><input style="font-size:25px; font-family:Arial" type="submit" name = "art1" value="Recommendation for Children"></input></center></p>
 #</div>
#</div>  
 #</form> 