// $("#ID_textCreateBtn").on("click",function () {
//     // console.log($('#ID_textCreateInput').val());
//     // console.log($('#ID_textCreateInput').val().length);
//     if($('#ID_textCreateInput').val().length > 0){
//         $.ajax({
//                 url: "/tools/qrcode/",
//                 type: "POST",
//                 data: {
//                     what: "qrcode",
//                     createType:"text",
//                     text:$("#ID_textCreateInput").val(),
//                     'csrfmiddlewaretoken':$("[name='csrfmiddlewaretoken']").val()
//                 },
//                 success: function (data) {
//                     var obj =  $.parseJSON(data);
//                     if(obj['state'] == 'true' && obj['createType'] == 'text') {
//                         var myImgSrc = obj['path'];
//                             $('#ID_qrcodeShow').attr('src', myImgSrc);
//                     }
//                 }
//
//         })
//     }
// })

$("#ID_textCreateBtn").on("click",function () {
    // console.log($('#ID_textCreateInput').val());
    // console.log($('#ID_textCreateInput').val().length);
    // if (qrcode){qrcode.clear();}
    $('#ID_qrcodeShow').empty();
    var qrcode = new QRCode('ID_qrcodeShow', {
      text: $('#ID_textCreateInput').val(),
      width: $('#ID_qrcodeShow').width(),
      height: $('#ID_qrcodeShow').width(),
      colorDark : '#000000',
      colorLight : '#ffffff',
      correctLevel : QRCode.CorrectLevel.H
    });
    // qrcode.clear();

})

function cilckCreateType(index) {
    // if(index==1)


}