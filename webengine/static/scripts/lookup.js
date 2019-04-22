function search_char(){
    document.getElementsByClassName("hideable-content").style.display = "none";
    document.getElementById("load-anim").style.display = "block";
    var url="http://frer.se/lookup/" + document.getElementById("realm_c").value + "/" + document.getElementById("name_c").value.toLowerCase();
    location.href=url;
    return false;
}
