$(function () {
    // 服务端已在 index.py 完成当前层级内容（含经纬度、日出日落、是否夜晚、天气预报）的服务端渲染，
    // 这里只做「渐进增强」：
    // 1) 点击下钻/返回/首页/面包屑链接时走 AJAX 局部刷新 + pushState，避免整页刷新，体验更顺滑；
    // 2) 没有 JS 或被搜索引擎抓取时，真实 <a href> 链接也能正常跳转并被收录；
    // 3) 天气预报已随页面服务端渲染，无需前端异步拉取。

    // 统一用 AJAX 拉取目标页的主体内容（?partial=1 仅返回 #main 内的 HTML，含 SSR 天气）
    function fetchMain(url, push) {
        var sep = url.indexOf('?') > -1 ? '&' : '?';
        $.get(url + sep + 'partial=1', function (html) {
            $('#main').html(html);
            if (push) {
                window.history.pushState({ url: url }, '', url);
            }
            window.scrollTo(0, 0);
        });
    }

    // 拦截所有站内导航链接（下钻、面包屑、返回、首页）
    $(document).on('click', 'a.drill-link', function (e) {
        e.preventDefault();
        fetchMain(this.href, true);
    });

    // 浏览器前进/后退：重新拉取对应层级的主体内容（含 SSR 天气）
    window.addEventListener('popstate', function () {
        var url = window.location.pathname + window.location.search;
        fetchMain(url, false);
    });

    // 切换语言：保留当前省/市/区县/乡镇路径，只替换 lang 参数（整页刷新以重新服务端渲染）
    $('#language-select').on('change', function () {
        var params = new URLSearchParams(window.location.search);
        params.set('lang', this.value);
        params.delete('partial');
        window.location.search = params.toString();
    });
});
