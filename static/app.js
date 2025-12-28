const inputArea = document.getElementById('sourceTextArea');
const outputArea = document.getElementById('resultDiv');
const loader = document.getElementById('loader');
const targetLangInput = document.getElementById('targetLangCode');
const selectedLangNameDisplay = document.getElementById('selectedLangName');

// CSRF Token সংগ্রহের সঠিক ফাংশন
function getCSRF() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function autoResizeInput() {
    inputArea.style.height = 'auto';
    inputArea.style.height = inputArea.scrollHeight + 'px';
}

function toggleMenu(event) {
    event.stopPropagation();
    document.getElementById("userMenu").classList.toggle("show-dropdown");
}

window.onclick = (e) => {
    if (!e.target.closest('.user-menu-wrapper')) {
        document.getElementById("userMenu").classList.remove('show-dropdown');
    }
}

// Search Filter
document.getElementById('langSearchInput').addEventListener('input', function () {
    const filter = this.value.toLowerCase();
    document.querySelectorAll('.lang-option').forEach(opt => {
        opt.style.display = opt.textContent.toLowerCase().includes(filter) ? "block" : "none";
    });
});

// Language Select
const modalEl = document.getElementById('languageModal');
const bootstrapModal = new bootstrap.Modal(modalEl);
document.querySelectorAll('.lang-option').forEach(opt => {
    opt.addEventListener('click', function () {
        targetLangInput.value = this.dataset.code;
        selectedLangNameDisplay.innerText = this.dataset.name;
        bootstrapModal.hide();
        performTranslation();
    });
});

function loadHistory(source, translated, langCode) {
    inputArea.value = source;
    const formattedText = translated.replace(/\n/g, '<br>');
    outputArea.innerHTML = `<div style="text-align:left; color:#000; width:100%;">${formattedText}</div>`;
    targetLangInput.value = langCode;
    autoResizeInput();
    const sidebar = bootstrap.Offcanvas.getInstance(document.getElementById('historySidebar'));
    if (sidebar) sidebar.hide();
}

function performTranslation() {
    const text = inputArea.value.trim();
    const placeholderMsg = outputArea.getAttribute('data-placeholder'); // HTML থেকে অনুবাদিত টেক্সট নেয়া

    if (text.length > 5000) {
        Swal.fire({ icon: 'warning', title: 'Text Too Long', text: 'Max 5000 characters allowed.' });
        return;
    }

    if (!text) {
        outputArea.innerHTML = `<span class="placeholder-text">${placeholderMsg}</span>`;
        return;
    }

    loader.style.display = 'block';
    outputArea.style.opacity = '0.5';

    fetch('/translate-api/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRF() // এখানে টোকেনটি পাঠানো হচ্ছে
        },
        body: JSON.stringify({ 'text': text, 'target': targetLangInput.value })
    })
    .then(res => res.json())
    .then(data => {
        loader.style.display = 'none';
        outputArea.style.opacity = '1';
        if (data.translated_text) {
            const formattedText = data.translated_text.replace(/\n/g, '<br>');
            outputArea.innerHTML = `<div style="text-align:left; color:#000; width:100%;">${formattedText}</div>`;
        }
    })
    .catch(err => {
        loader.style.display = 'none';
        outputArea.style.opacity = '1';
        console.error(err);
    });
}

// Auto-translate on input with debounce
let timeout = null;
inputArea.addEventListener('input', () => {
    autoResizeInput();
    clearTimeout(timeout);
    timeout = setTimeout(performTranslation, 700);
});

document.getElementById('clearBtn').onclick = () => {
    inputArea.value = '';
    inputArea.style.height = '180px';
    performTranslation();
};

document.getElementById('copyBtn').onclick = () => {
    const textToCopy = outputArea.innerText;
    if (textToCopy && !textToCopy.includes('Translation results')) {
        navigator.clipboard.writeText(textToCopy);
        Swal.fire({ title: 'Copied!', toast: true, position: 'top-end', showConfirmButton: false, timer: 1500, icon: 'success' });
    }
};

// Voice recognition setup
const voiceBtn = document.getElementById('voiceBtn');
const micIcon = document.getElementById('micIcon');
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    voiceBtn.onclick = () => {
        micIcon.classList.contains('recording') ? recognition.stop() : recognition.start();
    };
    recognition.onstart = () => micIcon.classList.add('recording', 'fa-microphone-alt');
    recognition.onresult = (e) => {
        inputArea.value = e.results[0][0].transcript;
        autoResizeInput();
        performTranslation();
    };
    recognition.onend = () => micIcon.classList.remove('recording', 'fa-microphone-alt');
}