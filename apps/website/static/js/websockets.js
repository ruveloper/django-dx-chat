/*
* Chat and WebScokets modules
* ------------------------------------------------------------------------------------------
 */

// * Constans
const USER_CHAT_ENTRY = "user-chat-entry w-fit h-full p-4 shrink-0 flex items-center md:w-full md:h-fit hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
const USER_CHAT_ENTRY_SELECTED = "user-chat-entry w-fit h-full p-4 shrink-0 flex items-center md:w-full md:h-fit bg-blue-100 dark:bg-blue-600"
const USER_CHAT_ENTRY_AVATAR = "w-10 h-10 flex-none mr-2 rounded-full bg-teal-600"
const CHAT_BUBBLE_INFO_CLASSES = "p-2 rounded-lg text-center font-normal bg-gray-100 dark:bg-gray-600"
const CHAT_BUBBLE_LOGGED_USER_CLASSES = "ml-8 p-3 rounded-lg md:ml-28 bg-violet-100 dark:bg-violet-800"
const CHAT_BUBBLE_USER_CLASSES = "mr-8 p-3 rounded-lg md:mr-28 bg-indigo-100 dark:bg-indigo-800"

// * Elements
const onlineUsersWindow = document.getElementById("online-users-window");
// Chat window related
const placeholderChatWindowEl = document.getElementById("placeholder-chat-window")
const chatWindowEl = document.getElementById("chat-window");
const chatWindowScrollEl = document.getElementById("chat-window-scroll");
const chatWindowCleanEl = document.getElementById("chat-window-clean");
const chatWindowCloseEl = document.getElementById("chat-window-close");
// Global actions related
const chatMessagesWindowEl = document.getElementById("chat-messages-window");
// Send messages related
const chatInputMessageEl = document.getElementById("chat-input-message")
const chatSendMessageEl = document.getElementById("chat-send-message")

// * Globals
let userChatMessages = {} // ex: { username1: [ {type: "", user: "", message: ""}, ... ], ... }
let usersWebsockets = {}; // ex: { username1: userWebsocket:WebSocket, username2:  ... }
let activeUserWebsocket = null;
let activeChatUser = null;
let activeLoggedUser = null;
let activeSendChatMessage = false;

// * Listerners
// * Chat Messages Windows Scroll -
// Scroll to end on message added if chatWindowScrollEl is checked
chatMessagesWindowEl.addEventListener("DOMNodeInserted", (e) => {
    if (chatWindowScrollEl.checked) {
        chatMessagesWindowEl.scrollTo({
            left: 0,
            top: (chatMessagesWindowEl.scrollHeight - chatMessagesWindowEl.offsetHeight),
            behavior: "smooth",
        });
    }
});


// * Funtions
function updateOnlineUsers(loggedUser, usersOnline) {
    // Clean online users window
    while (onlineUsersWindow.firstChild) {
        onlineUsersWindow.removeChild(onlineUsersWindow.firstChild);
    }
    // Create element for each user online and append to online users window
    for (let chatUser in usersOnline) {
        const avatar_url = usersOnline[chatUser]
        // ! If chatUser equals to loggedUser skip this iteration (Shouldn't be listed in online users)
        if (chatUser === loggedUser) {
            continue;
        }
        // * Create chat entry
        const userChatEntry = document.createElement("button")
        userChatEntry.setAttribute("data-logged-user", loggedUser)
        userChatEntry.setAttribute("data-chat-user", chatUser)
        userChatEntry.setAttribute("data-chat-user-avatar", avatar_url)
        userChatEntry.className = USER_CHAT_ENTRY
        const img = document.createElement("img")
        img.src = avatar_url
        img.alt = `${chatUser} avatar`
        img.className = USER_CHAT_ENTRY_AVATAR
        userChatEntry.append(img, chatUser)
        // * Add element to online users window
        onlineUsersWindow.append(userChatEntry)
        // * Attach onClick event
        onClickChatEntry();
    }

}

