import random
import sqlite3


connection = sqlite3.connect('lightup.db',check_same_thread=False)
db = connection.cursor()

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

class Games:
    '''def __init__(self, no_of_games, score, time, player1, player2, correct_responses, incorrect_responses, player_mode):
        self.no_of_games = no_of_games
        self.score = score
        self.time = time
        self.player1 = player1
        self.player2 = player2
        self.correct_responses = correct_responses
        self.incorrect_responses = incorrect_responses
        self.player_mode = player_mode'''

    def game_description(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def restart(self):
        pass

    def quit(self):
        pass

    def music(self):
        pass

    def calculate_score(self):
        pass

    def update_database(self):
        pass


class Mastermind(Games):
    '''def __init__(self, guess, number, found_count, freeze_count):
        super().__init__
        self.guess = guess
        self.number = number
        self.found_count = found_count
        self.freeze_count = freeze_count'''

    def stopwatch(self):
        pass

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


'''
sec = 0
while(!validate()):
    sec = stopwatch(sec)
'''


'''game = Mastermind
fo = game.found(['1','2','6','0'], '1862')
fr = game.freeze(['1','2','6','0'], '1862')
print("Found : ",fo)
print("Freeze : ",fr)'''


'''game1 = Mastermind()
number = game1.generate_num()
print(number)
while True:
    guess = input("Enter your Guess: ")
    if(game1.validate(number, guess)):
        print("Guessed Correctly!!!")
        break'''



class ChalkboardChallenge(Games):
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



class ColourMatch(Games):
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


class ThinkPic(Games):
    def __init__(self, previous_pic, present_pic):
        super().__init__
        self.previous_pic = previous_pic
        self.present_pic = present_pic

    def timer(self):
        pass


class TapIt(Games):
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

    
#connection.close()