EMOTE_SERVER = "http://127.0.0.1:5000";


// functions for fill sidebar
// fill categories
function fillSidebarContent(name, cats) {
    for (i = 0; i < cats.length; i++) {
        if (name != "authors") {
            cname = cats[i].toLowerCase();
        } else {
            cname = cats[i];
        }

        $('div[name="' + name + '"]').append(
            "<div class='wrap-content line-radio'>" +
            "<input type='radio' id='line' style='display:none'>" +
            "<img src='images/radio_off.svg' alt='unchecked'>" +
            "<label for='line' class='line-label' style='padding-left: 4px;'>" +
            cname + 
            "</label></div>"
        )
    }
}

//sidebar radio buttons click
function clickRadio() {
    // get radio state
    image = $(this).children('img');
    checkbox = $(this).children('input');
    state = checkbox.is( ":checked" );

    console.log($(this));
    console.log(checkbox);
    console.log(state);
    console.log('end');

    if (!state) {
        checkbox.attr('checked', true);
        image.attr('src', 'images/radio_on.svg');
        image.attr('alt', 'checked');
    } else {
        checkbox.attr('checked', false);
        image.attr('src', 'images/radio_off.svg');
        image.attr('alt', 'unchecked');
    }
}

//sidevar click title 
function clickTitle() {
    image = $(this).children().children();
    content = $(this).next();

    image.toggleClass('rotate');
    state = content.attr('style');
    if (state === 'display: none;') {
        content.attr('style', 'display: block;');
        content.toggleClass('fade-insert');
    } else {
        content.attr('style', 'display: none;');
        content.toggleClass('fade-insert');
    }
}

function loadEmotes(query, categories, tags, authors, page, limit){}

async function loadSidebar(endpoint) {
    return $.ajax({
        url: EMOTE_SERVER + endpoint,
        method: 'GET',
        dataType: 'json',
    })

}

function showGIF() {
    console.log("show gif");
    console.log($(this));
    image = $(this).children().children('div[class="emote-img"]').children('img');
    image.attr('style', 'display: none;');
    wait = $(this).children().children('div[class="emote-img"]').prev();
    wait.attr('style', 'display: flex;');
    // get src
    img_name = image.attr('src');
    // get regex ([\S]+)\/(.+).(?:gif|png|jpg)
    regex = /[\S]+\/(.+).(?:gif|png|jpg)/;
    match = regex.exec(img_name);

    // get 1 group 
    _name = match[1];

    console.log(_name);

    //image.attr('src', 'images/' + _name + '.gif');
}

function hideGIF() {
    console.log("hide gif");
    image = $(this).children().children('div[class="emote-img"]').children('img');
    wait = $(this).children().children('div[class="emote-img"]').prev();
    console.log(image);
    //img_src = image.attr('src');



    //image.attr('style', '');
    //wait.attr('style', 'display: none;');
    //console.log(image);
    // get src
    //img_name = image.attr('src');
    //console.log(img_name);
    // get regex ([\S]+)\/(.+).(?:gif|png|jpg)
    //regex = /[\S]+\/(.+).(?:gif|png|jpg)/;
    //match = regex.exec(img_src);

    // get 1 group 
    //_name = match[1];
    //console.log(_name);

    //console.log(_name);

    //image.attr('src', 'images/' + _name + '.png');
}


function search(query, categories, tags, authors, page, limit) {
    $.ajax({
        url: EMOTE_SERVER + '/search',
        method: 'GET',
        dataType: 'json',
        data: {
            query: query,
            categories: categories,
            tags: tags,
            authors: authors,
            page: page,
            limit: limit
        }
    }).then(function(data) {
        console.log(data);
        for (i = 0; i < data.data.length; i++) {
            $.ajax({
                url: EMOTE_SERVER + '/emote/' + data.data[i].uuid,
                method: 'GET',
                dataType: 'json'
            }).then(function(edata) {
                console.log(edata);
                addEmote(
                    edata.data.json.name, 
                    edata.data.json.author, 
                    edata.data.png, 
                    edata.data.gif, 
                    edata.data.uuid
                );
            })
        }
    })
}



function addEmote(title, author, png, gif, id) {
    emote = document.createElement('div');
    emote.className = 'emote';
    // set id 
    emote.id = id;

    emote_header = document.createElement('div');
    emote_header.className = 'emote-header';

    emote_wait = document.createElement('div');
    emote_wait.className = 'wait loading';
    emote_wait.style.display = 'none';

    logo = document.createElement('img');
    logo.src = 'images/logo.svg';
    logo.alt = 'wait';

    emote_img = document.createElement('div');
    emote_img.className = 'emote-img';

    png_img = document.createElement('img');
    png_img.src = 'data:image/png;base64, ' + png;
    png_img.alt = 'png';

    gif_img = document.createElement('img');
    gif_img.src = 'data:image/png;base64, ' + gif;
    gif_img.alt = 'gif';
    gif_img.style.display = 'none';

    emote_like = document.createElement('div');
    emote_like.className = 'emote-like';

    emote_like_img = document.createElement('img');
    emote_like_img.src = 'images/heart_outline.svg';
    emote_like_img.alt = 'like';

    emote_footer = document.createElement('div');
    emote_footer.className = 'emote-footer';

    emote_footer_content = document.createElement('div');
    emote_footer_content.className = 'emote-footer-content';

    emote_title = document.createElement('div');
    emote_title.className = 'emote-title';

    title_span = document.createElement('span');
    title_span.innerText= title;

    console.log(title_span);

    emote_author = document.createElement('div');
    emote_author.className = 'emote-author';

    author_span = document.createElement('span');
    author_span.innerHTML = author;

    emote_download = document.createElement('div');
    emote_download.className = 'emote-download';

    emote_download_img = document.createElement('img');
    emote_download_img.src = 'images/download.svg';

    emote.appendChild(emote_header);
    emote.appendChild(emote_footer);

    emote_header.appendChild(emote_wait);
    emote_wait.appendChild(logo);
    emote_header.appendChild(emote_img);
    emote_img.appendChild(png_img);
    emote_img.appendChild(gif_img);
    emote_header.appendChild(emote_like);
    emote_like.appendChild(emote_like_img);

    emote_footer.appendChild(emote_footer_content);
    emote_footer_content.appendChild(emote_title);
    emote_title.appendChild(title_span);
    emote_footer_content.appendChild(emote_author);
    emote_author.appendChild(author_span);
    emote_footer_content.appendChild(emote_download);
    emote_download.appendChild(emote_download_img);

    emote = $(emote);

    emote.appendTo('div[class="emotes-grid"]')

    //$('div[class="emotes-grid"]').append(emote);
    console.log(emote);

    $(".emote").hover(showGIF, hideGIF)

    return emote;
}

// onload func 
$(document).ready(() => {
    console.log("ready");

    loadSidebar('/categories').then(function(resp) {
        fillSidebarContent("categories", resp.data);
    })

    loadSidebar('/tags').then(function(resp) {
        fillSidebarContent("tags", resp.data);
    })

    loadSidebar('/authors').then(function(resp) {
        fillSidebarContent("authors", resp.data);
    })

    search();
})

// run after document load
$(window).load(function(){
    // func for sidebar radio buttons
    $(".line-radio").click(clickRadio)

    // func for title in sidebar, for transform image
    $(".title-flipper").click(clickTitle)

    // hover on image
    $(".emote").hover(showGIF, hideGIF)
});