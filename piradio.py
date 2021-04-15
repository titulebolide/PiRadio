import subprocess
import flask
import json
import os

app = flask.Flask(__name__)
radios = json.load(open('radios.json', 'r'))['radios']
p = None
selected_radio = 0
stopped = False

@app.route('/')
def frontend():
    global selected_radio, stopped
    html = """<html><head><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"></head><body>"""
    html += """<div class='container'/>"""

    if stopped:
        btn_type='success'
        href='/radio/'+str(selected_radio)
        text='Play'
    else:
        btn_type='danger'
        href='/stop'
        text='Pause'

    html += """
<div class='row'>
    <div class='col-sm-12'>
        <center>
            <a
                class = "btn btn-outline-{}"
                style = "width:50%;min-width:200px;margin-top:10px;"
                href="{}">
                {}
            </a>
        </center>
    </div>
</div>
""".format(btn_type, href, text)

    for radio_id, radio in enumerate(radios):
        additionnal_style = ""
        if radio_id == selected_radio:
            additionnal_style = "font-weight:bold; color:red"
        html += """
<div class='row'>
    <div class='col-sm-12'>
        <center>
            <a
                class = "btn btn-outline-secondary"
                style = "width:50%;min-width:200px;margin-top:10px;{}"
                href="/radio/{}">
                {}
            </a>
        </center>
    </div>
</div>
""".format(additionnal_style, radio_id, radio['name'])

    html += "</div></body></html>"
    return html


@app.route('/radio/<radio_id>')
def select_radio(radio_id):
    global p, selected_radio,stopped
    stopped = False
    with open('default_radio.txt', 'w') as f:
        f.write(radio_id)
    radio_id = int(radio_id)
    selected_radio = radio_id
    if p is not None:
        p.kill()
        p = None
    p = subprocess.Popen(['mplayer', radios[radio_id]['url']])
    return frontend()

@app.route('/stop/')
def stop():
    global p, selected_radio, stopped
    if p is not None:
        p.kill()
        p = None
    stopped = True
    return frontend()


if os.path.isfile('default_radio.txt'):
    with open('default_radio.txt', 'r') as f:
        selected_radio = f.readline()
    try:
        selected_radio = int(selected_radio)
    except ValueError:
        selected_radio = 0
    if selected_radio>=len(radios) and selected_radio<0:
        selected_radio = 0
else:
    selected_radio=0
if not stopped:
    select_radio(str(selected_radio))



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)
