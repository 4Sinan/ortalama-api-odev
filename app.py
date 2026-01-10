from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'odev_gizli_anahtar_123' # JWT imzalamak için gerekli

# --- TOKEN KONTROL MEKANİZMASI ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"hata": "Token eksik! Lütfen 'Authorization' header'ına ekleyin."}), 401
        
        try:
            # "Bearer <token>" formatından token'ı ayıklar
            token_clean = token.split(" ")[1] if " " in token else token
            jwt.decode(token_clean, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({"hata": "Geçersiz veya süresi dolmuş token!"}), 401
        
        return f(*args, **kwargs)
    return decorated

# 1. AÇIK ENDPOINT (10 Puan)
# Senin eski ortalama kodun, herkes erişebilir.
@app.route("/ortalama", methods=['GET'])
def ortalama_hesapla():
    sayi1_str = request.args.get('sayi1')
    sayi2_str = request.args.get('sayi2')

    if sayi1_str is None or sayi2_str is None:
        return jsonify({"hata": "Lütfen 'sayi1' ve 'sayi2' parametrelerini girin."}), 400

    try:
        sayi1 = float(sayi1_str)
        sayi2 = float(sayi2_str)
        sonuc = (sayi1 + sayi2) / 2
        return jsonify({"ortalama_sonucu": sonuc}), 200
    except ValueError:
        return jsonify({"hata": "Parametreler sayısal bir değer olmalıdır."}), 400

# 2. LOGIN - TOKEN ALMA BÖLÜMÜ
# Bu bölüm kilitli kapıyı açmak için anahtar (token) üretir.
@app.route("/login", methods=['POST'])
def login():
    auth = request.json
    if auth and auth.get('username') == 'admin' and auth.get('password') == '123':
        token = jwt.encode({
            'user': 'admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    
    return jsonify({"hata": "Hatalı kullanıcı adı veya şifre!"}), 401

# 3. KİLİTLİ ENDPOINT (20 Puan)
# Sadece geçerli token ile girilebilir.
@app.route("/ozel-veri", methods=['GET'])
@token_required
def ozel_veri():
    # Basit bir veritabanı verisi simülasyonu (20 Puan)
    veritabani_verisi = {"id": 1, "mesaj": "Bu veri veritabanından şifreli tünelle geldi."}
    return jsonify(veritabani_verisi), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
