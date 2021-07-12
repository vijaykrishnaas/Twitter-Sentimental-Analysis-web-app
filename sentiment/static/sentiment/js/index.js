function preloader() {
    var styles = {
        "display": "block",
        "width": "100%",
        "height": "100%",
        "margin": "auto",
        "position": "absolute",
        "top": "45%",
        "text-align": "center"
    }
    document.getElementById("content").style.display = "none";
    document.getElementById("navigation").style.display = "none";
    document.documentElement.style.overflowY = "hidden";
    document.body.style.overflowY = "hidden";
    var obj = document.getElementById("loading");
    Object.assign(obj.style, styles);
}

function EnableDisable(searchField) {
    var btnSubmit = document.getElementById("searchButton");
    if (searchField.value.trim() != "") {
        btnSubmit.disabled = false;
    } else {
        btnSubmit.disabled = true;
    }
}