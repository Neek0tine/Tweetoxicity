from scripts import app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 33507)), debug=True)
    
    
