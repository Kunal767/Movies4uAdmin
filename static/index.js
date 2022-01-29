
function saveData() {
    var contentTitle = document.getElementById('contentName').value;
    var imgLink = document.getElementById('imgUrl').value;
    var language = document.getElementById('language').value;
    var category = document.getElementById('category').value;
    var subtitles = document.getElementById('subtitles').value;
    var format = document.getElementById('format').value;

    var jsondata = {
        "ctitle": contentTitle,
        "imgurl": imgLink,
        "lang": language,
        "category": category,
        "subt": subtitles,
        "fmat": format
    }

    $.ajax({
        url: '/savetempcontent',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        data: JSON.stringify(jsondata),
        dataType: "json"
    })
}

function saveEditContentData(){
    var contentTitle = document.getElementById('contentName').value;
    var imgLink = document.getElementById('imgUrl').value;
    var description = document.getElementById('description').value;
    var language = document.getElementById('language').value;
    var release_year = document.getElementById('releaseyear').value;
    var duration = document.getElementById('duration').value;
    var category = document.getElementById('category').value;
    var subtitles = document.getElementById('subtitles').value;
    var format = document.getElementById('format').value;

    var jsondata = {
        "ctitle": contentTitle,
        "imgurl": imgLink,
        "desc": description,
        "lang": language,
        "ryear": release_year,
        "duration": duration,
        "category": category,
        "subt": subtitles,
        "fmat": format
    }

    $.ajax({
        url: '/saveedittempcontent',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        data: JSON.stringify(jsondata),
        dataType: "json"
    })
}