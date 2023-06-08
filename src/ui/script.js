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

    setTimeout(() => {
        // func for sidebar radio buttons
        $(".line-radio").click(clickRadio)

        // func for title in sidebar, for transform image
        $(".title-flipper").click(clickTitle)
        console.log("done");
    }, 1000)


})

