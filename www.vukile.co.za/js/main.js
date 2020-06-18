jQuery(window).load(function() {
	


var anchgt = $('header section').height();	
	
    function goToByScroll(id){
       jQuery('html,body').animate({scrollTop: $("#"+id).offset().top - anchgt},'slow');
    }

    if(window.location.hash != '') {
        goToByScroll(window.location.hash.substr(1));  
};
	var hitems = $('section.showcase .main .big');
	var sw = window.innerWidth||document.documentElement.clientWidth||document.body.clientWidth;
	hitems.each(function() {
		if (sw > 800) {
			var itheight = $(this).find('ul li:nth-of-type(1)').outerHeight();
			$(this).css('height', itheight + 'px');
			$(this).find('img').css('height', itheight + 'px');
		}
		
	});
	
	
});


jQuery(document).ready(function() {

function homeSizes() {
	var homeart = $('body.home section aside.news').height();
	$('article.lft.hme').height('auto'); //homeart
	$('aside.news').height($('article.lft.hme').height());
}

$(window).load(homeSizes);
$(window).resize(homeSizes);

 

var anchgt = $('header section').height();

// anchors
$(function() {
	$('a.anchorJS').css('top', -($('header section').height()) + 'px');
	
	$('a[href*=#]:not([href=#])').click(function() {

		if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
			var target = $(this.hash);
			target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
			if (target.length) {
				$('html,body').animate({scrollTop: target.offset().top - anchgt}, 500);
				// return false;
			}
		}
	});
}); 
 
 
// SET HEIGHTS START 
var wdt = window.innerWidth;
var hgt = window.innerHeight;
var hgtsct = window.innerHeight - ($('header > section').height() + $('footer').outerHeight() - 1);
var hgtdiv = window.innerHeight / 2;

function resize () {
	//$('.wrapper .inner').css({minHeight:hgt+'px'});
	$('.inner > section').css({minHeight:hgtsct+'px'});
}
resize(); window.onresize = function () {resize();};
// SET HEIGHTS END 




// ACCORDIONO
$("ul.accpp li > div.drop").slideUp(300);
$("ul.accpp > li > a").click(function(){
	$('html,body').animate({scrollTop: $(this).offset().top - $('header section').height()}, 500);
	
    $(this).parent("li").parent("ul").find("div.drop").slideUp(300);
    $(this).parent("li").parent("ul").find("a").removeClass("active");
    if(!$(this).next().is(":visible"))
    {
     $(this).next().slideDown(300);
     $(this).addClass("active");
    }
 });


// MAIN NAV START
$('div.dropped').slideUp(0);
	$('a.nav').click(function(){
		$('div.dropped').slideToggle(300);
			$('a.nav div strong').toggleClass('close').html($('a.nav div strong').text() == 'CLOSE' ? 'MENU' : 'CLOSE');
				$('a.nav').toggleClass('shadow');
				});

// MAIN NAV END		



// SUB NAV START
$("ul.subnav li ul").hide(0);
jQuery('ul.subnav li').mouseleave(function(event) {
	$(this).find("ul").hide(0);
});

jQuery('ul.subnav li').mouseenter(function(event) {
    $(this).find("ul").slideToggle(300);
    if(!$(this).next().is(":visible"))
    {
     $(this).next().slideToggle(300);
    }
 });	
// SUB NAV END	
	


$('ul.subnav li a').on('click', function (event) {
	$("ul.subnav li ul").hide(0);
    var h = $(this.hash);
    var t = $(this).attr("href").split('#')[0]; // get the page name from href
    var l = window.location.pathname.replace(/\//g,""); // get the pathname from location
    if (t == l) { // if pathname matches the href page name
        event.preventDefault();
        $('html, body').animate({scrollTop: h.offset().top - 270}, 500);
    }
});



// UPDATES / CALENDAR
	/*$('li.calendarview').show(0);
	$('li.calendar').addClass('highlight');*/
		
	
	$('div.inv ul li a#jse, div.inv ul li p.jse').addClass('active');
	
	$('div.inv ul li a').click(function(){
		$('div.inv ul li a, div.inv ul li p').removeClass('active');
		toShow = $(this).attr('id');
		$(this).addClass('active');
		$('div.inv ul li p.' + toShow).addClass('active');
	});

	$('li.calendarview').hide(0);
	$('li.updates').addClass('highlight');
	$('li.calendar').removeClass('highlight');
	
	$('li.updates').click(function(){
		$('li.updatesview').show(100);
		$('li.calendarview').hide(0);
		$('li.updates').addClass('highlight');
		$('li.calendar').removeClass('highlight');
	});
	$('li.calendar').click(function(){
		$('li.updatesview').hide(0);
		$('li.calendarview').show(100);
		$('li.updates').removeClass('highlight');
		$('li.calendar').addClass('highlight');
	});
			
// SUBSCRIBE
$('.subscribe li').show(0);
	$('.subscribe li:nth-child(2)').toggle(0);
	
	$('.subscribe a').click(function(){
	$('.subscribe li:nth-child(1)').toggle(100);
	$('.subscribe li:nth-child(2)').toggle(100);
				});	

 
 // HOME - PROPERTY PORTFOLIO 
/*var thumb = $('.thumbnails a').width() - 2;
	$('.thumbnails a').css({width:thumb+'px'});*/

$('.thumbnails a').click(function(e){	
//$('.thumbnails a').on('click', function (e) {
	e.preventDefault();
	//e.stopPropagation();
	var eq = $(this).index();
	$('.main .big').removeClass('show'); $('.main .big').eq(eq).addClass('show'); $('.thumbnails a').removeClass('show'); $('.thumbnails a').eq(eq).addClass('show');
	
	var hitems = $('section.showcase .main .big');
	var sw = window.innerWidth||document.documentElement.clientWidth||document.body.clientWidth;
	hitems.each(function() {
		if (sw > 800) {
			var itheight = $(this).find('ul li:nth-of-type(1)').outerHeight();
			$(this).css('height', itheight + 'px');
			$(this).find('img').css('height', itheight + 'px');
		}
		
	});
	$('html,body').animate({scrollTop: $('.thumbnails').offset().top}, 0);
});
 

 // NEWS TABS START
$('.sens a').on('click', function () {var eq = $(this).index();
    $('.sensmain .big').removeClass('show'); $('.sensmain .big').eq(eq).addClass('show'); $('.sens a').removeClass('show');  $('.sens a').eq(eq).addClass('show');
});

$('.ceo a').on('click', function () {var eq = $(this).index();
    $('.ceomain .big').removeClass('show'); $('.ceomain .big').eq(eq).addClass('show'); $('.ceo a').removeClass('show');  $('.ceo a').eq(eq).addClass('show');
});
$('.press a').on('click', function () {var eq = $(this).index();
    $('.pressmain .big').removeClass('show'); $('.pressmain .big').eq(eq).addClass('show'); $('.press a').removeClass('show');  $('.press a').eq(eq).addClass('show');
});
 // NEWS TABS END



var sctwdt = $('section > header').width() - 2;
$('section.full').css({width:sctwdt+'px'});

// BACKTOP
jQuery('a.back-top').fadeOut(0);
jQuery(window).scroll(function() {
 if (jQuery(this).scrollTop() > 0) {
	 	jQuery('a.back-top').fadeIn(1500);
	} 
	else {
	 	jQuery('a.back-top').fadeOut(1500);
		}
 
 });
 
	jQuery('.back-top').click(function(event) {
        event.preventDefault();
        jQuery('html, body').animate({scrollTop: 0}, 1500);
        return false;
    }); 
	
});
function mobTableWidth() {
	"use strict";
	var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
	if (screenWidth < 1100) {
		jQuery('.mob-table-wrapper').css('width', (screenWidth - 60) + 'px');
	} else {
		jQuery('.mob-table-wrapper').css('width', '100%');
	}
}

function setMenuHeight() {
	"use strict";
	var hH = jQuery('header nav ul').outerHeight();
	var menH = jQuery('.txt ul').outerHeight();
	var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
	if (screenWidth < 1080) {
		if (!jQuery('body').hasClass('home')) {
			if (hH > 0) {
				jQuery('.wrapper .inner header:nth-of-type(1) img').css('height', (hH + menH + 20) + 'px');
				jQuery('.wrapper .inner header:nth-of-type(1) img').css('width', '100%');
			} else {
				jQuery('.wrapper .inner header:nth-of-type(1) img').css('height', '170px');
			}
		}
	}
}
jQuery(document).ready(function() {
	"use strict";
	mobTableWidth();
	setMenuHeight();
});

jQuery(window).resize(function() {
	"use strict";
	mobTableWidth();
	setMenuHeight();
});

//function setHeight() {
	/*if ($(window).width() > 800) {
		$('.main .big.show ul.img li:nth-of-type(2)').each(function(){
			$(this).find('img').height($(this).parent().height());
		});
	} else {
		$('.main .big.show ul.img li:nth-of-type(2)').each(function(){
			$(this).find('img').height('auto');
		});
	}*/
//}

//$(window).load(setHeight);
//$(window).resize(setHeight);