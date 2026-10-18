$(function () {
    // 服务端已渲染好当前层级内容（含真实 <a href> 链接），这里只做「渐进增强」：
    // 1) 点击下钻/返回/首页链接时走 AJAX 局部刷新 + pushState，避免整页刷新，体验更顺滑；
    // 2) 没有 JS 或被搜索引擎抓取时，真实链接也能正常跳转并被收录。

    // 统一用 AJAX 拉取目标页的主体内容（?partial=1 仅返回 #main 内的 HTML）
    function fetchMain(url) {
        var sep = url.indexOf('?') > -1 ? '&' : '?';
        $.get(url + sep + 'partial=1', function (html) {
            $('#main').html(html);
            window.history.pushState({ url: url }, '', url);
            window.scrollTo(0, 0);
        });
    }

    // 拦截所有站内导航链接（下钻、面包屑、返回、首页）
    $(document).on('click', 'a.drill-link', function (e) {
        e.preventDefault();
        fetchMain(this.href);
    });

    // 浏览器前进/后退：重新拉取对应层级的主体内容
    window.addEventListener('popstate', function () {
        var url = window.location.pathname + window.location.search;
        var sep = url.indexOf('?') > -1 ? '&' : '?';
        $.get(url + sep + 'partial=1', function (html) {
            $('#main').html(html);
        });
    });

    // 切换语言：保留当前省/市/区县/乡镇路径，只替换 lang 参数（整页刷新以重新服务端渲染）
    $('#language-select').on('change', function () {
        var params = new URLSearchParams(window.location.search);
        params.set('lang', this.value);
        params.delete('partial');
        window.location.search = params.toString();
    });
});
