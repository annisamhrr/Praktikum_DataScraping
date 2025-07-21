from flask import Flask, render_template, request
from main import (
    scrape_bolasport,
    scrape_detik_jatim,
    scrape_detik_jateng,
    scrape_detik_jabar,
    scrape_liputan6,
    scrape_cnnindonesia,
    scrape_detail_berita
)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bola-sport')
def bola_sport():
    data = scrape_bolasport()
    return render_template('bola-sport.html', data=data)

@app.route('/detik-jatim')
def detik_jatim():
    data = scrape_detik_jatim()
    return render_template('detik-jatim.html', data=data)

@app.route('/detik-jateng')
def detik_jateng():
    data = scrape_detik_jateng()
    return render_template('detik-jateng.html', data=data)

@app.route('/detik-jabar')
def detik_jabar():
    data = scrape_detik_jabar()
    return render_template('detik-jabar.html', data=data)

@app.route('/berita-gabungan')
def berita_gabungan():
    liputan6_data = scrape_liputan6()
    cnn_data = scrape_cnnindonesia()
    return render_template('berita_gabungan.html', liputan6=liputan6_data, cnn=cnn_data)

@app.route('/berita')
def detail_berita():
    url = request.args.get('url')
    if not url:
        return 'URL berita tidak ditemukan', 400

    detail = scrape_detail_berita(url)
    return render_template('detail_berita.html', berita=detail)

if __name__ == '__main__':
    app.run(debug=True)
