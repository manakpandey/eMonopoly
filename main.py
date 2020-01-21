from wtforms import Form, BooleanField, StringField, IntegerField, validators, SelectField
from flask import Flask, render_template, redirect, flash, request

app  = Flask(__name__)
app.config['SECRET_KEY'] = 'a7hg0kf4jh6b4qb8fj5d'

startBal = 1500

data = [[startBal,startBal,startBal,startBal,startBal,startBal],
		[0,0,0,0,0,0],
		[0,0,0,0,0,0]]
flag=0
log=[[],[],[]]
player=[]


class PayForm(Form):
    username = SelectField('Username', choices=[player])
    amount = IntegerField('Amount', [
        validators.DataRequired()
    ])

class StartForm(Form):
    user1 = StringField('User1', [validators.DataRequired()])
    user2 = StringField('User2', [validators.DataRequired()])
    user3 = StringField('User3')
    user4 = StringField('User4')
    user5 = StringField('User5')
    user6 = StringField('User6')    


@app.route('/player/<id>', methods=['GET', 'POST'])
def user(id):
	user = int(id)-1
	return render_template('home.html', cash=data[0][user], #mortage=data[1][user], 
															#urlm='/player/'+str(id)+'/mortage', 
															urlp='/player/'+str(id)+'/pay', 
															un=player[user],
															br=data[2][user])
@app.route('/player/<id>/pay', methods=['GET', 'POST'])
def pay(id):
	user = int(id)-1
	form = PayForm(request.form)
	if request.method == 'POST':

		if form.amount.data <= data[0][user] and form.username.data in player:
			data[0][user] = data[0][user] - form.amount.data
			data[0][player.index(form.username.data)] = data[0][player.index(form.username.data)] + form.amount.data
			flash(player[user]+' paid '+str(form.amount.data)+' to '+str(form.username.data))
			log[0].insert(0,player[user])
			log[1].insert(0,form.username.data)
			log[2].insert(0,form.amount.data)			
			return redirect('player/'+str(id))
		elif form.username.data == 'Bank' and form.amount.data <= data[0][user]:
			data[0][user] = data[0][user] - form.amount.data
			flash(player[user]+' paid '+str(form.amount.data)+' to '+str(form.username.data))
			log[0].insert(0,player[user])
			log[1].insert(0,form.username.data)
			log[2].insert(0,form.amount.data)									

			return redirect('player/'+str(id))		
		else: 
			return render_template('error.html',url='/player/'+str(id), 
												urlp='/player/'+str(id)+'/pay', 
												un=player[user],
												br=data[2][user])				
	return render_template('pay.html', form=form, 
									url='/player/'+str(id), 
									un=player[user],
									br=data[2][user],
									player=player)

'''@app.route('/bank', methods=['GET','POST'])
def banker():
	return render_template('bank_credit.html', player=player,cash=data[0],br=data[2])'''

@app.route('/board', methods=['GET','POST'])
def board():
	return render_template('board.html', player=player,cash=data[0],br=data[2])	

@app.route('/bank', methods=['GET','POST'])
def credit():
	form=PayForm(request.form)
	if request.method == 'POST':		
			data[0][player.index(form.username.data)] = data[0][player.index(form.username.data)] + form.amount.data
			flash(str(form.amount.data)+' credited to '+str(form.username.data))
			log[0].insert(0,'Bank')
			log[1].insert(0,form.username.data)
			log[2].insert(0,form.amount.data)			
			return redirect('/bank')

	return render_template('bank_credit.html', player=player, br=data[2])

@app.route('/bank/bankrupt', methods=['GET','POST'])
def bankrupt():
	form=PayForm(request.form)
	if request.method == 'POST':
		data[2][player.index(form.username.data)] = 1
		return redirect('/banker')
	return render_template('bankrupt.html', player=player, br=data[2])

@app.route('/log', methods=['GET','POST'])
def logs():	
	return render_template('log.html', log=log, len=len(log[0]))


@app.route('/start', methods=['GET','POST'])
def start():
	form=StartForm(request.form)
	if request.method == 'POST':
		global flag
		flag=1
		player.append(form.user1.data)
		player.append(form.user2.data)
		player.append(form.user3.data)
		player.append(form.user4.data)
		player.append(form.user5.data)
		player.append(form.user6.data)
		return redirect('/board')
	return render_template('start.html')



@app.route('/', methods=['GET','POST'])
def homepage():
	print (flag)
	return render_template('homepage.html', player=player,start=flag)












if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0',port=5000, threaded=True)   

