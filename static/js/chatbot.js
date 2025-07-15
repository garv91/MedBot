document.getElementById('chat-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    appendMessage('user', message);
    input.value = '';

    const botMsg = appendMessage('bot', '...');
    botMsg.classList.add('typing');

    await fetchBotReply(message, botMsg);
});

function appendMessage(sender, text, time = null) {
    const chatBox = document.getElementById('chat-messages');
    const msgWrapper = document.createElement('div');
    msgWrapper.classList.add('message', sender);

    const msgText = document.createElement('div');
    msgText.textContent = text;
    msgWrapper.appendChild(msgText);

    const timestamp = document.createElement('div');
    timestamp.classList.add('timestamp');
    timestamp.textContent = time || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    msgWrapper.appendChild(timestamp);

    chatBox.appendChild(msgWrapper);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msgText;
}

async function fetchBotReply(message, botElement) {
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await response.json();
        botElement.parentElement.classList.remove('typing');
        botElement.textContent = '';
        await typeEffect(botElement, data.reply);

        if (data.sources && Array.isArray(data.sources)) {
            const sourceContainer = document.createElement('div');
            sourceContainer.className = 'sources';
            sourceContainer.innerHTML = data.sources.map((s, i) => `<div class="source">🔗 Source ${i + 1}: ${s}</div>`).join('');
            botElement.parentElement.appendChild(sourceContainer);
        }

    } catch (error) {
        botElement.textContent = "Sorry, there was an error.";
    }
}

function typeEffect(element, text, delay = 20) {
    return new Promise(resolve => {
        let i = 0;
        const interval = setInterval(() => {
            element.textContent += text.charAt(i);
            i++;
            if (i >= text.length) {
                clearInterval(interval);
                resolve();
            }
        }, delay);
    });
}
