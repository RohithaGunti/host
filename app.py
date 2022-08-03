from flask import Flask, jsonify, request
import sqlite3

import classesr
import string
import random
import soundfile as sf
import sounddevice as sd

app = Flask(__name__)

guess = classesr.Mastermind().generate_num()
s = 0

@app.route('/start',methods=["GET","POST"])
def start():
    name = ""
    if(classesr.User().empty()):
        name = classesr.User().switch_profile()
    return jsonify({"Count":classesr.User().empty(), "Name":name})

@app.route('/music',methods=["GET","POST"])
def play_music():
    data, fs = sf.read('MyMusic.wav', dtype='float32')
    flag = request.get_json()
    print(flag)
    if(flag == True):
        sd.play(data, fs)
    else:
        sd.stop()
    return ""

@app.route('/getTrail', methods=["GET","POST"])
def trail_num():
    global guess
    num = list(guess)
    print(num)
    trail = request.get_json()
    if ''.join(trail) == guess:
        guess = classesr.Mastermind().generate_num()
    return jsonify({"Trail":''.join(trail), "Found":classesr.Mastermind().found(num,trail), "Freeze":classesr.Mastermind().freeze(num,trail)})

@app.route('/createProfile', methods=["GET","POST"])
def createProfile():
    arr = request.get_json()
    username = arr[0]
    propic = arr[1]
    classesr.User().create_profile(username, str(propic))
    return "True"

@app.route('/playerDetails', methods=["GET","POST"])
def player_details():
    user = request.get_json()
    d = classesr.User().details(user)
    return jsonify({"PP":d})

@app.route('/score/<game>', methods=["GET","POST"])
def scoreboard(game):
    details = request.get_json()
    user = details[0]
    score = details[1]
    if(game == 'mastermind'):
        s = classesr.Scoreboard().mastermind(user,score)
    if(game == 'colour'):
        s = classesr.Scoreboard().colour(user,score)
    if(game == 'chalk'):
        s = classesr.Scoreboard().chalk(user,score)
    if(game == 'think'):
        s = classesr.Scoreboard().think(user,score)
    if(game == 'tap'):
        s = classesr.Scoreboard().tap(user,score)
    return jsonify({"Your":s[0],"Best":s[1]})

@app.route('/leaderboard', methods=["GET","POST"])
def leaderboard():
    mm = classesr.Leaderboard().mastermind()
    cc = classesr.Leaderboard().chalkboard_challenge()
    cm = classesr.Leaderboard().colour_match()
    tp = classesr.Leaderboard().think_pic()
    ti = classesr.Leaderboard().tap_it()
    return jsonify({"mm1":str(mm[0][0]),"mm1score": str(mm[0][1]), "mm2": str(mm[1][0]), "mm2score": mm[1][1], "mm3": mm[2][0], "mm3score": mm[2][1], "cc1": cc[0][0], "cc1score": cc[0][1], "cc2": cc[1][0], "cc2score": cc[1][1], "cc3": cc[2][0], "cc3score": cc[2][1], "cm1": cm[0][0], "cm1score": cm[0][1], "cm2": cm[1][0], "cm2score": cm[1][1], "cm3": cm[2][0], "cm3score": cm[2][1], "tp1": tp[0][0], "tp1score": tp[0][1], "tp2": tp[1][0], "tp2score": tp[1][1], "tp3": tp[2][0], "tp3score": tp[2][1], "ti1": ti[0][0], "ti1score": ti[0][1], "ti2": ti[1][0], "ti2score": ti[1][1], "ti3": ti[2][0], "ti3score": ti[2][1]})

@app.route('/viewProfiles', methods=["GET","POST"])
def view_profiles():
    names = classesr.User().get_usernames()
    pics = classesr.User().get_pics()
    mm = classesr.User().mm_score()
    cc = classesr.User().cc_score()
    cm = classesr.User().cm_score()
    tp = classesr.User().tp_score()
    ti = classesr.User().ti_score()
    return jsonify({"Names":names,"Pics":pics,"MM":mm,"CC":cc,"CM":cm,"TP":tp,"TI":ti})

@app.route('/deleteProfiles', methods=["GET","POST"])
def delete_profiles():
    username = request.get_json()
    classesr.User().delete_profile(username[0])
    return "True"

@app.route('/getExpressions', methods=["GET","POST"])
def get_expressions():
    exp1 = classesr.ChalkboardChallenge().expression1()
    exp2 = classesr.ChalkboardChallenge().expression2()
    return jsonify({"Expression1":exp1, "Expression2":exp2})

@app.route('/getNumbers', methods=["GET","POST"])
def get_numbers():
    numbers = classesr.TapIt().generate_numbers()
    order = classesr.TapIt().order
    arranged = classesr.TapIt().sorting(numbers,order)
    print(order)
    print(arranged)
    return jsonify({"numbers":numbers,"order":order,"sorted":arranged})

@app.route('/checkAnswers', methods=["GET","POST"])
def check_answers():
    exp1 = classesr.ChalkboardChallenge().expression1()
    exp2 = classesr.ChalkboardChallenge().expression2()
    answer = request.get_json()
    ans = classesr.ChalkboardChallenge().validate(answer[0],answer[1])
    return jsonify({"Expression1":exp1, "Expression2":exp2, "Answer":ans})

@app.route('/checkNumbers', methods=["GET","POST"])
def check_numbers():
    numbers = classesr.TapIt().generate_numbers()
    order = classesr.TapIt().order
    arranged = classesr.TapIt().sorting(numbers,order)
    print(order)
    print(arranged)
    return jsonify({"numbers":numbers,"order":order,"sorted":arranged})

@app.route('/getScore', methods=["GET","POST"])
def get_score():
    global s
    s = request.get_json()
    return ""

@app.route('/getColours', methods=["GET","POST"])
def get_cards():
    cards = classesr.ColourMatch().generate_colour()
    card1 = classesr.ColourMatch().cardOne(cards)
    card2 = classesr.ColourMatch().cardTwo(cards)
    colour1 = classesr.ColourMatch().colourOne(cards)
    colour2 = classesr.ColourMatch().colourTwo(cards)
    return jsonify({"cards":classesr.ColourMatch().answerOne(cards),"card1":card1, "card2": card2,"colour1": colour1, "colour2": colour2})

@app.route('/checkColours', methods=["GET","POST"])
def check_cards():
    cards = classesr.ColourMatch().generate_colour()
    card1 = classesr.ColourMatch().cardOne(cards)
    card2 = classesr.ColourMatch().cardTwo(cards)
    colour1 = classesr.ColourMatch().colourOne(cards)
    colour2 = classesr.ColourMatch().colourTwo(cards)
    answer = request.get_json()
    ans = classesr.ColourMatch().validate(answer)
    return jsonify({"cards":classesr.ColourMatch().answerOne(cards),"card1":card1, "card2": card2,"colour1": colour1, "colour2": colour2, "Answer": ans })

@app.route('/displayScore', methods=["GET","POST"])
def display_score():
    global s
    return jsonify({"Score":s})

app.run()