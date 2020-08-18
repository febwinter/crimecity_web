$('.tab_menu_btn').on('click', function () {
    //버튼 색 제거,추가
    $('.tab_menu_btn').removeClass('on');
    $(this).addClass('on')

    //컨텐츠 제거 후 인덱스에 맞는 컨텐츠 노출
    var idx = $('.tab_menu_btn').index(this);

    $('.tab_box').hide();
    $('.tab_box').eq(idx).show();
});