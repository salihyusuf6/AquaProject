let socket;
function connectWebSocket() {//son olarak  burası
    socket = new WebSocket('ws://185.240.104.86:4949');
    socket.onopen = () => {
    console.log("WebSocket bağlantısı kuruldu!");
};
socket.onclose = () => {
    console.log("WebSocket bağlantısı kapatıldı.");
};
socket.onerror = (error) => {
    console.error("WebSocket hatası:", error);
};
socket.onmessage = (event) =>{
    if (event.data != "False")
    {
        sessionStorage.setItem("Logined", "true")
        sessionStorage.setItem("Name",event.data)
        sessionStorage.setItem("School",document.getElementById("SchoolMenu").value)
        window.location.href = "/home.html";
    }
    else if(event.data == "False")
    {
        alert("Öğretmen Id veya şifre yanlış")
    }
};}
function sendLoginRequest() {
    let name = document.getElementById("name")
    let password = document.getElementById("passwords")
    let menu = document.getElementById("SchoolMenu")
    menu = menu.value
    menu.replaceAll(" ","_")
    name = name.value
    name = name.replaceAll(" ","_")
    password = password.value
    password = password.replaceAll(" ","")
    if (socket && socket.readyState === WebSocket.OPEN) {
        let message = `${menu}$${name}$${password}$login`
        socket.send(message);
    } else {
        alert("WebSocket bağlantısı açık değil!");
    }
    connectWebSocket()
}
connectWebSocket()
var elements = document.getElementsByClassName("engelle");
Array.from(elements).forEach(a => {
    a.addEventListener("click", function(event) {
        event.preventDefault();
    });
});