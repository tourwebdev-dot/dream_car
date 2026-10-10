# 🏎️ MX-5 Dream Tracker (Backend Data Pipeline)

Ένα εργαλείο αυτοματισμού γραμμένο σε Python, το οποίο λειτουργεί ως το Backend τμήμα μιας Full-Stack εφαρμογής. Αναλαμβάνει να σαρώσει τη δυναμική αγορά του car.gr (παρακάμπτοντας anti-bot συστήματα) και να εντοπίσει ευκαιρίες για Mazda MX-5 κάτω των 5.000€.

Τα δεδομένα εξάγονται αυτόματα σε μορφή JSON, δημιουργώντας μια "γέφυρα" (API-like behavior) για να καταναλωθούν από ένα React Frontend.

## 🛠️ Τεχνολογίες & Εργαλεία
* **Python 3**
* **Playwright:** Χρήση εικονικού browser για rendering της JavaScript, διαχείριση Cookies και αντιμετώπιση του Cloudflare.
* **Regular Expressions (RegEx):** Εξαγωγή καθαρών αριθμητικών δεδομένων αγνοώντας τις δυναμικές αλλαγές στο Tailwind CSS (DOM HTML).
* **JSON:** Δομημένη εξαγωγή δεδομένων για άμεση ενσωμάτωση με JavaScript/React.

## 💡 Προκλήσεις που αντιμετωπίστηκαν
1. **Δυναμικές Κλάσεις CSS:** Αποφυγή χρήσης ασταθών CSS Selectors. Η αναζήτηση γίνεται δομικά στο DOM (αναζητώντας HTML Tags με βάση το σύμβολο €).
2. **Cloudflare / Bot Protection:** Υλοποίηση **Smart Wait**. Το πρόγραμμα περιμένει έξυπνα να φορτώσει το περιεχόμενο, δίνοντας περιθώριο στον χρήστη να λύσει το Captcha αν το Cloudflare μπλοκάρει τον αυτοματισμό.
3. **Data Cleaning:** Αυτόματος καθαρισμός συμβόλων, κενών και εξαγωγή απόλυτων URLs από relative links.

## 🚀 Πώς να το τρέξετε
1. Εγκαταστήστε τις απαιτούμενες βιβλιοθήκες:
   ```bash
   pip install -r requirements.txt
   playwright install chromium