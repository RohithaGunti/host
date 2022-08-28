from flask import Flask, jsonify, request
import sqlite3

#import classesr
import random
import soundfile as sf
import sounddevice as sd

app = Flask(__name__)




connection = sqlite3.connect('lightup.db')
db = connection.cursor()

class Database:
    def __init__(self):
        db.execute("CREATE TABLE users (username VARCHAR PRIMARY KEY, profile_pic VARCHAR);")
        connection.commit()

class User:
    def create_profile(self, name, pro_pic):
        db.execute("INSERT INTO users values(?,?)",(name,pro_pic,))
        db.execute("INSERT INTO chalkboard_challenge values(?,?)",(name,0,))
        db.execute("INSERT INTO mastermind values(?,?)",(name,0,))
        db.execute("INSERT INTO colour_match values(?,?)",(name,0,))
        db.execute("INSERT INTO tap_it values(?,?)",(name,0,))
        db.execute("INSERT INTO think_pic values(?,?)",(name,0,))
        connection.commit()
    def delete_profile(self, name):
        db.execute("DELETE FROM mastermind WHERE username = ?",(name,))
        db.execute("DELETE FROM chalkboard_challenge WHERE username = ?",(name,))
        db.execute("DELETE FROM colour_match WHERE username = ?",(name,))
        db.execute("DELETE FROM tap_it WHERE username = ?",(name,))
        db.execute("DELETE FROM think_pic WHERE username = ?",(name,))
        db.execute("DELETE FROM users WHERE username = ?",(name,))
        connection.commit()
    def switch_profile(self):
        db.execute("SELECT username FROM users LIMIT 1")
        name = db.fetchone()
        return name[0]
    def empty(self):
        db.execute("SELECT COUNT(*) FROM users")
        count = db.fetchall()
        if(count[0][0] == 0):
            return False
        return True
    def mm_score(self):
        db.execute("SELECT no_guess FROM mastermind ORDER BY username ASC;")
        score = db.fetchall()
        return score
    def cc_score(self):
        db.execute("SELECT highscore1 FROM chalkboard_challenge ORDER BY username ASC;")
        score = db.fetchall()
        return score
    def cm_score(self):
        db.execute("SELECT highscore2 FROM colour_match ORDER BY username ASC;")
        score = db.fetchall()
        return score
    def tp_score(self):
        db.execute("SELECT highscore3 FROM think_pic ORDER BY username ASC;")
        score = db.fetchall()
        return score
    def ti_score(self):
        db.execute("SELECT highscore4 FROM tap_it ORDER BY username ASC;")
        score = db.fetchall()
        return score
    def get_pics(self):
        db.execute("SELECT profile_pic FROM users ORDER BY username ASC;")
        pics = db.fetchall()
        return pics
    def get_usernames(self):
        db.execute("SELECT username FROM users ORDER BY username ASC;")
        users = db.fetchall()
        return users
    def details(self,username):
        db.execute("SELECT profile_pic FROM users WHERE username = ?",(username,))
        p = db.fetchone()
        return p[0]


class Mastermind:
    def generate_num(self):
        number = ''.join(random.sample("0123456789", 4))
        return number
    def validate(self, number, guess):
        if(number == guess):
            return True
        return False
    def found(self, guess, number):
        count = 0
        for i in range(4):
            if number[i] in guess and number[i] != guess[i]:
                count += 1
        return count
    def freeze(self, guess, number):
        count = 0
        for i in range(4):
            if guess[i] == number[i]:
                count += 1
        return count


