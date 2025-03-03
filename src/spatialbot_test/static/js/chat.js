
function sendMessage() {
    const userInput = document.getElementById('user-input').value;

    if (!userInput) return;

    // Ajouter le message de l'utilisateur dans la fenêtre de chat
    const chatArea = document.getElementById('chat-area');
    chatArea.innerHTML += `<div class="user-message">${userInput}</div>`;
    document.getElementById('user-input').value = '';

    // Envoyer le message à l'API Flask
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Afficher la réponse du chatbot
        chatArea.innerHTML += `<div class="bot-message">${data.response}</div>`;
        chatArea.scrollTop = chatArea.scrollHeight;
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}
const sendBtn = document.getElementById('sendBtn');
    const chatbox = document.getElementById('chatbox');
    const dbNameInput = document.getElementById('db_name');
    const hostInput = document.getElementById('host');
    const userInput = document.getElementById('user');
    const passwordInput = document.getElementById('password');

    const layersSelect = document.getElementById('layers');
    const loadLayersBtn = document.getElementById('loadLayersBtn');
    const sendPromptBtn = document.getElementById('sendPromptBtn');
    const promptInput = document.getElementById('prompt');

    let step = 0;

   

    sendBtn.addEventListener('click', async function () {
        const userInputValue = step === 0 ? dbNameInput.value :
                              step === 1 ? hostInput.value :
                              step === 2 ? userInput.value :
                              step === 3 ? passwordInput.value : "";
        
        if (userInputValue) {
            // N'affichez pas le mot de passe dans le chat
            if (step !== 3) {
                chatbox.innerHTML += `<div class="chat-message user">${userInputValue}</div>`;
            }
            if (step === 0) {
                step++;
                chatbox.innerHTML += `<div class="chat-message bot">Entrez l'hôte de la base de données.</div>`;
                dbNameInput.style.display = 'none';
                hostInput.style.display = 'block';
            } else if (step === 1) {
                step++;
                chatbox.innerHTML += `<div class="chat-message bot">Entrez votre nom d'utilisateur.</div>`;
                hostInput.style.display = 'none';
                userInput.style.display = 'block';
            } else if (step === 2) {
                step++;
                chatbox.innerHTML += `<div class="chat-message bot">Entrez votre mot de passe.</div>`;
                userInput.style.display = 'none';
                passwordInput.style.display = 'block';
            } else if (step === 3) {
                const response = await fetch('/connect_db', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        db_name: dbNameInput.value,
                        host: hostInput.value,
                        user: userInput.value,
                        password: passwordInput.value
                    })
                });
                const data = await response.json();
                if (data.success) {
                    chatbox.innerHTML += `<div class="chat-message bot">Connexion réussie ! Que voulez-vous faire ?</div>`;
                    // Ajoutez ici d'autres interactions pour afficher les layers ou d'autres actions
                    step++;
                    loadLayers();
                } else {
                    chatbox.innerHTML += `<div class="chat-message bot">Erreur de connexion : ${data.error}</div>`;
                }
                passwordInput.style.display = 'none';
            }
            chatbox.scrollTop = chatbox.scrollHeight;
        }
    });

    // Charger les couches
     function loadLayers() {
        console.log("1");
        const response =  fetch('/get_layers_name');
        // const data =  response.json();
        console.log("response ", response);
        if (data.success) {
            chatbox.innerHTML += `<div class="chat-message bot">Voici les couches disponibles :</div>`;
            console.log("data ", data);
        //     data.layers.forEach(layer => {
        //         const option = document.createElement('option');
        //         option.value = layer;
        //         option.textContent = layer;
        //         layersSelect.appendChild(option);
        //     });
            
        //  // Afficher la sélection des couches
        //  document.querySelector('.input-container').style.display = 'block'; 
        } 
         else {
            chatbox.innerHTML += `<div class="chat-message bot">Erreur lors du chargement des couches : ${data.error}</div>`;
        }       
    }

   


    window.onload = function () {
        chatbox.innerHTML += `<div class="chat-message bot">Entrez le nom de la base de données.</div>`;
        dbNameInput.style.display = 'block';


         // Envoyer les couches sélectionnées
    loadLayersBtn.addEventListener('click', async function () {
        const selectedLayers = Array.from(layersSelect.selectedOptions).map(option => option.value);
        chatbox.innerHTML += `<div class="chat-message user">Couches sélectionnées : ${selectedLayers.join(', ')}</div>`;

        // Vous pouvez maintenant utiliser ces couches pour effectuer d'autres actions
    });

    // Envoyer un prompt SQL
    sendPromptBtn.addEventListener('click', async function () {
        const prompt = promptInput.value;
        chatbox.innerHTML += `<div class="chat-message user">Prompt SQL : ${prompt}</div>`;
        const response = await fetch('/process_prompt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                db_name: dbNameInput.value,
                host: hostInput.value,
                user: userInput.value,
                password: passwordInput.value,
                prompt: prompt
            })
        });

        const data = await response.json();
        if (data.success) {
            chatbox.innerHTML += `<div class="chat-message bot">Résultat du prompt : ${JSON.stringify(data.result)}</div>`;
        } else {
            chatbox.innerHTML += `<div class="chat-message bot">Erreur dans le prompt : ${data.error}</div>`;
        }
    });
    };



