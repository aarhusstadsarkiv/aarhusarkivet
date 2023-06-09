// var notify = function(resp) {
//     var notelist = document.getElementById("notificationlist");
//     var notification = document.createElement('li');
//     notification.classList.add('callout');
//     notification.innerHTML = '<p>' + resp.msg + '</p>';
//     if (resp.error) {
//         notification.classList.add('alert');
//     } else {
//         notification.classList.add('success');
//     }
//     notelist.appendChild(notification);
// };

function notify(resp) {
    //append the new notifications DOM in Page
    var cls = 'success';
    if (resp.error) {
        cls = 'alert';
    }
    // var id = resp.id + '-' + resp.method;
    // cls = 'alert' ? resp.error : 'success';
    var notice = '<li class="callout ' + cls + '"><p>' + resp.msg + '</p></li>';
    $(notice).prependTo( $('#notificationlist') ).fadeOut(3500);
}

// const scrollIntoViewWithOffset = (el, offset) => {
//     window.scrollTo({
//         top:
//             document.querySelector(selector).getBoundingClientRect().top - document.body.getBoundingClientRect().top - offset,
//             // el.getBoundingClientRect().top - document.body.getBoundingClientRect().top - offset,
//     })
// }
  
// window.addEventListener('load', function () {
//     if (window.location.hash == '') {
//         return false;
//     }
//     console.log(window.location.hash);
//     console.log(window.location.hash.slice(1))
//     // var el = document.querySelector("[data-id='" + window.location.hash.slice(1) + "']");
//     // var el = document.querySelector(window.location.hash);
//     scrollIntoViewWithOffset("[data-id='" + window.location.hash.slice(1) + "']", 300);
//     // if (el !== null) {
//     //     console.log("element is found");
//     //     var topint = el.getBoundingClientRect().top - document.body.getBoundingClientRect().top - 60
//     //     console.log("top is: " + topint);
//     //     window.scrollTo({top: topint});
//     //     // el.scrollIntoView({ behavior: 'smooth' });
//     // } else {
//     //     console.log()
//     // }
// }, false);

// Catchall-doc for small or global stuff
$(document).ready(function() {

    // if (window.location.hash) {
    //     scroll(0, 0);
    //     // setTimeout(scroll(0, 0), 1); // void some browsers issue
    //     var anchorLink = $(window.location.hash);
    //     // var offsetSize = $("#navigation").innerHeight() + 5;
    //     $(anchorLink).scrollTop( 100 );
    //     // $("html, body").delay(400).animate({scrollTop: anchorLink.offset().top - 180}, 700);
    //     anchorLink.focus();
    // }

    $('.global-search-field').on( "keyup", function(e) {
        if ($(this).val().length > 1) {
            $('.global-search-button').addClass('activated');
        } else {
            $('.global-search-button').removeClass('activated');
        }
    });

    $('#single-video').lightGallery({"counter": false});
    $('#single-image').lightGallery({"download": false, "counter": false});
    $('#gallery-results__').lightGallery({
        // "loop": false,
        "selector": ".gallery-img",
        "getCaptionFromTitleOrAlt": false,
        "appendSubHtmlTo": ".lg-sub-html",
        "addClass": "gallery-box",
        "subHtmlSelectorRelative": true,
        // "download": false
    });

    // if ( !$('#ordering') ) {
    //     $('#ordering-link').hide();
    // }

    // TODO: Tidy Up! Very hacky
    var agendaText = $('#agendaItems').text();
    if (agendaText) {
        $('#agendaItems').replaceWith(function() {
            var agendaJSON = jQuery.parseJSON(agendaText);
            var output = "";
            $.each(agendaJSON, function(i, value) {
                var fn = value.href.substring(value.href.lastIndexOf('/') + 1);
                var label = fn.slice(0,4) + '-' + fn.slice(4,6) + '-' + fn.slice(6,8);
                output += "<li><a href=\"" + value.href + '#page=' + value.start_page + "\">" + label + "</a></li>";
            });
            return "<h5 style='font-size:105%;'>Sagen behandles på følgende byrådsmøder</h5><ul style='list-style-type:none;margin-left:0;'>" + output + "</ul>";
        });
        $('#agendaItems-container').toggleClass('hide');
    }

    // Toogle top-link
    $(window).scroll(function(){
        if($(window).scrollTop() >= 400){ // Value of scrollTop is in pixels - maybe
            $(".top-link").fadeIn(1000);
        }else{
            $(".top-link").fadeOut(800);
        }
    });

    // Both elements are selected due to browser differences
    // Opera has problems with this double selecting, as it tries to scroll both elements at once
    $('.top-link').click(function(){
        $('html, body').animate({scrollTop:0}, 400);
        return false;
    });

    // var populateNotifications = function(resp) {
    //     //append the new notifications DOM in Page
    //     cls = '';
    //     if (resp.error) {
    //         cls = 'warning';
    //     }
    //     $('#notifications ul').append('<li class="callout ' + cls + '"><p>' + resp.msg + '</p></li>');
    // };
});
