let socket;
let teacher = document.getElementById("teacherName")
teacher.innerHTML = sessionStorage.getItem("Name")
let school = sessionStorage.getItem("School")
console.log(school)
function connectWebSocket() {
    socket = new WebSocket('ws://185.240.104.86:4949');//Burası Ana sunucu ıp olcak!!!!!!!!!!!!!!!!!!!!!!!
    socket.onopen = () => {
    console.log("WebSocket bağlantısı kuruldu!");
};
socket.onclose = () => {//bağlantı kapatıldığında
    console.log("WebSocket bağlantısı kapatıldı.");
};
socket.onerror = (error) => {
    console.error("WebSocket hatası:", error);
    };
socket.onmessage = (event) => {//mesaj alınması durumunda
    message = event.data;
    if (message === "YOK")
    {
        alert(`Sınıf Bulunamadı`);
    }
    else {
        alert(`şifre:${event.data}`);
    }
};
}
connectWebSocket()
function openBoard() {//açma emri
    let message = document.getElementById("selecting")
    message = message.value
    message = message.replaceAll(" ","")
    message = `${school}$${message}$open`
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(message);
    } else {
        alert("WebSocket bağlantısı açık değil!");
    }
    connectWebSocket()
}
function GetPass() {//şifre alma 
    let message = document.getElementById("selecting")
    message = message.value
    message = message.replaceAll(" ","")
    message =`${school}$${message}$givepass`
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(message);
    } else {
        alert("WebSocket bağlantısı açık değil!");
    }
    connectWebSocket()
}
function closeBoard(){//kapatma emri
    let message = document.getElementById("selecting")
    message = message.value
    message = message.replaceAll(" ","")
    message =`${school}$${message}$close`
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(message);
    } else {
        alert("WebSocket bağlantısı açık değil!");
    }
    connectWebSocket()
}
var elements = document.getElementsByClassName("engelle"); // buttonların temel yönlendirmesini engelleme
Array.from(elements).forEach(a => {
    a.addEventListener("click", function(event) {
        event.preventDefault();
    });
});

if(sessionStorage.getItem("Logined") !== "true")//Login kontrolü
{
    window.location.href = "/login.html";
}