class ChalkboardChallenge:
    def __init__(self):
        self.exp1= []
        self.exp2= []
        self.res1= 0
        self.res2= 0
        self.res=None
        self.inp=None
        self.score=0
        self.op=["+","-","*"]
    def expression1(self):
        while(True):
            self.exp1.append(str(random.randint(0,20)))
            self.exp1.append(self.op[random.randint(0,len(self.op)-1)])
            self.exp1.append(str(random.randint(0,20)))
            self.res1= int(self.exp1[0])
            temp= int(self.exp1[2])
            if(self.exp1[1]=="+"):
                self.res1+=temp
            elif(self.exp1[1]=="-"):
                self.res1-=temp
            elif(self.exp1[1]=="*"):
                self.res1*=temp
            if(self.res1>=0):
                break
            else:
                self.exp1=[]
        return ' '.join(self.exp1)
    def expression2(self):
        while(True):
            self.exp2.append(str(random.randint(0,20)))
            self.exp2.append(self.op[random.randint(0,len(self.op)-1)])
            self.exp2.append(str(random.randint(0,20)))
            self.res2= int(self.exp2[0])
            temp= int(self.exp2[2])
            if(self.exp2[1]=="+"):
                self.res2+=temp
            elif(self.exp2[1]=="-"):
                self.res2-=temp
            elif(self.exp2[1]=="*"):
                self.res2*=temp
            if(self.res2>=0):
                break
            else:
                self.exp2=[]
        return ' '.join(self.exp2)
    def validate(self,exp1,exp2):
        e1=exp1.split(' ')
        e2=exp2.split(' ')
        res1= int(e1[0])
        temp= int(e1[2])
        if(e1[1]=="+"):
            res1+=temp
        elif(e1[1]=="-"):
            res1-=temp
        elif(e1[1]=="*"):
            res1*=temp
        res2= int(e2[0])
        temp= int(e2[2])
        if(e2[1]=="+"):
            res2+=temp
        elif(e2[1]=="-"):
            res2-=temp
        elif(e2[1]=="*"):
            res2*=temp
        if(res1>res2):
            res= "one"
        elif(res1<res2):
            res="two"
        else:
            res="equal"
        return res


class ColourMatch:
    def __init__(self):
        self.word=['black','blue','red','purple','yellow','green']
        self.rgb=['#000000','#0000FF','#FF0000','#A020F0','#FFBA01','#1DE023']
        self.cards=[]
    def generate_colour(self):
        c1=[]
        res=[]
        i1=random.randint(0,5)
        c1.append(self.word[i1])
        c1.append(self.rgb[i1])
        c1.append('correct')
        res.append(c1)
        c2=[]
        i2=random.randint(0,5)
        while(i2==i1):
            i2=random.randint(0,5)
        c2.append(self.word[i2])
        i3=random.randint(0,5)
        while(i2==i3):
            i3=random.randint(0,5)
        c2.append(self.rgb[i3])
        c2.append('wrong')
        res.append(c2)
        i=random.randint(0,1)
        if(i==1):
            res.reverse()
        self.cards=res
        return res
    def cardOne(self,cards):
        return cards[0][0]
    def cardTwo(self,cards):
        return cards[1][0]
    def colourOne(self,cards):
        return cards[0][1]
    def colourTwo(self,cards):
        return cards[1][1]
    def answerOne(self,cards):
        return cards[0][2]        
    def validate(self,cards):
        if(cards=="correct"):
            res="one"
        else:
            res="two"
        return res


class TapIt:
    def __init__(self):
        self.arr=["ascending","descending"]
        self.order=random.choice(self.arr)
        self.randomlist=[]
    def generate_numbers(self):
        count=0
        while(count<5):
            n=random.randint(0,200)
            if n in self.randomlist:
                continue
            self.randomlist.append(n)
            count+=1
        return self.randomlist
    def sorting(self,list,order):
        l = sorted(list)
        if(order=='descending'):
            l.reverse()
        return l


