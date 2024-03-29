#Static Folder Name
folder_name = "financial"

dz_array = {
        "public":{
            "description":"financialSystem",
            "og_title":"financialSystem",
            "og_description":"financialSystem financialSystem",
            "og_image":"/social-image.png",
            "title":"financial platform",
        },
        "global":{
            "css":[
                    f"{folder_name}/vendor/bootstrap-select/dist/css/bootstrap-select.min.css",
					f"{folder_name}/css/style.css",
                ],

            "js":{
                "top":[
                    f"{folder_name}/vendor/global/global.min.js",
					f"{folder_name}/vendor/bootstrap-select/dist/js/bootstrap-select.min.js",
                ],
                "bottom":[
                    f"{folder_name}/js/dlabnav-init.js",
                    f"{folder_name}/js/custom.js",
                ]
            },

        },
        "pagelevel":{
            "financial":{#AppName
                "financial_views":{
                    "css":{
                        "user_watchlist_view": [
                            f"{folder_name}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                        ],
                        "stock_detail_view":[
                            f"{folder_name}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                        ],
                        "news_view":[
                            f"{folder_name}/vendor/swiper/css/swiper-bundle.min.css",
                        ],
                        "stock_list_view":[
                            f"{folder_name}/vendor/swiper/css/swiper-bundle.min.css",
                        ],
                        "page_empty": [
                        ],
                    },
                    "js":{
                        "user_watchlist_view": [
                            f"{folder_name}/vendor/echarts/echarts.js",
                        ],
                        "stock_detail_view":[
                            f"{folder_name}/vendor/echarts/echarts.js",
                        ],
                        "news_view": [
                            f"{folder_name}/vendor/swiper/js/swiper-bundle.min.js",
                        ],
                        "stock_list_view": [
                            f"{folder_name}/vendor/swiper/js/swiper-bundle.min.js",
                        ],
                    },
                }
            }
        }


}