function onClickChatEntry() {
    // Attach or update onClick event to each chat entry
    const chatEntriesEls = document.querySelectorAll(".user-chat-entry");
    chatEntriesEls.forEach((chatEntry) => {
        // Get users data from data attributes
        const loggedUser = chatEntry.dataset.loggedUser
        const chatUser = chatEntry.dataset.chatUser
        const chatUserAvatar = chatEntry.dataset.chatUserAvatar
        // Init chat on click
        chatEntry.onclick = () => {
            // Get user websocket
            let userWebsocket = chatUser in usersWebsockets ? usersWebsockets[chatUser] : connectUserWebsocket(chatUser);
            // Set active websocket and chat username associated to selected chat
            activeUserWebsocket = userWebsocket;
            activeChatUser = chatUser;
            // Open chat process
            openChat(chatUser, chatUserAvatar, userWebsocket);
        };

    });
}

function toggleChatWindow(close = false) {
    if (close) {
        placeholderChatWindowEl.classList.remove("hidden");
        chatWindowEl.classList.add("hidden");
        return
    }
    placeholderChatWindowEl.classList.add("hidden");
    chatWindowEl.classList.remove("hidden");
}

function toggleActiveChatEntry(chatUser) {
    // Attach or update onClick event to each chat entry
    const chatEntriesEls = document.querySelectorAll(".user-chat-entry");
    chatEntriesEls.forEach((chatEntry) => {
        if (chatUser === chatEntry.dataset.chatUser) {
            chatEntry.className = USER_CHAT_ENTRY_SELECTED;
            chatEntry.setAttribute("disabled", "");
            return null;
        }
        chatEntry.className = USER_CHAT_ENTRY
        chatEntry.removeAttribute("disabled")
    });
}

function openChat(chatUser, chatUserAvatar) {
    // Update chat user window
    document.getElementById("chat-user-window-avatar").src = chatUserAvatar
    document.getElementById("chat-user-window-username").innerText = chatUser
    // Clean chat messages window
    while (chatMessagesWindowEl.firstChild) {
        chatMessagesWindowEl.removeChild(chatMessagesWindowEl.firstChild);
    }
    // * Load stored messages in the chat window
    if (userChatMessages[activeChatUser] !== undefined) {
        userChatMessages[activeChatUser].forEach((chatMessage) => {
            addChatMessage(chatMessage["type"], chatMessage["user"], chatMessage["message"])
        })
    }
    // Show chat window
    toggleChatWindow();
    // Set active chat entry
    toggleActiveChatEntry(chatUser)
    // Focus to send
    chatInputMessageEl.focus();
}

function cleanChat(chatUser) {
    // Clean chat messages window
    while (chatMessagesWindowEl.firstChild) {
        chatMessagesWindowEl.removeChild(chatMessagesWindowEl.firstChild);
    }
    // * Clean stored chat messages of actual chat user
    userChatMessages[chatUser] !== undefined ? delete userChatMessages[chatUser] : null
}

function closeChat(chatUser) {
    // Close chat window and websocket
    switch (true) {
        // If chatUser is the active user, close the active websocket and the chat window
        case (chatUser === activeChatUser):
            activeUserWebsocket.close();
            delete usersWebsockets[activeChatUser];
            activeUserWebsocket = activeChatUser = null;
            toggleChatWindow(true);
            break;
        // Otherwise, close and delete the stored websocket
        case (chatUser !== activeChatUser && chatUser in usersWebsockets):
            usersWebsockets[chatUser].close()
            delete usersWebsockets[chatUser];
            break;
    }
    // Toggle active chat entry
    toggleActiveChatEntry(false)
}

function addChatMessage(type, user, message) {
    // Get element style classes based on type
    let elClasses = null;
    switch (true) {
        case type === "chat.information":
            elClasses = CHAT_BUBBLE_INFO_CLASSES;
            break;
        case (type === "chat.message" && user === activeLoggedUser) :
            elClasses = CHAT_BUBBLE_LOGGED_USER_CLASSES;
            break;
        case (type === "chat.message" && user === activeChatUser) :
            elClasses = CHAT_BUBBLE_USER_CLASSES;
            break;
    }
    // Create <p> element
    let pEl = document.createElement("p");
    pEl.className = elClasses;
    pEl.innerText = message
    // Add element to chat message window
    chatMessagesWindowEl.appendChild(pEl)
}

function storeChatMessage(chatUser, type, user, message) {
    // Init array if it hasn't already been done
    userChatMessages[chatUser] === undefined ? userChatMessages[chatUser] = [] : null
    // Store message for the active chat user
    userChatMessages[chatUser].push({
        type: type,
        user: user,
        message: message,
    })
}

