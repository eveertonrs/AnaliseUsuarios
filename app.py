from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Lista para armazenar os eventos
events = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track():
    if request.is_json:
        data = request.get_json()
        print('Dados recebidos:', data)  # Log para debug
        event = {
            "event_type": data['eventType'],
            "url": data.get('url'),
            "time_spent": data.get('timeSpent'),
            "timestamp": data['timestamp'],
            "ip": request.headers.get('X-Forwarded-For', request.remote_addr)  # Use o cabeçalho X-Forwarded-For se estiver disponível, caso contrário, use remote_addr
        }
        events.append(event)
        print('Evento armazenado:', event)  # Log para debug
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Content-Type must be application/json"}), 400


@app.route('/data', methods=['GET'])
def get_data():
    #ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    data = {"events": events}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
