// Done
function addProductToBasket(productId){
    var count=$('#productCount').val();

    $.get('/orders/add-product-to-basket-orders/?product_id=' + productId + '&count='+ count,{
        // count:count,
        // product_id:productId
    }).then(res=>{
        if(res.status=='not-authenticated'){
            Swal.fire({
                title: res.title,
                text:res.text,
                icon: res.icon,
                showConfirmButton: true,
                confirmButtonColor: "#3085d6",
                confirmButtonText:"صفحه ورود",
              }).then((result) => {
                if (result.isConfirmed && res.status === 'not-authenticated') {
                    window.location.href= '/account/login/'
                }
              });
        }else{
            Swal.fire({
                title: res.title,
                text:res.text,
                icon: res.icon,
                showConfirmButton: false,
                showCancelButton: true,
                cancelButtonColor: "#d33",
                cancelButtonText:'باشه',
            });
        };

    })
}

// Done 
function orderDetail(detailId) {
    $.get('/orders/remove_order_detail/?detail_id=' + detailId).then(res=>{
        if (res.status === "success") {
            $('#order-detail-content').html(res.body);
        }
    });
}

function removeOrderBasket(detailId) {
    console.log(detailId);
    $.get('/orders/remove_basket_card_order_detail/?detail_id=' + detailId).then(res=>{
        if (res.status === "success") {
            $('#basket-card').html(res.body);
        }
    });
}

// Done
function changeOrderDetailCount(detailId,state) {
    $.get('/orders/change_order_detail_count/?detail_id=' + detailId+'&state='+state).then(res=>{
        if (res.status === "success") {
            $('#order-detail-content').html(res.body);
        }
    });
}

function SendArticleComment(ArticleId){

    var comment=$('#text').val();
    var parentId=$('#parentId').val();

    $.get('/blog/add-comment/article_comment/',{
        comment:comment,
        article_id:ArticleId,
        parent_id:parentId
        
    }).then(res=>{
        $('#comments_area').html(res)
        $('#text').val('');
        $('#parentId').val('');
        
        //after adding comment must scroll to that 
        if(parentId !== null && parentId !== ''){
            document.getElementById('single_comment_'+parentId).scrollIntoView({behavior:'smooth'})
        }else{
            document.getElementById('comments_area').scrollIntoView({behavior:'smooth'})
        }
    })
}


function fillParentId(parentId) {
    $('#parentId').val(parentId);
    document.getElementById('comment_form').scrollIntoView({behavior:'smooth'})
}

// function addProductToFavoriteList(productId) {

//     $.get('/products/add-to-user-favorite-list/?product_id=' + productId ,{
//     }).then(res=>{
//         if(res.status=='not-authenticated'){
//             Swal.fire({
//                 title: res.title,
//                 text:res.text,
//                 icon: res.icon,
//                 showCancelButton: true,
//                 showConfirmButton: true,
//                 confirmButtonColor: "#3085d6",
//                 cancelButtonColor: "#d33",
//                 cancelButtonText:'OK',
//                 confirmButtonText:res.confirm_button_text,
//               }).then((result) => {
//                 if (result.isConfirmed && res.status === 'not-authenticated') {
//                     window.location.href= '/accounts/login/'
//                 }
//               });
//         }else{
//             Swal.fire({
//                 title: res.title,
//                 text:res.text,
//                 icon: res.icon,
//                 showConfirmButton: false,
//                 showCancelButton: true,
//                 cancelButtonColor: "#d33",
//                 cancelButtonText:'OK',
//             });
//         };

//     })
// }
