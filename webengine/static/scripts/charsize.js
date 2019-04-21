function char_size(){
    if (document.getElementById("c_race").textContent == 'Tauren'){
        document.getElementById("picbox").style.backgroundSize ="620px 465px";
    }
    if ((document.getElementById("c_race").textContent == 'Worgen' || document.getElementById("c_race").textContent.includes('Draenei')) && document.getElementById("c_gender").textContent == 'Male'){
        document.getElementById("picbox").style.backgroundSize ="660px 495px";
    }
}
