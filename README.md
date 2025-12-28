# 🌐 Universal Translator — Professional Django Web Suite

![Django](https://img.shields.io/badge/django-%23092e20.svg?style=for-the-badge&logo=django&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

**Universal Translator** is an enterprise-grade translation platform developed with **Django**. It offers real-time text and voice translation for over 100 languages. Designed with high-security standards and performance optimization, this app features a persistent history system, profile management, and a seamless asynchronous UI.

---

## ✨ Key Features

* **⚡ Real-time Translation:** Asynchronous Fetch API architecture for instant results without refreshing.
* **⌨️ Intelligent Debounce:** Optimized with a 700ms debounce logic to reduce unnecessary API hits and improve performance.
* **🎙️ Voice Input:** Integrated **Web Speech API** allowing users to dictate text directly for translation.
* **📂 Translation History:** Persistent database storage for logged-in users, accessible via a slide-out sidebar.
* **👤 User Profiles:** Custom user profiles with image upload (Pillow) and secure credential management.
* **🛡️ Secure Logic:** Robust CSRF handling for all AJAX requests and protected views.

---

## 🛠️ Technical Fixes & Improvements

This project identifies and resolves several critical real-world development challenges:

1.  **CSRF Token Validation (Fixed):** Resolved the `X-CSRFToken` mismatch error by creating a custom JavaScript utility that securely extracts tokens from browser cookies for AJAX headers.
2.  **API Rate Limiting:** Implemented a debounce mechanism to ensure the system only sends a request after the user finishes typing.
3.  **UI Data Integrity:** Integrated a "Login Required" alert for history access, ensuring a logical flow for guest vs. authenticated users.
4.  **Stability:** Backend `try-except` blocks ensure that API errors or network timeouts don't crash the server.

---

## 💻 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python 3.x, **Django 5.x** |
| **Translation** | `deep-translator` (Google Translate Engine) |
| **Frontend** | ES6 JavaScript, Bootstrap 5, FontAwesome 6 |
| **Database** | SQLite (Dev) / PostgreSQL (Ready) |
| **Alerts** | SweetAlert2 (Professional Popups) |

---

## 🚀 Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/universal-translator.git](https://github.com/your-username/universal-translator.git)
    cd universal-translator
    ```

2.  **Environment Setup:**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    pip install django deep-translator Pillow
    ```

3.  **Migration & Superuser:**
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

4.  **Run Application:**
    ```bash
    python manage.py runserver
    ```

---

## 📁 API Documentation

### **Translate Endpoint**
* **URL:** `/translate-api/`
* **Method:** `POST`
* **Body:** `{"text": "Hello world", "target": "bn"}`
* **Response:** `{"translated_text": "ওহে বিশ্ব"}`

---

## 🛡️ License

This project is licensed under the **GNU General Public License v3.0**. 

### ⚖️ Permissions under GPLv3:
* **Commercial Use:** You can use this software for commercial purposes.
* **Modification:** You can modify the code, but you must keep the source code open.
* **Distribution:** You can distribute the original or modified code.
* **Credit:** You must give credit to the original author (Md Jahid Hasan).

See the [LICENSE](LICENSE) file for more details.

---
## 👤 Author

- Developer: Md Jahid Hasan  
- Email: jahidhasanpiyesh@gmail.com  
- LinkedIn: [https://www.linkedin.com/in/md-jahid-hasan-9418b9298](https://www.linkedin.com/in/md-jahid-hasan-9418b9298)  
- Portfolio: [https://jahidhasanpiyesh.github.io/](https://jahidhasanpiyesh.github.io/)  
