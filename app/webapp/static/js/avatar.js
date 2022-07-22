// 用于异步加载用户头像
function user_avatar(t_url, uid){
    $.ajax({
        url:t_url,
        type:"POST",
        data:"id=" + uid,
        dataType: 'json',
        success:function(obj){
            $("#avatar_user").attr("src", obj.data);
        },
        error:function(e){
            alert("internal error happened when retrieving user avatar");
        }
    });
}

// 用于异步上传用户头像
function uploadProfile(){
    var formFile = new FormData($('#uploadForm')[0]);
    $.ajax({
        url:"/user/upload_avatar",
        type:"POST",
        data:formFile,
        processData:false,
        contentType:false,
        success:function(obj){
            window.location.reload();
        },
        error:function(e){
            alert("请选择有效的图片");
        }
    });
}

// 用于异步批量获取用户头像数据
function user_avatar_batch(t_url){
    var avatar_hash = new Array();
    var key = 0;
    $(".avatar_user").each(function () {
        avatar_hash[key] = $(this).attr("name");
        key += 1
    })
    avatar_hash = avatar_hash.join(";");
    // alert(avatar_hash);
    $.ajax({
        url:t_url,
        type:"POST",
        data:"avatar_hash_list=" + avatar_hash,
        dataType: 'json',
        success:function(obj){
            var key = 0;
            $(".avatar_user").each(function () {
                $(this).attr("src", obj.data[key]);
                key += 1;
            })
            // console.log(obj.data)
            // $("#avatar_user").attr("src", obj.data);
        },
        error:function(e){
            alert("server internal error happened when retrieving user avatar");
        }
    });
}

// 用于异步批量获取评论的用户头像数据
function user_avatar_comment_batch(t_url){
    var avatar_hash = new Array();
    var key = 0;
    $(".avatar_user_comment").each(function () {
        avatar_hash[key] = $(this).attr("name");
        key += 1
    })
    avatar_hash = avatar_hash.join(";");
    // alert(avatar_hash);
    $.ajax({
        url:t_url,
        type:"POST",
        data:"avatar_hash_list=" + avatar_hash,
        dataType: 'json',
        success:function(obj){
            var key = 0;
            $(".avatar_user_comment").each(function () {
                $(this).attr("src", obj.data[key]);
                key += 1;
            })
            // console.log(obj.data)
            // $("#avatar_user").attr("src", obj.data);
        },
        error:function(e){
            alert("server internal error happened when retrieving user avatar");
        }
    });
}

