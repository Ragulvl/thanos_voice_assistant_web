document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.querySelector("input[type='text']");
    const sendButton = document.querySelector("button");
    const chatContainer = document.querySelector(".border-t");

    // Function to add a message to the chat
    function addMessage(text, isUser = true) {
        const messageWrapper = document.createElement("div");
        messageWrapper.classList.add("flex", "items-center", "space-x-4", "mb-4", "fade-in");
        if (isUser) messageWrapper.classList.add("justify-end");

        const message = document.createElement("div");
        message.classList.add("bg-gray-700", "p-4", "rounded-lg", "w-full", isUser ? "text-right" : "");
        message.innerHTML = `<p class="text-gray-200">${text}</p>`;
        
        if (isUser) {
            const userAvatar = document.createElement("img");
            userAvatar.src = "https://storage.googleapis.com/a1aa/image/zeGxWopRYbVhHyzMUn8z8jsLLCKBYfmwYRxArqMSpcNzo8sTA.jpg";
            userAvatar.classList.add("w-12", "h-12", "rounded-full");
            messageWrapper.append(message, userAvatar);
        } else {
            const aiAvatar = document.createElement("img");
            aiAvatar.src = "https://storage.googleapis.com/a1aa/image/DN0J8zrvYEqFLdTQaOexuffRoMfBS1XPn0IEZRFcA46GjyzOB.jpg";
            aiAvatar.classList.add("w-12", "h-12", "rounded-full");
            messageWrapper.append(aiAvatar, message);
        }
        
        chatContainer.appendChild(messageWrapper);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Function to handle sending a message
    function sendMessage() {
        const userMessage = inputField.value.trim();
        if (userMessage) {
            addMessage(userMessage); // Add user's message
            inputField.value = "";
            setTimeout(() => {
                addMessage("This is a response from Jarvis.", false); // Simulated AI response
            }, 1000);
        }
    }

    // Event listeners for sending messages
    sendButton.addEventListener("click", sendMessage);
    inputField.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});
