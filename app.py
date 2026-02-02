from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Function to check website safety
def check_website(url):
    score = 0
    result = {}

    # 1. HTTPS check
    if url.startswith("https://"):
        score += 20
        result['https'] = 'Yes'
    else:
        result['https'] = 'No'

    # 2. URL length check
    if len(url) < 75:
        score += 20
        result['length'] = 'Normal'
    else:
        result['length'] = 'Too Long'

    # 3. Suspicious keyword check
    suspicious_words = ['login', 'verify', 'free', 'bonus', 'win', 'secure']
    found_words = [word for word in suspicious_words if word in url.lower()]

    if not found_words:
        score += 20
        result['keywords'] = 'None'
    else:
        result['keywords'] = ', '.join(found_words)

    # 4. Special characters check
    if re.search(r"@|//", url[8:]):
        result['special'] = 'Suspicious'
    else:
        score += 20
        result['special'] = 'Safe'

    # 5. Dummy blacklist check (simulated)
    blacklisted_sites = ['fakebank.com', 'phishingsite.net']
    if any(site in url for site in blacklisted_sites):
        result['blacklist'] = 'Blacklisted'
    else:
        score += 20
        result['blacklist'] = 'Clean'

    # Final decision
    if score >= 80:
        verdict = 'SAFE'
    elif score >= 50:
        verdict = 'WARNING'
    else:
        verdict = 'UNSAFE'

    return score, verdict, result


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        score, verdict, details = check_website(url)
        return render_template('index.html', score=score, verdict=verdict, details=details, url=url)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)