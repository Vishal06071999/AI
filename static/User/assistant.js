const commandEl = document.getElementById("command");
const responseEl = document.getElementById("response");

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.lang = "en-US";
recognition.continuous = true;
recognition.interimResults = false;

let processing = false;

let voices = [];

function loadVoices(){
    voices = speechSynthesis.getVoices();
}

loadVoices();
speechSynthesis.onvoiceschanged = loadVoices;

function speak(text){

    if(!text) return;

    const utter = new SpeechSynthesisUtterance(text);

    let voice = voices.find(v => v.lang.includes("en"));

    if(voice) utter.voice = voice;

    utter.rate = 1;
    utter.pitch = 1;

    speechSynthesis.speak(utter);

    utter.onend = ()=>{
        processing = false;
    }

}

function startListening(){

    try{
        recognition.start();
    }catch(e){}
}

window.onload = ()=>{
    startListening();
}

recognition.onresult = async (event)=>{

    if(processing) return;

    const command = event.results[event.results.length - 1][0].transcript.toLowerCase();

    commandEl.innerText = command;

    processing = true;

    try{

        const formData = new FormData();
        formData.append("command", command);

        const res = await fetch("/assistant",{
            method:"POST",
            body:formData
        });

        const data = await res.json();

        if(data.type === "redirect"){
            window.location.href = data.url;
            return;
        }

        if(data.type === "youtube"){
            window.open(data.url, "_blank");
        }

        responseEl.innerText = data.message;

        speak(data.message);

    }catch(err){

        console.log(err);
        processing = false;

    }

}

recognition.onerror = (e)=>{
    processing = false;
}

recognition.onend = ()=>{
    setTimeout(startListening,200);
}