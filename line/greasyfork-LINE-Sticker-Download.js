// ==UserScript==
// @name                LINE Sticker Download
// @name:zh-CN          LINE Sticker Download
// @name:ja             LINE Sticker Download
// @include             https://store.line.me/stickershop/product/*
// @include             https://store.line.me/emojishop/product/*
// @include             https://store.line.me/themeshop/product/*
// @namespace           https://veltlion.github.io/line-sticker-download
// @icon                https://secure.gravatar.com/avatar/6b0d31e600391e6f15240323202f5482
// @version             1.7
// @description         Add download button for line sticker/emoji/theme store.
// @description:zh-cn   在 LINE STORE 的 Sticker/Emoji/Theme 页面添加下载按钮。
// @description:ja      LINE STORE にダウンロードボタンを追加する。
// @author              空
// @grant               GM_download
// ==/UserScript==

(function(){
    'use strict';

    var path, id, btn, btn2, btnstr, link2, filename, link, lang ;
    path = window.location.pathname;
    id = path.replace(/\/(emoji|sticker)shop\/product\/([a-f\d]+).*/, '$2');
    //var lang = navigator.language;
    lang = document.documentElement.lang;
    btnstr = 'Download';
    if (lang.indexOf('zh') > -1) btnstr = '下载';
    else if (lang.indexOf('ja') > -1) btnstr = 'ダウンロードする';
    if (path.indexOf('stickershop') > -1) {
        if ($('span').hasClass('MdIcoAni_b') || $('span').hasClass('MdIcoPlay_b') ||$('span').hasClass('MdIcoSound_b') ||
            $('span').hasClass('MdIcoFlashAni_b') || $('span').hasClass('MdIcoFlash_b')) {
                link = 'https://sdl-stickershop.line.naver.jp/stickershop/v1/product/' + id + '/iphone/stickerpack@2x.zip';
            } else {
                link = 'https://sdl-stickershop.line.naver.jp/stickershop/v1/product/' + id + '/iphone/stickers@2x.zip';
            }
            btn = '<li><button class="MdBtn01P01" id="download" style="background: #33b1ff" >'
                + btnstr
                + '</button></li>';
            $('.mdCMN38Item01Ul').find('li:eq(0)').remove();
            $('.mdCMN38Item01Ul').prepend(btn);
            btn = '<li class="mdCMN08Li" style="list-style-type: none">'
            + '<a class="MdBtn01 mdBtn01" id="download" style="background: #33b1ff">'
            + '<span class="mdBtn01Inner">'
            + '<span class="mdBtn01Txt">' + btnstr + '</span>'
            + '</span></a></li>';
    } else if (path.indexOf('emojishop') > -1) {
        link = "http://dl.stickershop.line.naver.jp/sticonshop/v1/" + id + "/sticon/iphone/package.zip?v=1";
        btn = '<li class="mdCMN08Li" style="list-style-type: none">'
            + '<a class="MdBtn01 mdBtn01" id="download" style="background: #33b1ff">'
            + '<span class="mdBtn01Inner">'
            + '<span class="mdBtn01Txt">' + btnstr + '</span>'
            + '</span></a></li>';
        $('.mdCMN08Ul').find('li:eq(0)').remove();
        $('.mdCMN08Ul').prepend(btn);
    } else {
        id = $("div.mdCMN08Img>img").attr("src").replace(/https\:\/\/shop.line-scdn.net\/themeshop\/v1\/products\/(.+)\/WEBSTORE\/.+/, '$1');
        link = 'https://shop.line-scdn.net/themeshop/v1/products/' + id + '/ANDROID/theme.zip';
        link2 = 'https://shop.line-scdn.net/themeshop/v1/products/' + id + '/IOS/theme.zip';
        btn = '<li class="mdCMN08Li" style="list-style-type: none">'
        + '<a class="MdBtn01 mdBtn02" id="download" style="background: #00b84f">'
        + '<span class="mdBtn01Inner">'
        + '<span class="mdBtn01Txt">' + btnstr + ' (Android)</span>'
        + '</span></a></li>';
        btn2 = '<li class="mdCMN08Li" style="list-style-type: none">'
        + '<a class="MdBtn01 mdBtn01" id="download2" style="background: #33b1ff">'
        + '<span class="mdBtn01Inner">'
        + '<span class="mdBtn01Txt">' + btnstr + ' (iOS)</span>'
        + '</span></a></li>';
        $('.mdCMN08Ul').find('li:eq(0)').remove();
        $('.mdCMN08Ul').find('li:eq(0)').remove();
        $('.mdCMN08Ul').prepend(btn2);
        $('.mdCMN08Ul').prepend(btn);
    }

    if ($('div').hasClass('mdMN05Btn')) {
        //$('.MdBtn01').remove();
        $('.mdMN05Btn').prepend(btn2);
        $('.mdMN05Btn').prepend(btn);
    }

    
    filename = document.title.replace(/(.+) (-|–) .+/g, '$1');
    filename = filename.replace(/\"|\\|\/|\:|\*|\?|\<|\>|\|/g, "");
    var file = { url: link, name: filename + '.zip' };
    var file2 = { url: link2, name: filename + ' (iOS).zip' };

    $('body').on('click', '#download2', function(){ var result = GM_download(file2); });
    $('body').on('click', '#download', function(){ var result = GM_download(file); });

}());