class Scoreboard:
    def mastermind(self,username,score):
        your = db.execute("SELECT no_guess FROM mastermind WHERE username = ?",(username,))
        your = your.fetchone()
        your = int(your[0])
        if(score < your):
            db.execute("UPDATE mastermind SET no_guess = ? WHERE username = ?",(score,username,))
        your = score
        connection.commit()
        best = db.execute("SELECT MIN(no_guess) FROM mastermind WHERE no_guess > 0")
        best = best.fetchone()
        best = int(best[0])
        score = [your,best]
        return score
    def colour(self,username,score):
        your = db.execute("SELECT highscore2 FROM colour_match WHERE username = ?",(username,))
        your = your.fetchone()
        your = int(your[0])
        if(score > your):
            db.execute("UPDATE colour_match SET highscore2 = ? WHERE username = ?",(score,username,))
            your = score
        connection.commit()
        best = db.execute("SELECT MAX(highscore2) FROM colour_match")
        best = best.fetchone()
        best = int(best[0])
        score = [your,best]
        return score
    def chalk(self,username,score):
        your = db.execute("SELECT highscore1 FROM chalkboard_challenge WHERE username = ?",(username,))
        your = your.fetchone()
        your = int(your[0])
        if(score > your):
            db.execute("UPDATE chalkboard_challenge SET highscore1 = ? WHERE username = ?",(score,username,))
            your = score
        connection.commit()
        best = db.execute("SELECT MAX(highscore1) FROM chalkboard_challenge")
        best = best.fetchone()
        best = int(best[0])
        score = [your,best]
        return score
    def think(self,username,score):
        your = db.execute("SELECT highscore3 FROM think_pic WHERE username = ?",(username,))
        your = your.fetchone()
        your = int(your[0])
        if(score > your):
            db.execute("UPDATE think_pic SET highscore3 = ? WHERE username = ?",(score,username,))
            your = score
        connection.commit()
        best = db.execute("SELECT MAX(highscore3) FROM think_pic")
        best = best.fetchone()
        best = int(best[0])
        score = [your,best]
        return score
    def tap(self,username,score):
        your = db.execute("SELECT highscore4 FROM tap_it WHERE username = ?",(username,))
        your = your.fetchone()
        your = int(your[0])
        if(score > your):
            db.execute("UPDATE tap_it SET highscore4 = ? WHERE username = ?",(score,username,))
            your = score
        connection.commit()
        best = db.execute("SELECT MAX(highscore4) FROM tap_it")
        best = best.fetchone()
        best = int(best[0])
        score = [your,best]
        return score


class Leaderboard:
    def mastermind(self):
        db.execute("SELECT username,min(no_guess) AS score FROM mastermind WHERE no_guess>0 GROUP BY username ORDER BY min(no_guess) ASC LIMIT 3;")
        top = db.fetchall()
        return top
    def chalkboard_challenge(self):
        db.execute("SELECT username,max(highscore1) AS score FROM chalkboard_challenge GROUP BY username ORDER BY max(highscore1) DESC LIMIT 3;")
        top = db.fetchall()
        return top
    def colour_match(self):
        db.execute("SELECT username,max(highscore2) AS score FROM colour_match GROUP BY username ORDER BY max(highscore2) DESC LIMIT 3;")
        top = db.fetchall()
        return top
    def think_pic(self):
        db.execute("SELECT username,max(highscore3) AS score FROM think_pic GROUP BY username ORDER BY max(highscore3) DESC LIMIT 3;")
        top = db.fetchall()
        return top
    def tap_it(self):
        db.execute("SELECT username,max(highscore4) AS score FROM tap_it GROUP BY username ORDER BY max(highscore4) DESC LIMIT 3;")
        top = db.fetchall()
        return top




guess = Mastermind().generate_num()
s = 0

@app.route('/',methods=["GET","POST"])
def index():
    Database()
    return "Welcome, hello"

@app.route('/start',methods=["GET","POST"])
def start():
    Database()
    name = ""
    if(User().empty()):
        name = User().switch_profile()
    return jsonify({"Count":User().empty(), "Name":name})

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
        guess = Mastermind().generate_num()
    return jsonify({"Trail":''.join(trail), "Found":Mastermind().found(num,trail), "Freeze":Mastermind().freeze(num,trail)})

@app.route('/createProfile', methods=["GET","POST"])
def createProfile():
    arr = request.get_json()
    username = arr[0]
    propic = arr[1]
    User().create_profile(username, str(propic))
    return "True"

@app.route('/playerDetails', methods=["GET","POST"])
def player_details():
    user = request.get_json()
    d = User().details(user)
    return jsonify({"PP":d})

@app.route('/score/<game>', methods=["GET","POST"])
def scoreboard(game):
    details = request.get_json()
    user = details[0]
    score = details[1]
    if(game == 'mastermind'):
        s = Scoreboard().mastermind(user,score)
    if(game == 'colour'):
        s = Scoreboard().colour(user,score)
    if(game == 'chalk'):
        s = Scoreboard().chalk(user,score)
    if(game == 'think'):
        s = Scoreboard().think(user,score)
    if(game == 'tap'):
        s = Scoreboard().tap(user,score)
    return jsonify({"Your":s[0],"Best":s[1]})

