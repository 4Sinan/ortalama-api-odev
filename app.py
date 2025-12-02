from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ortalama", methods=['GET'])
def ortalama_hesapla():
    # Bu yorum satırı, 3 Aralik ödevi icin eklendi. (Kod degisikligi)
    sayi1_str = request.args.get('sayi1')
    sayi2_str = request.args.get('sayi2')

    if sayi1_str is None or sayi2_str is None:
        return jsonify({"hata": "Lütfen 'sayi1' ve 'sayi2' parametrelerini girin."}), 400

    try:
        sayi1 = float(sayi1_str)
        sayi2 = float(sayi2_str)
    except ValueError:
        return jsonify({"hata": "Parametreler sayısal bir değer olmalıdır."}), 400

    sonuc = (sayi1 + sayi2) / 2

    return jsonify({"ortalama_sonucu": sonuc}), 200

if __name__ == '__main__':
    app.run(debug=True)
