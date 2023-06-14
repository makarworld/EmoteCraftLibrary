EMOTE_SERVER = "http://127.0.0.1:5000";

function colour (text) {
    left = htmlEncode("<");  
    right = htmlEncode(">");
    text = text.replace(/</gi, left);  
    text = text.replace(/>/gi, right);
    text = text.replace(/\n/gi, "§r<br />");
    //colours
    text = text.replace(/§0/gi,'</span>§r<span class="c-1">');
    text = text.replace(/§1/gi,'</span>§r<span class="c-2">');
    text = text.replace(/§2/gi,'</span>§r<span class="c-3">');
    text = text.replace(/§3/gi,'</span>§r<span class="c-4">');
    text = text.replace(/§4/gi,'</span>§r<span class="c-5">');
    text = text.replace(/§5/gi,'</span>§r<span class="c-6">');
    text = text.replace(/§6/gi,'</span>§r<span class="c-7">');
    text = text.replace(/§7/gi,'</span>§r<span class="c-8">');
    text = text.replace(/§8/gi,'</span>§r<span class="c-9">');
    text = text.replace(/§9/gi,'</span>§r<span class="c-10">');
    text = text.replace(/§a/gi,'</span>§r<span class="c-11">');
    text = text.replace(/§b/gi,'</span>§r<span class="c-12">');
    text = text.replace(/§c/gi,'</span>§r<span class="c-13">');
    text = text.replace(/§d/gi,'</span>§r<span class="c-14">');
    text = text.replace(/§e/gi,'</span>§r<span class="c-15">');
    text = text.replace(/§f/gi,'</span>§r<span class="c-16">');
    //bold
    text = text.replace(/§l/gi,"<span style='font-weight:900;'>");
    //italic
    text = text.replace(/§o/gi,"<span style='font-style:italic;'>");
    //strikethrough
    text = text.replace(/§m/gi,"<span style='text-decoration:line-through'>");
    //underlined
    text = text.replace(/§n/gi,"<span style='text-decoration:underline'>");
    //obfuscated
    text = text.replace(/§k/gi,"<span class='obfuscated'>");
    //reset
    text = text.replace(/§r/gi, "</span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span>");
    return text
}

function htmlEncode(value){
    return $('<div/>').text(value).html();
  }

function randomizer(rawr) {
    var length = rawr.length;
    var text = '';
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < length; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

$.fn.selectRange = function(start, end){
    if(!end) end = start;
    return this.each(function(){
        if (this.setSelectionRange) {
            this.focus();
            this.setSelectionRange(start, end);
        } else if (this.createTextRange) {
            var range = this.createTextRange();
            range.collapse(true);
            range.moveEnd('character', end);
            range.moveStart('character', start);
            range.select();
        }
    });
};

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
    png = $(this).children().children('div[class="emote-img"]').children('img');
    gif = png.next();
    wait = $(this).children().children('div[class="emote-img"]').prev();

    //wait.attr('style', '');

    // hide png and show gif
    console.log(png.attr('style', 'display: none;'));
    console.log(gif.attr('style', ''));
    //wait.attr('style', '');

}

function hideGIF() {
    console.log("hide gif");
    png = $(this).children().children('div[class="emote-img"]').children('img');
    gif = png.next();
    wait = $(this).children().children('div[class="emote-img"]').prev();
    // hide gif and show png
    wait.attr('style', 'display: none;');
    console.log(png.attr('style', ''));
    console.log(gif.attr('style', 'display: none;'));


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
                //console.log(edata);
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

    console.log(title, colour(title))

    title_span = document.createElement('span');
    title_span.innerHTML = colour(title);

    //console.log(title_span);

    emote_author = document.createElement('div');
    emote_author.className = 'emote-author';

    author_span = document.createElement('span');
    author_span.innerHTML = colour(author);

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

    console.log(emote);
    emote = $(emote);
    emote.appendTo('div[class="emotes-grid"]')

    //$('div[class="emotes-grid"]').append(emote);
    //console.log(emote);

    //console.log('unbind');
    //$(".emote").unbind('mouseenter mouseleave');
    //console.log('bind');
    //$(".emote").hover(showGIF, hideGIF)

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
$(window).on('load', function(){
    // func for sidebar radio buttons
    $(".line-radio").click(clickRadio)

    // func for title in sidebar, for transform image
    $(".title-flipper").click(clickTitle)

    $('.emotes-grid').on('mouseenter', '.emote', showGIF);

    $('.emotes-grid').on('mouseleave', '.emote', hideGIF);

});

