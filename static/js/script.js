/**
 * Created with PyCharm.
 * User: 立翔
 * Date: 13-5-4
 * Time: 下午2:16
 * To change this template use File | Settings | File Templates.
 */


$(document).ready(function(){
    var isFrist = false;
    var times = 1;

    $(".btn-action-comment").click(function(){
        var obj = this;
        if (isFrist) {
                    times++;
            if($(obj).parent('.actions').next('.comments').css('display') =='none'){
                        $(obj).parent('.actions').next('.comments').css('display','inline-block');
                    }
                    else{
                        $(obj).parent('.actions').next('.comments').css('display','none');
                    }
        } else {
                    $.get($(this).attr("href"),function(data,status){
                    $(obj).parent('.actions').next('.comments').children('.comment-item').html(data);
                    });
                    $(obj).parent('.actions').next('.comments').css('display','inline-block');
                    isFrist = true;
                }
        return false
  });
    $("#id_status_content").keyup(function(){
        var txt = $(this).val();
        var btn = $('#status-btn');
        var count = $('#count');

        var n = 140;
        if(txt.length){
            if(txt.length<=140){
                btn.removeAttr('disabled');
                count.html("还可以输入"+(n-txt.length)+"字");
                console.log(count.html());
            }else{
                btn.attr('disabled','disabled');
                count.html("已经超过"+(txt.length-n)+"字");
            }
        }else{
            count.html("还可以输入140字");
            btn.attr('disabled','disabled')
        }
});


    $("#id_message_content").keyup(function(){
        var txt = $(this).val();
        var btn = $('#board-btn');

        if(txt.length){
                btn.removeAttr('disabled');
        }else{
            btn.attr('disabled','disabled')
        }
});



    $("#id_comment_content").keyup(function(){
        var txt = $(this).val();
        var btn = $('#comment-btn');

        if(txt.length){
                btn.removeAttr('disabled');
        }else{
            btn.attr('disabled','disabled')
        }
});


       $(".comment-form").submit(function(event) {
           var obj = $(this)

          /* stop form from submitting normally */
          event.preventDefault();

          /* get some values from elements on the page: */
          var $form = $( this ),
              input = $form.find('input[name="comment"]'),
              comment = input.val(),
              url = $form.attr( 'action' );

          /* Send the data using post */
          var posting = $.post( url, { comment: comment }, 'json');

          /* Put the results in a div */
          posting.done(function( data ) {
            var content = data['comment']+" - <a href='http://localhost/people/"+data['comment_author_url'] +"'>"+ data['comment_author_nickname']+"</a>";
            obj.prev('.comment-item').append( '<p>'+content+'</p>' );
            input.val('');
          });
           return false
        });



        $("input.comment-input").keyup(function(){
        var txt = $(this).val();
        var btn = $('button.comment-btn');

        var n = 140;
        if(txt.length){
            btn.removeAttr('disabled');
        }else{
            btn.attr('disabled','disabled')
        }

    })





});

    jQuery(function($){
        $('#jcrop-target').Jcrop({
            onChange: showPreview,
            onSelect: showPreview,
            aspectRatio: 1
        });

        function showPreview(coords){
            var rx = 100 / coords.w;
            var ry = 100 / coords.h;

            $('#preview').css({
                width: Math.round(rx * $('#jcrop-target').width()) +'px',
                height: Math.round(ry * $('#jcrop-target').height()) +'px',
                marginLeft: '-'+ Math.round(rx * coords.x) +'px',
                marginTop: '-'+ Math.round(rx * coords.y) +'px'
            });
        }
    });

$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
