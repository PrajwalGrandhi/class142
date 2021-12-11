from flask import Flask,jsonify,request
import csv
from demo_filt import output
from content_filt import get_recomm

app=Flask(__name__)

all_movies=[]

with open('final.csv',encoding="utf8") as f:
    csvreader=csv.reader(f)
    data=list(csvreader)
    all_movies=data[1:]

liked_movies=[]
disliked_movies=[]
didnw_movies=[]

@app.route('/get-movies')
def get_movies():
    return jsonify(
        {
            "data":all_movies[0],
            "status":"success"
        }
    )

@app.route('/liked-movie',methods=['POST'])
def liked_movie():
    movie=all_movies[0]
    all_movies=all_movies[1:]
    liked_movies.append(movie)
    return jsonify({
        "status":"success"
    },201)
    
@app.route('/disliked-movie',methods=['POST'])
def disliked_movie():
    movie=all_movies[0]
    all_movies=all_movies[1:]
    disliked_movies.append(movie)
    return jsonify({
        "status":"success"
    },201)
        
@app.route('/didnw-movie',methods=['POST'])
def didnw_movie():
    movie=all_movies[0]
    all_movies=all_movies[1:]
    didnw_movies.append(movie)
    return jsonify({
        "status":"success"
    },201)
    
@app.route('/get-recommended')
def get_recomm():
    all_recommended=[]
    for liked_movie in liked_movies:
        output=get_recomm(liked_movie[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended=list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    movie_data=[]
    for recommended in all_recommended:
        _d={
            "title":recommended[0],
            "poster":recommended[1],
            "release_data":recommended[2]or "N/a",
            "duration":recommended[3],
            "rating":recommended[4],
            "overview":recommended[5]
        }
        movie_data.append(_d)
    return jsonify({
        "data":movie_data,
        "status":"success"
    },200)


@app.route('/get-popular')
def get_pop():
    movie_data=[]
    for movie in output:
        _d={
            "title":movie[0],
            "poster":movie[1],
            "release_data":movie[2]or "N/a",
            "duration":movie[3],
            "rating":movie[4],
            "overview":movie[5]
        }
        movie_data.append(_d)
    return jsonify({
        "data":movie_data,
        "status":"success"
    },200)
    
    
    
    
    
if(__name__=="__main__"):
    app.run()