function activateSendChatMessage(loggedUser, chatUser, connectedUsers) {
    // * If both users are connected, active function (and html elements) to send chat messages,
    // * otherwise, desactivate
    if(connectedUsers.includes(loggedUser) && connectedUsers.includes(chatUser) ){
        chatInputMessageEl.removeAttribute("disabled");
        chatSendMessageEl.removeAttribute("disabled");
        activeSendChatMessage = true;
    } else {
        chatInputMessageEl.setAttribute("disabled", "");
        chatSendMessageEl.setAttribute("disabled", "");
        activeSendChatMessage = false;
    }
}

function sendChatMessage() {
    if(!activeSendChatMessage){
        return;
    }
    // Get message from chat input
    const inputMessage = chatInputMessageEl.value;
    if (!inputMessage) return
    // Format the message
    const msg = {
        type: "chat.message",
        user: activeLoggedUser,
        message: inputMessage,
    }
    // Send message
    activeUserWebsocket.send(JSON.stringify(msg))
    // Clean chat input element
    chatInputMessageEl.value = "";
    chatInputMessageEl.focus();
}

// * Websockets
function connectStateWebsocket() {
    const stateWebsocket = new WebSocket(`ws://${window.location.host}/state/`)
    // Websockets events
    stateWebsocket.onopen = function (e) {
        console.log("The user state connection was OPEN");
    };
    stateWebsocket.onclose = function (e) {
        console.log("The user state connection was CLOSE");
    };
    stateWebsocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if (data["type"] === "state.users.online") {
            let loggedUser = data["user"];
            let usersOnline = data["message"];
            // Set global active logged user
            activeLoggedUser = data["user"]
            // Update list of online users
            updateOnlineUsers(loggedUser, usersOnline);
        }
    }
    return stateWebsocket;
}

function connectUserWebsocket(chatUser) {
    // Assing the socket url based on the selected chatUser
    const ws_url = chatUser === "echo"
        ? `ws://${window.location.host}/chat/echo/`
        : `ws://${window.location.host}/chat/?chat_user=${chatUser}`
    // Create a new Socket
    const userWebsocket = new WebSocket(ws_url);
    // Websockets events
    userWebsocket.onopen = function (e) {
        console.log("The chat connection was OPEN for --> " + chatUser);
    };
    userWebsocket.onclose = function (e) {
        console.log("The chat connection was CLOSE for --> " + chatUser);
        closeChat(chatUser);
    };
    userWebsocket.onmessage = function (e) {
        const data = JSON.parse(e.data)
        // * Handle chat room type messages
        if(data["type"].includes("chat.room.users")) {
            activateSendChatMessage(data["user"], data["chat_user"], data["message"])
        }
        // * Handle chat user messages and information type
        if (data["type"].includes("chat.message") || data["type"].includes("chat.information")) {
            // Add message to chat window if correspond to the active chat user or the logged user
            if (data["user"] === activeChatUser || data["user"] === activeLoggedUser) {
                addChatMessage(data["type"], data["user"], data["message"])
            }
            // Store chat message in userChatMessages except for chat.information type
            storeChatMessage(chatUser, data["type"], data["user"], data["message"])
            // data["type"] !== "chat.information"
            //     ? storeChatMessage(chatUser, data["type"], data["user"], data["message"])
            //     : null
        }
    }
    // Store websocket object and return
    usersWebsockets[chatUser] = userWebsocket;
    return userWebsocket;
}

// * Websocket State
// * -------------------------------------------------------------------
// Connect to the state websocket in order to notify our online status and
// get the users online
let stateWebsocket = connectStateWebsocket()

// * Start Chat
// * -------------------------------------------------------------------
onClickChatEntry();

// * Send Message
// * -------------------------------------------------------------------
chatInputMessageEl.onkeyup = (e) => e.key === "Enter" ? sendChatMessage() : null;
chatSendMessageEl.onclick = () => sendChatMessage();

// * Clean Chat
// * -------------------------------------------------------------------
chatWindowCleanEl.onclick = () => cleanChat(activeChatUser);

// * Close Chat
// * -------------------------------------------------------------------
chatWindowCloseEl.onclick = () => closeChat(activeChatUser);
