        const translations = {
            "zh-CN": {
                title: "跑途网 - 经纬网，日出、日落查询",
                header: "在线经纬度查询工具",
                currentLocation: "当前位置：查询工具 > 经纬度查询",
                provinceHeader: "省市级:",
                cityHeader: "城市:",
                areaHeader: "区域:",
                coordinatesHeader: "定位坐标:",
                sunHeader: "日出、日落:",
                isnightHeader: "是否夜晚:",
                backButton: "返回上一页",
                homeButton: "返回首页",
                footerText: "Copyright © 2021-2024 跑途网. All Rights Reserved."
            },
            "zh-TW": {
                title: "跑途網 - 經緯網，日出、日落查詢",
                header: "在線經緯度查詢工具",
                currentLocation: "當前位置：查詢工具 > 經緯度查詢",
                provinceHeader: "省市級:",
                cityHeader: "城市:",
                areaHeader: "區域:",
                coordinatesHeader: "定位坐標:",
                sunHeader: "日出、日落:",
                isnightHeader: "是否夜晚:",
                backButton: "返回上一頁",
                homeButton: "返回首頁",
                footerText: "Copyright © 2021-2024 跑途網. All Rights Reserved."
            },
            "en": {
                title: "Paotu Net - Coordinate Query Tool, Sunrise and Sunset",
                header: "Online Coordinate Query Tool",
                currentLocation: "Current Location: Query Tool > Coordinate Query",
                provinceHeader: "Provinces:",
                cityHeader: "Cities:",
                areaHeader: "Areas:",
                coordinatesHeader: "Location Coordinates:",
                sunHeader: "Sunrise and Sunset:",
                isnightHeader: "Is it Night:",
                backButton: "Go Back",
                homeButton: "Home",
                footerText: "Copyright © 2021-2024 Paotu Net. All Rights Reserved."
            },
            "ja": {
                title: "パオツネット - 緯度経度、日の出、日の入りの問い合わせ",
                header: "オンライン緯度経度問い合わせツール",
                currentLocation: "現在の位置：問い合わせツール > 緯度経度問い合わせ",
                provinceHeader: "省・市:",
                cityHeader: "都市:",
                areaHeader: "地域:",
                coordinatesHeader: "位置座標:",
                sunHeader: "日の出、日の入り:",
                isnightHeader: "夜ですか？:",
                backButton: "前のページに戻る",
                homeButton: "ホーム",
                footerText: "Copyright © 2021-2024 パオツネット. All Rights Reserved."
            },
            "de": {
                title: "Paotu-Netz - Koordinatenabfrage, Sonnenaufgang und -untergang",
                header: "Online-Koordinatenabfrage-Tool",
                currentLocation: "Aktueller Standort: Abfragewerkzeug > Koordinatenabfrage",
                provinceHeader: "Provinzen:",
                cityHeader: "Städte:",
                areaHeader: "Bereiche:",
                coordinatesHeader: "Standortkoordinaten:",
                sunHeader: "Sonnenaufgang und -untergang:",
                isnightHeader: "Ist es Nacht:",
                backButton: "Zurück",
                homeButton: "Startseite",
                footerText: "Copyright © 2021-2024 Paotu-Netz. Alle Rechte vorbehalten."
            },
            "ru": {
                title: "Пауто Сеть - Запрос координат, восход и заход солнца",
                header: "Онлайн инструмент запроса координат",
                currentLocation: "Текущее местоположение: Инструмент запроса > Запрос координат",
                provinceHeader: "Провинции:",
                cityHeader: "Города:",
                areaHeader: "Районы:",
                coordinatesHeader: "Координаты местоположения:",
                sunHeader: "Восход и заход солнца:",
                isnightHeader: "Ночь ли сейчас:",
                backButton: "Назад",
                homeButton: "На главную",
                footerText: "Copyright © 2021-2024 Пауто Сеть. Все права защищены."
            },
            "fr": {
                title: "Paotu Net - Outil de recherche de coordonnées, lever et coucher de soleil",
                header: "Outil de recherche de coordonnées en ligne",
                currentLocation: "Emplacement actuel : Outil de recherche > Recherche de coordonnées",
                provinceHeader: "Provinces :",
                cityHeader: "Villes :",
                areaHeader: "Zones :",
                coordinatesHeader: "Coordonnées géographiques :",
                sunHeader: "Lever et coucher du soleil :",
                isnightHeader: "Est-ce la nuit :",
                backButton: "Retour",
                homeButton: "Accueil",
                footerText: "Copyright © 2021-2024 Paotu Net. Tous droits réservés."
            },
            "es": {
                title: "Paotu Net - Herramienta de consulta de coordenadas, amanecer y atardecer",
                header: "Herramienta de consulta de coordenadas en línea",
                currentLocation: "Ubicación actual: Herramienta de consulta > Consulta de coordenadas",
                provinceHeader: "Provincias:",
                cityHeader: "Ciudades:",
                areaHeader: "Áreas:",
                coordinatesHeader: "Coordenadas de ubicación:",
                sunHeader: "Amanecer y atardecer:",
                isnightHeader: "¿Es de noche?",
                backButton: "Volver",
                homeButton: "Inicio",
                footerText: "Copyright © 2021-2024 Paotu Net. Todos los derechos reservados."
            }
        };

        function changeLanguage(language) {
            const lang = translations[language];
            if (lang) {
                document.getElementById("page-title").innerText = lang.title;
                document.getElementById("header-title").innerText = lang.header;
                document.getElementById("current-location").innerText = lang.currentLocation;
                document.getElementById("province-header").innerText = lang.provinceHeader;
                document.getElementById("city-header").innerText = lang.cityHeader;
                document.getElementById("area-header").innerText = lang.areaHeader;
                document.getElementById("coordinates-header").innerText = lang.coordinatesHeader;
                document.getElementById("sun-header").innerText = lang.sunHeader;
                document.getElementById("isnight-header").innerText = lang.isnightHeader;
                document.getElementById("back-button").innerText = lang.backButton;
                document.getElementById("home-button").innerText = lang.homeButton;
                document.getElementById("footer-text").innerText = lang.footerText;
            }
        }

        $(document).ready(function() {
            // 检测浏览器语言并设置默认语言
            const userLang = navigator.language || navigator.userLanguage;
            const defaultLang = userLang.startsWith('zh') ? 'zh-CN' : 
                               userLang.startsWith('en') ? 'en' : 
                               userLang.startsWith('ja') ? 'ja' : 
                               userLang.startsWith('de') ? 'de' : 
                               userLang.startsWith('ru') ? 'ru' : 
                               userLang.startsWith('fr') ? 'fr' : 
                               userLang.startsWith('es') ? 'es' : 'en';

            $('#language-select').val(defaultLang);
            changeLanguage(defaultLang);

            $('#language-select').change(function() {
                changeLanguage(this.value);
            });

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