@app.route('/leaderboard', methods=["GET","POST"])
def leaderboard():
    mm = Leaderboard().mastermind()
    cc = Leaderboard().chalkboard_challenge()
    cm = Leaderboard().colour_match()
    tp = Leaderboard().think_pic()
    ti = Leaderboard().tap_it()
    return jsonify({"mm1":str(mm[0][0]),"mm1score": str(mm[0][1]), "mm2": str(mm[1][0]), "mm2score": mm[1][1], "mm3": mm[2][0], "mm3score": mm[2][1], "cc1": cc[0][0], "cc1score": cc[0][1], "cc2": cc[1][0], "cc2score": cc[1][1], "cc3": cc[2][0], "cc3score": cc[2][1], "cm1": cm[0][0], "cm1score": cm[0][1], "cm2": cm[1][0], "cm2score": cm[1][1], "cm3": cm[2][0], "cm3score": cm[2][1], "tp1": tp[0][0], "tp1score": tp[0][1], "tp2": tp[1][0], "tp2score": tp[1][1], "tp3": tp[2][0], "tp3score": tp[2][1], "ti1": ti[0][0], "ti1score": ti[0][1], "ti2": ti[1][0], "ti2score": ti[1][1], "ti3": ti[2][0], "ti3score": ti[2][1]})

@app.route('/viewProfiles', methods=["GET","POST"])
def view_profiles():
    names = User().get_usernames()
    pics = User().get_pics()
    mm = User().mm_score()
    cc = User().cc_score()
    cm = User().cm_score()
    tp = User().tp_score()
    ti = User().ti_score()
    return jsonify({"Names":names,"Pics":pics,"MM":mm,"CC":cc,"CM":cm,"TP":tp,"TI":ti})

@app.route('/deleteProfiles', methods=["GET","POST"])
def delete_profiles():
    username = request.get_json()
    User().delete_profile(username[0])
    return "True"

@app.route('/getExpressions', methods=["GET","POST"])
def get_expressions():
    exp1 = ChalkboardChallenge().expression1()
    exp2 = ChalkboardChallenge().expression2()
    return jsonify({"Expression1":exp1, "Expression2":exp2})

@app.route('/getNumbers', methods=["GET","POST"])
def get_numbers():
    numbers = TapIt().generate_numbers()
    order = TapIt().order
    arranged = TapIt().sorting(numbers,order)
    print(order)
    print(arranged)
    return jsonify({"numbers":numbers,"order":order,"sorted":arranged})

@app.route('/checkAnswers', methods=["GET","POST"])
def check_answers():
    exp1 = ChalkboardChallenge().expression1()
    exp2 = ChalkboardChallenge().expression2()
    answer = request.get_json()
    ans = ChalkboardChallenge().validate(answer[0],answer[1])
    return jsonify({"Expression1":exp1, "Expression2":exp2, "Answer":ans})

@app.route('/checkNumbers', methods=["GET","POST"])
def check_numbers():
    numbers = TapIt().generate_numbers()
    order = TapIt().order
    arranged = TapIt().sorting(numbers,order)
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
    cards = ColourMatch().generate_colour()
    card1 = ColourMatch().cardOne(cards)
    card2 = ColourMatch().cardTwo(cards)
    colour1 = ColourMatch().colourOne(cards)
    colour2 = ColourMatch().colourTwo(cards)
    return jsonify({"cards":ColourMatch().answerOne(cards),"card1":card1, "card2": card2,"colour1": colour1, "colour2": colour2})

@app.route('/checkColours', methods=["GET","POST"])
def check_cards():
    cards = ColourMatch().generate_colour()
    card1 = ColourMatch().cardOne(cards)
    card2 = ColourMatch().cardTwo(cards)
    colour1 = ColourMatch().colourOne(cards)
    colour2 = ColourMatch().colourTwo(cards)
    answer = request.get_json()
    ans = ColourMatch().validate(answer)
    return jsonify({"cards":ColourMatch().answerOne(cards),"card1":card1, "card2": card2,"colour1": colour1, "colour2": colour2, "Answer": ans })

@app.route('/displayScore', methods=["GET","POST"])
def display_score():
    global s
    return jsonify({"Score":s})

app.run()
