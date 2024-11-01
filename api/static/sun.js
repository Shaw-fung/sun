        $(document).ready(function() {
            // 其余原始代码保持不变
            let currentLocation = ['经纬度查询'];

            function updateLocation() {
                $('.location').text('当前位置：查询工具 > ' + currentLocation.join(' > '));
            }

            $('.province-link').click(function(){
                var province = $(this).data('province');
                currentLocation[1] = province; // 更新城市位置
                $('#cities-list').empty();
                $('#areas-list').empty();
                $('#coordinates-list').empty();
                updateLocation(); // 更新位置显示

                $.get('/location', {province: province}, function(data){
                    data.forEach(function(city){
                        $('#cities-list').append('<a href="#" class="link-button city-link" data-province="' + province + '" data-city="' + city + '">' + city + '</a>');
                    });
                    document.getElementById("provinces").style.display = "none";
                    document.getElementById("cities").style.display = "block";
                });
            });

            $(document).on('click', '.city-link', function(){
                var province = $(this).data('province');
                var city = $(this).data('city');
                currentLocation[2] = city; // 更新省市位置
                $('#areas-list').empty();
                $('#coordinates-list').empty();
                updateLocation(); // 更新位置显示

                $.get('/location', {province: province, city: city}, function(data){
                    data.forEach(function(area){
                        $('#areas-list').append('<a href="#" class="link-button area-link" data-province="' + province + '" data-city="' + city + '" data-area="' + area + '">' + area + '</a>');
                    });
                    document.getElementById("cities").style.display = "none";
                    document.getElementById("areas").style.display = "block";
                });
            });

            $(document).on('click', '.area-link', function(){
                var province = $(this).data('province');
                var city = $(this).data('city');
                var area = $(this).data('area');
                currentLocation[3] = area; // 更新区域位置
                $('#coordinates-list').empty();
                $('#sun-times-row td').empty(); // 清空之前的日出日落时间
                updateLocation(); // 更新位置显示

                $.get('/location', {province: province, city: city, area: area}, function(data){
                    data.forEach(function(coordinate){
                        $('#coordinates-list').append('<div class="coordinate-item">' + coordinate.area + ': ' + coordinate.lat + ', ' + coordinate.lng + '</div>');
                        $('#sun-list').append('<div class="sun-info"><a href="/sun?latitude=' + coordinate.lat + '&longitude=' + coordinate.lng + '&date=today&timezone=asia/shanghai">查看' + coordinate.area + '日出、日落时间</a></div>');
                        $('#isnight-list').append('<div class="isnight-info"><a href="/isnight?latitude=' + coordinate.lat + '&longitude=' + coordinate.lng + '&date=today&timezone=asia/shanghai">查看' + coordinate.area + '现在是否夜晚</a></div>');

                        // 请求日出日落时间
                        $.get('/sun', {
                            latitude: coordinate.lat,
                            longitude: coordinate.lng,
                            date: 'today',
                            timezone: 'asia/shanghai'
                        }, function(sunData) {
                            // 填充表格
                            $('#sun-times-row td:nth-child(1)').text(sunData.日期);
                            $('#sun-times-row td:nth-child(2)').text(sunData.天亮);
                            $('#sun-times-row td:nth-child(3)').text(sunData.日出);
                            $('#sun-times-row td:nth-child(4)').text(sunData.正午);
                            $('#sun-times-row td:nth-child(5)').text(sunData.日落);
                            $('#sun-times-row td:nth-child(6)').text(sunData.天黑);
                        });
                    });
                    document.getElementById("areas").style.display = "none";
                    document.getElementById("coordinates").style.display = "block";
                });
            });
        });