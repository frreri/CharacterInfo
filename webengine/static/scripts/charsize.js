function char_size() {

    var size_L = ['Tauren', 'Orc'];
    var size_M = ['Worgen', 'Draenei', 'Lightforged Draenei', 'Night Elf', 'Nightborne'];

    if (size_L.includes(document.getElementById("c_race").textContent)) {
        document.getElementById("picbox").style.backgroundSize = "620px 465px";
    } else if (size_M.includes(document.getElementById("c_race").textContent) && document.getElementById("c_gender").textContent == 'Male') {
        document.getElementById("picbox").style.backgroundSize = "660px 495px";
    }

}
