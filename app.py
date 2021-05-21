import requests
from flask import Flask, render_template, request
from twilio.rest import Client

account_sid = 'AC36ee07378c106ec6330aa5cf8865e736'
auth_token = 'b3556d95c2505dc228aac436e5b8931d'
client = Client(account_sid, auth_token)
app = Flask(__name__, template_folder='./templates',
            static_folder='./static')


@app.route('/')
def registration_form():
    r = requests.get('https://api.covid19india.org/v4/data.json').json()
    # print(r.keys())
    return render_template('form.html', states=r.keys())


@app.route('/register', methods=['GET', 'POST'])
def login_registration_dtls():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source_state']
    source_dt = request.form['source']
    destination_st = request.form['dest_state']
    destination_dt = request.form['destination']
    phoneNumber = request.form['phoneNumber']
    id_proof = request.form['idcard']
    full_name = first_name + "." + last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass = ((cnt / pop) * 100)
    if travel_pass < 30 and request.method == 'POST':
        status = 'CONFIRMED'
        client.messages.create(to="+918897644494",
                               from_="+18173832689",
                               body="Hello " + " " + full_name + " " + "Your Travel From " + " " + source_dt + " to " +
                                    destination_dt + " " + "Has " + " " + status + " On " + " " + ", Apply later")
        return render_template('home', firstname=first_name, lastname=last_name,
                               status="confirmed", email=email_id)
    else:
        status = 'NOT CONFIRMED'
        client.messages.create(to="+918897644494",
                               from_="+18173832689",
                               body="Hello " + " " + full_name + " " + "Your Travel From " + " " +
                                    source_dt + " to " + destination_dt + " " + "Has " + " " + status + " On " + " " +
                                    ", Apply later")
        return render_template('home', firstname=first_name, lastname=last_name,
                               status="confirmed", email=email_id)


if __name__ == "__main__":
    app.run(port=9001, debug=True)
