import $ from "jquery";
window.$ = window.jQuery = $;
const mixitup = require("mixitup");

!(function (e) {
  "use strict";
  function o() {
    e(".newsletter-form").addClass("animated shake"),
      setTimeout(function () {
        e(".newsletter-form").removeClass("animated shake");
      }, 1e3);
  }
  function s(o, s) {
    if (o) var a = "validation-success";
    else a = "validation-danger";
    e("#validator-newsletter").removeClass().addClass(a).text(s);
  }
  jQuery(".mean-menu").meanmenu({ meanScreenWidth: "991" }),
    e(window).on("scroll", function () {
      e(this).scrollTop() > 120
        ? e(".sinmun-nav").addClass("is-sticky")
        : e(".sinmun-nav").removeClass("is-sticky");
    }),
    e(".popup-youtube").magnificPopup({
      disableOn: 320,
      type: "iframe",
      mainClass: "mfp-fade",
      removalDelay: 160,
      preloader: false,
      fixedContentPos: false,
    }),
    e(".breaking-news-slides").owlCarousel({
      loop: true,
      nav: false,
      dots: false,
      autoplayHoverPause: true,
      autoplay: true,
      animateIn: "flipInX",
      items: 1,
    }),
    e(".nav-search-button").on("click", function () {
      e(".nav-search form").toggleClass("active");
    }),
    e(".nav-search-close-button").on("click", function () {
      e(".nav-search form").removeClass("active");
    }),
    e(".popular-news-slides").owlCarousel({
      loop: true,
      nav: true,
      dots: false,
      autoplayHoverPause: true,
      autoplay: true,
      margin: 30,
      navText: [
        "<i class='icofont-rounded-left'></i>",
        "<i class='icofont-rounded-right'></i>",
      ],
      responsive: { 0: { items: 1 }, 768: { items: 2 }, 1200: { items: 3 } },
    }),
    e(".health-lifestyle-news-slides").owlCarousel({
      loop: true,
      nav: true,
      dots: false,
      autoplayHoverPause: true,
      autoplay: true,
      items: 1,
      navText: [
        "<i class='icofont-rounded-left'></i>",
        "<i class='icofont-rounded-right'></i>",
      ],
    }),
    e(".politics-news-slides").owlCarousel({
      loop: true,
      nav: true,
      dots: false,
      autoplayHoverPause: true,
      autoplay: true,
      items: 1,
      navText: [
        "<i class='icofont-rounded-left'></i>",
        "<i class='icofont-rounded-right'></i>",
      ],
    }),
    e(".gallery-news-inner-slides").owlCarousel({
      loop: true,
      nav: true,
      dots: false,
      autoplayHoverPause: true,
      autoplay: true,
      items: 1,
      navText: [
        "<i class='icofont-rounded-left'></i>",
        "<i class='icofont-rounded-right'></i>",
      ],
    }),
    e(".blog-home-slides").owlCarousel({
      loop: true,
      nav: true,
      dots: false,
      smartSpeed: 2e3,
      autoplayHoverPause: true,
      autoplay: true,
      navText: [
        "<i class='icofont-arrow-left'></i>",
        "<i class='icofont-arrow-right'></i>",
      ],
      responsive: {
        0: { items: 1 },
        576: { items: 2 },
        768: { items: 2 },
        1200: { items: 3 },
      },
    }),
    setInterval(function () {
      var o, s, a, t, i, n, l;
      (o = new Date("September 30, 2025 17:00:00 PDT")),
        (o = Date.parse(o) / 1e3),
        (s = new Date()),
        (a = o - (s = Date.parse(s) / 1e3)),
        (t = Math.floor(a / 86400)),
        (i = Math.floor((a - 86400 * t) / 3600)),
        (n = Math.floor((a - 86400 * t - 3600 * i) / 60)),
        (l = Math.floor(a - 86400 * t - 3600 * i - 60 * n)),
        i < "10" && (i = "0" + i),
        n < "10" && (n = "0" + n),
        l < "10" && (l = "0" + l),
        e("#days").html(t + "<span>Days</span>"),
        e("#hours").html(i + "<span>Hours</span>"),
        e("#minutes").html(n + "<span>Minutes</span>"),
        e("#seconds").html(l + "<span>Seconds</span>");
    }, 1e3),
    e(".new-news-slides").owlCarousel({
      loop: true,
      nav: true,
      dots: false,
      autoplayHoverPause: true,
      autoplay: true,
      items: 1,
      animateOut: "slideOutLeft",
      navText: [
        "<i class='icofont-rounded-left'></i>",
        "<i class='icofont-rounded-right'></i>",
      ],
    }),
    e(".more-news-slides").owlCarousel({
      loop: true,
      nav: true,
      dots: false,
      autoplayHoverPause: true,
      autoplay: true,
      margin: 30,
      navText: [
        "<i class='icofont-rounded-left'></i>",
        "<i class='icofont-rounded-right'></i>",
      ],
      responsive: { 0: { items: 1 }, 768: { items: 2 }, 1200: { items: 3 } },
    }),
    e(".default-news-slides").owlCarousel({
      loop: true,
      nav: true,
      dots: false,
      autoplayHoverPause: true,
      autoplay: true,
      margin: 30,
      navText: [
        "<i class='icofont-rounded-left'></i>",
        "<i class='icofont-rounded-right'></i>",
      ],
      responsive: { 0: { items: 1 }, 768: { items: 2 }, 1200: { items: 3 } },
    }),
    e(".popup-btn").magnificPopup({ type: "image", gallery: { enabled: !0 } }),
    e(".video-news-slides").owlCarousel({
      loop: true,
      nav: true,
      dots: false,
      autoplayHoverPause: true,
      autoplay: true,
      margin: 30,
      navText: [
        "<i class='icofont-rounded-left'></i>",
        "<i class='icofont-rounded-right'></i>",
      ],
      responsive: { 0: { items: 1 }, 768: { items: 2 }, 1200: { items: 2 } },
    }),
    e(function () {
      e(window).on("scroll", function () {
        var o = e(window).scrollTop();
        o > 300 && e(".go-top").fadeIn("slow"),
          o < 300 && e(".go-top").fadeOut("slow");
      }),
        e(".go-top").on("click", function () {
          e("html, body").animate({ scrollTop: "0" }, 500);
        });
    }),
    e(window).on("load", function () {
      e(".wow").length &&
        new WOW({
          boxClass: "wow",
          animateClass: "animated",
          offset: 20,
          mobile: true,
          live: true,
        }).init();
    });
})(jQuery);

(function ($) {
  "use strict";
function toggleTheme() {
  if (localStorage.getItem("sinmun_theme") === "theme-dark") {
    setTheme("theme-light");
  } else {
    setTheme("theme-dark");
  }
}
  // Switch Btn
  $("body").append(
    "<div class='switch-box'><label id='switch' class='switch'><input type='checkbox' id='slider'><span class='slider round'></span></label></div>"
  );


  $("input#slider").on("change", function(event){
    event.preventDefault();
    toggleTheme()
  })

})(jQuery);

// function to set a given theme/color-scheme
function setTheme(themeName) {
  localStorage.setItem("sinmun_theme", themeName);
  document.documentElement.className = themeName;
}

// Immediately invoked function to set the theme on initial load
(function () {
  if (localStorage.getItem("sinmun_theme") === "theme-dark") {
    setTheme("theme-dark");
    document.getElementById("slider").checked = false;
  } else {
    setTheme("theme-light");
    document.getElementById("slider").checked = true;
  }
})();

// mixitup
try {
  var mixer = mixitup(".shorting", {
    controls: {
      toggleDefault: "none",
    },
  });
} catch (err) {}
