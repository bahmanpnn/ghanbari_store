function addProductToBasket(productId){
    // var count=$('#productCount').val();
    var count = $(`#productCount_${productId}`).val();

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
                cancelButtonColor: "#dd8533",
                cancelButtonText:'باشه',
            });
        };

    })
}

function addModalProductToBasket(productId) {
    var quantityInputId = $(".add-to-basket-btn").data("quantity-id");
    var count = $("#" + quantityInputId).val();  
    
    if (!count || isNaN(count) || count <= 0) {
        Swal.fire({
            title: "خطا",
            text: "لطفاً تعداد معتبر وارد کنید",
            icon: "error",
            confirmButtonColor: "#d33",
            confirmButtonText: "باشه",
        });
        return;
    }

    $.get('/orders/add-product-to-basket-orders/?product_id=' + productId + '&count=' + count)
    .then(res => {
        if (res.status === 'not-authenticated') {
            Swal.fire({
                title: res.title,
                text: res.text,
                icon: res.icon,
                showConfirmButton: true,
                confirmButtonColor: "#3085d6",
                confirmButtonText: "صفحه ورود",
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/account/login/';
                }
            });
        } else {
            Swal.fire({
                title: res.title,
                text: res.text,
                icon: res.icon,
                showConfirmButton: false,
                showCancelButton: true,
                cancelButtonColor: "#dd8533",
                cancelButtonText: 'باشه',
            });
        }
    });
}


function orderDetail(detailId) {
    $.get('/orders/remove_basket_card_order_detail/?detail_id=' + detailId).then(res=> {
        if (res.status === "success") {
            // Update Mini-Basket
            $('#basket-card').empty().html(res.body);
            $('#basket-card-mobile').empty().html(res.mobile_body);
            
            // Update Full Basket Page (if visible)
            $('#order-detail-content').empty().html(res.mbody);
            // Wait for DOM update, then call updateTotal()
            setTimeout(updateTotal, 20);

            // Extract updated count from the new HTML
            let newBasketCount = $("#basket-card .fa-cart-shopping").attr("data-basket-count");

            if (newBasketCount !== undefined) {
                $(".fa-cart-shopping").attr("data-basket-count", newBasketCount);
                $(".fa-cart-shopping").css("--basket-count", `"${newBasketCount}"`);
            }
        }
    });
}


function removeOrderBasket(detailId) {
    $.get('/orders/remove_basket_card_order_detail/?detail_id=' + detailId).then(res=>{
        if (res.status === "success") {
            $('#basket-card').empty().html(res.body);
            $('#basket-card-mobile').empty().html(res.mobile_body);

            $('#order-detail-content').empty().html(res.mbody);
            //  Wait for DOM update, then call updateTotal()
            setTimeout(updateTotal, 20);
            
            // Extract updated count from the new HTML
            let newBasketCount = $("#basket-card .fa-cart-shopping").attr("data-basket-count");

            if (newBasketCount !== undefined) {
                $(".fa-cart-shopping").attr("data-basket-count", newBasketCount);
                $(".fa-cart-shopping").css("--basket-count", `"${newBasketCount}"`);
            }
        }
    });
}


function changeOrderDetailCount(detailId,state) {
    $.get('/orders/change_order_detail_count/?detail_id=' + detailId+'&state='+state).then(res=>{
        if (res.status === "success") {
            $('#order-detail-content').empty().html(res.body);
            $('#basket-card-mobile').empty().html(res.mobile_body);
            // Wait for DOM update, then call updateTotal()
            setTimeout(updateTotal, 20);
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

function addProductToFavoriteList(productId) {

    $.get('/products/add-to-user-favorite-list/?product_id=' + productId ,{
    }).then(res=>{
        if(res.status=='not-authenticated'){
            Swal.fire({
                title: res.title,
                text:res.text,
                icon: res.icon,
                showCancelButton: true,
                showConfirmButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                cancelButtonText:'نه',
                confirmButtonText:res.confirm_button_text,
              }).then((result) => {
                if (result.isConfirmed && res.status === 'not-authenticated') {
                    window.location.href= '/account/login/'
                }
              });
        }else{
            const heartIcon=document.getElementById('product_'+res.product_id)
            if(res.action =='removing'){
                heartIcon.classList.remove('favorite-heart');
            }else{
                heartIcon.classList.add('favorite-heart');
            }
            Swal.fire({
                title: res.title,
                text:res.text,
                icon: res.icon,
                showConfirmButton: true,
                confirmButtonColor:"#dd8533",
                confirmButtonText:res.confirm_button_text,
                showCancelButton: false,
                // cancelButtonColor: "#d33",
                // cancelButtonText:'باشه',
            });
        };

    })
}

function showLargeImage(imageSrc) {
    // Update the `src` of the main image
    $("#mainImage").attr('src', imageSrc);

    // Update the `background-image` style of the `.product-thumb` div
    $(".product-thumb.zoom").css('background-image', `url(${imageSrc})`);
}

// done
function removeUserFavoriteProduct(favoriteProductId) {
    $.get('/profile/remove_user_favorite_product/?favorite_product_id=' + favoriteProductId).then(res=> {
        if (res.status === "success") {
            // Update User Favorite List
            $('#user-favorite-list').html(res.body);
        }
    });
}

function changeUserFavoriteProductCount(favoriteProductId,state) {
    $.get('/profile/change_user_favorite_product_count/?favorite_product_id=' + favoriteProductId+'&state='+state).then(res=>{
        if (res.status === "success") {
            $('#user-favorite-list').html(res.body);
        }
    });
}

function SendProductReviewComment(productId) {
    var comment = $('#id_description').val();
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();  // Get CSRF token
    var product_rating=$('#rating').val()

    $.post('/products/add-product-comment/', {
        comment: comment,
        product_id: productId,
        product_rating:product_rating,
        csrfmiddlewaretoken: csrfToken  // Include CSRF token

    }).done(function(res) {
        if (res.status === 'not-authenticated') {
            Swal.fire({
                title: res.title,
                text:res.message,
                icon: res.icon,
                showConfirmButton: true,
                confirmButtonColor: "#3085d6",
                confirmButtonText:"صفحه ورود",
              }).then((result) => {
                if (result.isConfirmed && res.status === 'not-authenticated') {
                    window.location.href= '/account/login/'
                }
              });
        } else {
            if (res.status === 'success') {
                Swal.fire({
                    title: res.title,
                    text:res.message,
                    icon: res.icon,
                    showConfirmButton: false,
                    showCancelButton: true,
                    cancelButtonColor: "#dd8533",
                    cancelButtonText:'باشه',
                });
                $('#id_description').val('');  // Clear textarea
            } else{
                    Swal.fire({
                        title: res.title,
                        text:res.message,
                        icon: res.icon,
                        showConfirmButton: false,
                        showCancelButton: true,
                        cancelButtonColor: "#dd8533",
                        cancelButtonText:'باشه',
                    });
                };
        }
        
    }).fail(function(xhr) {
        console.error('AJAX Error:', xhr);
        alert('خطایی رخ داد!');
    });
}



