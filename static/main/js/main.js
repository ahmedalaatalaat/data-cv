AOS.init({
    duration: 800,
    easing: "slide",
    once: false,
});

jQuery(document).ready(function ($) {
    "use strict";

    $(".loader").delay(1000).fadeOut("slow");
    $("#overlayer").delay(1000).fadeOut("slow");

    $(".select2-with-label-single").select2({
        placeholder: "Choose...",
        allowClear: true,
    });

    $(".select2-with-label-multiple").select2();

    var siteMenuClone = function () {
        $(".js-clone-nav").each(function () {
            var $this = $(this);
            $this
                .clone()
                .attr("class", "site-nav-wrap")
                .appendTo(".site-mobile-menu-body");
        });

        setTimeout(function () {
            var counter = 0;
            $(".site-mobile-menu .has-children").each(function () {
                var $this = $(this);

                $this.prepend('<span class="arrow-collapse collapsed">');

                $this.find(".arrow-collapse").attr({
                    "data-toggle": "collapse",
                    "data-target": "#collapseItem" + counter,
                });

                $this.find("> ul").attr({
                    class: "collapse",
                    id: "collapseItem" + counter,
                });

                counter++;
            });
        }, 1000);

        $("body").on("click", ".arrow-collapse", function (e) {
            var $this = $(this);
            if ($this.closest("li").find(".collapse").hasClass("show")) {
                $this.removeClass("active");
            } else {
                $this.addClass("active");
            }
            e.preventDefault();
        });

        $(window).resize(function () {
            var $this = $(this),
                w = $this.width();

            if (w > 768) {
                if ($("body").hasClass("offcanvas-menu")) {
                    $("body").removeClass("offcanvas-menu");
                }
            }
        });

        $("body").on("click", ".js-menu-toggle", function (e) {
            var $this = $(this);
            e.preventDefault();

            if ($("body").hasClass("offcanvas-menu")) {
                $("body").removeClass("offcanvas-menu");
                $this.removeClass("active");
            } else {
                $("body").addClass("offcanvas-menu");
                $this.addClass("active");
            }
        });

        // click outisde offcanvas
        $(document).mouseup(function (e) {
            var container = $(".site-mobile-menu");
            if (!container.is(e.target) && container.has(e.target).length === 0) {
                if ($("body").hasClass("offcanvas-menu")) {
                    $("body").removeClass("offcanvas-menu");
                }
            }
        });
    };
    siteMenuClone();

    var sitePlusMinus = function () {
        $(".js-btn-minus").on("click", function (e) {
            e.preventDefault();
            if ($(this).closest(".input-group").find(".form-control").val() != 0) {
                $(this)
                    .closest(".input-group")
                    .find(".form-control")
                    .val(
                        parseInt(
                            $(this).closest(".input-group").find(".form-control").val()
                        ) - 1
                    );
            } else {
                $(this).closest(".input-group").find(".form-control").val(parseInt(0));
            }
        });
        $(".js-btn-plus").on("click", function (e) {
            e.preventDefault();
            $(this)
                .closest(".input-group")
                .find(".form-control")
                .val(
                    parseInt(
                        $(this).closest(".input-group").find(".form-control").val()
                    ) + 1
                );
        });
    };
    // sitePlusMinus();

    var siteSliderRange = function () {
        $("#slider-range").slider({
            range: true,
            min: 0,
            max: 500,
            values: [75, 300],
            slide: function (event, ui) {
                $("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
            },
        });
        $("#amount").val(
            "$" +
            $("#slider-range").slider("values", 0) +
            " - $" +
            $("#slider-range").slider("values", 1)
        );
    };
    // siteSliderRange();

    var siteStellar = function () {
        $(window).stellar({
            responsive: false,
            parallaxBackgrounds: true,
            parallaxElements: true,
            horizontalScrolling: false,
            hideDistantElements: false,
            scrollProperty: "scroll",
        });
    };
    // siteStellar();

    // navigation
    var OnePageNavigation = function () {
        var navToggler = $(".site-menu-toggle");
        $("body").on(
            "click",
            ".main-menu li a[href^='#'], .smoothscroll[href^='#'], .site-mobile-menu .site-nav-wrap li a",
            function (e) {
                e.preventDefault();

                var hash = this.hash;

                $("html, body").animate(
                    {
                        scrollTop: $(hash).offset().top - 0,
                    },
                    1000,
                    "easeInOutCirc",
                    function () {
                        window.location.hash = hash;
                    }
                );
            }
        );
    };
    OnePageNavigation();

    var siteScroll = function () {
        $(window).scroll(function () {
            var st = $(this).scrollTop();

            if (st > 100) {
                $(".js-sticky-header").addClass("shrink");
            } else {
                $(".js-sticky-header").removeClass("shrink");
            }
        });
    };
    siteScroll();
});

function get_random_project() {
    $.ajax({
        method: "GET",
        url: window.location.href,
        data: {
            type: "get_random_project",
        },
        success: function (data) {
            window.open(window.location.origin + data.url, '_blank');
        },
        error: function (error_data) { },
    });
}


