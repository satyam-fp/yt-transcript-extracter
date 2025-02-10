document.addEventListener('DOMContentLoaded', function() {
    let items = [];

    const customItemInput = document.getElementById('custom-item-input');
    const addCustomItemBtn = document.getElementById('add-custom-item-btn');
    const suggestionSelect = document.getElementById('suggestion-select');
    const addSelectedBtn = document.getElementById('add-selected-btn');
    const itemsList = document.getElementById('items-list');
    const generateMenuBtn = document.getElementById('generate-menu-btn');
    const regenerateMenuBtn = document.getElementById('regenerate-menu-btn');
    const voiceInputBtn = document.getElementById('voice-input-btn');
    const menuResultDiv = document.getElementById('menu-result');

    // Update the UI list to reflect the current items in the fridge.
    function updateItemsList() {
        itemsList.innerHTML = "";
        items.forEach((item, index) => {
            let li = document.createElement('li');
            li.className = "list-group-item d-flex justify-content-between align-items-center";
            li.textContent = item;
            let removeBtn = document.createElement('button');
            removeBtn.className = "btn btn-sm btn-danger";
            removeBtn.textContent = "Remove";
            removeBtn.addEventListener('click', function() {
                items.splice(index, 1);
                updateItemsList();
            });
            li.appendChild(removeBtn);
            itemsList.appendChild(li);
        });
    }

    // Add custom ingredient from the text input.
    addCustomItemBtn.addEventListener('click', function() {
        let value = customItemInput.value.trim();
        if (value && !items.includes(value)) {
            items.push(value);
            updateItemsList();
            customItemInput.value = "";
        }
    });

    // Add selected ingredients from the multi-select suggestions.
    addSelectedBtn.addEventListener('click', function() {
        const selectedOptions = Array.from(suggestionSelect.selectedOptions).map(option => option.value);
        selectedOptions.forEach(item => {
            if (item && !items.includes(item)) {
                items.push(item);
            }
        });
        updateItemsList();
    });

    // Send the list of items in the fridge to the backend to generate the menu.
    function generateMenu() {
        fetch("/generate-menu", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ items: items })
        })
        .then(response => response.json())
        .then(data => {
            if(data.menu) {
                // Use Marked.js to parse Markdown into HTML.
                menuResultDiv.innerHTML = marked.parse(data.menu);
            } else if(data.error) {
                menuResultDiv.innerHTML = `<span class="text-danger">${data.error}</span>`;
            }
        })
        .catch(error => {
            menuResultDiv.innerHTML = `<span class="text-danger">${error}</span>`;
        });
    }

    generateMenuBtn.addEventListener('click', generateMenu);
    regenerateMenuBtn.addEventListener('click', generateMenu);

    // Set up voice recognition using the Web Speech API.
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            // Call backend to process the transcript and extract the items list.
            fetch("/process-voice", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ voice_text: transcript })
            })
            .then(response => response.json())
            .then(data => {
                if(data.items) {
                    // Add extracted items if they are not duplicates.
                    data.items.forEach(item => {
                        if(item && !items.includes(item)) {
                            items.push(item);
                        }
                    });
                    updateItemsList();
                } else if(data.error) {
                    alert("Error processing voice input: " + data.error);
                }
            })
            .catch(error => {
                alert("Error processing voice input: " + error);
            });
        };

        recognition.onerror = function(event) {
            alert("Voice recognition error: " + event.error);
        };

        voiceInputBtn.addEventListener('click', function() {
            recognition.start();
        });
    } else {
        voiceInputBtn.disabled = true;
        voiceInputBtn.textContent = "Voice Input Not Supported";
    }
}); 