
## Mission to Mars


```python
from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests
import time
import pandas as pd
```

## NASA Mars News


```python
#set up splinter browser
executable_path = {'executable_path': 'driver/chromedriver'}
browser = Browser('chrome', **executable_path, headless = False)

#visit url
url = "https://mars.nasa.gov/news/"
browser.visit(url)

#pull html text and parse
html_code = browser.html
soup = BeautifulSoup(html_code, "html.parser")

#grab needed info
news_title = soup.find('div', class_="bottom_gradient").text
news_p = soup.find('div', class_="rollover_description_inner").text
```

## JPL Mars Space Images - Featured Image


```python
# Featured Image URL & visit
jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(jpl_url)

#navigate to link
browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(10)
browser.click_link_by_partial_text('more info')

# #get html code once at page
image_html = browser.html

# #parse
soup = BeautifulSoup(image_html, "html.parser")

# #find path and make full path
image_path = soup.find('figure', class_='lede').a['href']
featured_image_url = "https://www.jpl.nasa.gov/" + image_path
print(featured_image_url)
```

    https://www.jpl.nasa.gov//spaceimages/images/largesize/PIA18058_hires.jpg
    

## Mars Weather


```python
marsweather_url = "https://twitter.com/marswxreport?lang=en"
browser.visit(marsweather_url)

weather_html = browser.html

soup = BeautifulSoup(weather_html, 'html.parser')

mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
```

## Mars Facts


```python
#mars facts url and splinter visit
facts_url = "https://space-facts.com/mars/"
browser.visit(facts_url)

#get html
facts_html = browser.html

soup = BeautifulSoup(facts_html, 'html.parser')
soup
```




    <!DOCTYPE html>
    <html lang="en-US" prefix="og: http://ogp.me/ns#" xmlns="http://www.w3.org/1999/xhtml"><head>
    <meta content="153d19f04460b5eb7b1ed2d38890ad1e" name="maValidation"/>
    <meta charset="utf-8"/>
    <link href="https://space-facts.com/feed/" rel="alternate" title="Space Facts RSS Feed" type="application/rss+xml"/>
    <title>Mars Facts - Interesting Facts about Planet Mars</title>
    <meta content="Scientific, historic and cultural facts about Mars, the &quot;Red Planet&quot;. Learn about Mars' features, characteristics and missions!" name="description"/>
    <link href="https://space-facts.com/mars/" rel="canonical"/>
    <meta content="en_US" property="og:locale"/>
    <meta content="article" property="og:type"/>
    <meta content="Mars Facts - Interesting Facts about Planet Mars" property="og:title"/>
    <meta content="Scientific, historic and cultural facts about Mars, the &quot;Red Planet&quot;. Learn about Mars' features, characteristics and missions!" property="og:description"/>
    <meta content="https://space-facts.com/mars/" property="og:url"/>
    <meta content="Space Facts" property="og:site_name"/>
    <meta content="mars" property="article:tag"/>
    <meta content="Planets" property="article:section"/>
    <meta content="2012-01-05T13:32:39+00:00" property="article:published_time"/>
    <meta content="2017-12-06T21:13:47+00:00" property="article:modified_time"/>
    <meta content="2017-12-06T21:13:47+00:00" property="og:updated_time"/>
    <meta content="https://space-facts.com/wp-content/uploads/mars.jpg" property="og:image"/>
    <meta content="https://space-facts.com/wp-content/uploads/mars-size.png" property="og:image"/>
    <meta content="https://space-facts.com/wp-content/uploads/mars-orbit.png" property="og:image"/>
    <meta content="summary" name="twitter:card"/>
    <meta content="Scientific, historic and cultural facts about Mars, the &quot;Red Planet&quot;. Learn about Mars' features, characteristics and missions!" name="twitter:description"/>
    <meta content="Mars Facts - Interesting Facts about Planet Mars" name="twitter:title"/>
    <meta content="@_spacefacts" name="twitter:site"/>
    <meta content="https://space-facts.com/wp-content/uploads/mars.jpg" name="twitter:image"/>
    <meta content="@_SpaceFacts" name="twitter:creator"/>
    <script async="" src="https://apis.google.com/_/scs/apps-static/_/js/k=oz.gapi.en_US.9Iv2zI3hhA4.O/m=auth/exm=plusone/rt=j/sv=1/d=1/ed=1/am=AQE/rs=AGLTcCMpvfgYHgs56VN-05ik_fHHjzO8Cg/cb=gapi.loaded_1"></script><script async="" src="https://apis.google.com/_/scs/apps-static/_/js/k=oz.gapi.en_US.9Iv2zI3hhA4.O/m=plusone/rt=j/sv=1/d=1/ed=1/am=AQE/rs=AGLTcCMpvfgYHgs56VN-05ik_fHHjzO8Cg/cb=gapi.loaded_0"></script><script src="https://pagead2.googlesyndication.com/pub-config/r20160913/ca-pub-4251889121233823.js"></script><script async="" gapi_processed="true" src="https://apis.google.com/js/plusone.js" type="text/javascript"></script><script id="facebook-jssdk" src="//connect.facebook.net/en_GB/sdk.js#xfbml=1&amp;version=v2.3"></script><script async="" src="https://www.google-analytics.com/analytics.js"></script><script type="application/ld+json">{"@context":"http:\/\/schema.org","@type":"WebSite","@id":"#website","url":"https:\/\/space-facts.com\/","name":"Space Facts","potentialAction":{"@type":"SearchAction","target":"https:\/\/space-facts.com\/?s={search_term_string}","query-input":"required name=search_term_string"}}</script>
    <link href="//s0.wp.com" rel="dns-prefetch"/>
    <link href="//fonts.googleapis.com" rel="dns-prefetch"/>
    <link href="//s.w.org" rel="dns-prefetch"/>
    <link href="https://space-facts.com/feed/" rel="alternate" title="Space Facts » Feed" type="application/rss+xml"/>
    <link href="https://space-facts.com/comments/feed/" rel="alternate" title="Space Facts » Comments Feed" type="application/rss+xml"/>
    <link href="https://space-facts.com/mars/feed/" rel="alternate" title="Space Facts » Mars Facts Comments Feed" type="application/rss+xml"/>
    <script>window._wpemojiSettings={"baseUrl":"https:\/\/s.w.org\/images\/core\/emoji\/2.4\/72x72\/","ext":".png","svgUrl":"https:\/\/s.w.org\/images\/core\/emoji\/2.4\/svg\/","svgExt":".svg","source":{"concatemoji":"https:\/\/space-facts.com\/wp-includes\/js\/wp-emoji-release.min.js?ver=4.9.4"}};
    !function(a,b,c){function d(a,b){var c=String.fromCharCode;l.clearRect(0,0,k.width,k.height),l.fillText(c.apply(this,a),0,0);var d=k.toDataURL();l.clearRect(0,0,k.width,k.height),l.fillText(c.apply(this,b),0,0);var e=k.toDataURL();return d===e}function e(a){var b;if(!l||!l.fillText)return!1;switch(l.textBaseline="top",l.font="600 32px Arial",a){case"flag":return!(b=d([55356,56826,55356,56819],[55356,56826,8203,55356,56819]))&amp;&amp;(b=d([55356,57332,56128,56423,56128,56418,56128,56421,56128,56430,56128,56423,56128,56447],[55356,57332,8203,56128,56423,8203,56128,56418,8203,56128,56421,8203,56128,56430,8203,56128,56423,8203,56128,56447]),!b);case"emoji":return b=d([55357,56692,8205,9792,65039],[55357,56692,8203,9792,65039]),!b}return!1}function f(a){var c=b.createElement("script");c.src=a,c.defer=c.type="text/javascript",b.getElementsByTagName("head")[0].appendChild(c)}var g,h,i,j,k=b.createElement("canvas"),l=k.getContext&amp;&amp;k.getContext("2d");for(j=Array("flag","emoji"),c.supports={everything:!0,everythingExceptFlag:!0},i=0;i&lt;j.length;i++)c.supports[j[i]]=e(j[i]),c.supports.everything=c.supports.everything&amp;&amp;c.supports[j[i]],"flag"!==j[i]&amp;&amp;(c.supports.everythingExceptFlag=c.supports.everythingExceptFlag&amp;&amp;c.supports[j[i]]);c.supports.everythingExceptFlag=c.supports.everythingExceptFlag&amp;&amp;!c.supports.flag,c.DOMReady=!1,c.readyCallback=function(){c.DOMReady=!0},c.supports.everything||(h=function(){c.readyCallback()},b.addEventListener?(b.addEventListener("DOMContentLoaded",h,!1),a.addEventListener("load",h,!1)):(a.attachEvent("onload",h),b.attachEvent("onreadystatechange",function(){"complete"===b.readyState&amp;&amp;c.readyCallback()})),g=c.source||{},g.concatemoji?f(g.concatemoji):g.wpemoji&amp;&amp;g.twemoji&amp;&amp;(f(g.twemoji),f(g.wpemoji)))}(window,document,window._wpemojiSettings);</script><script defer="" src="https://space-facts.com/wp-includes/js/wp-emoji-release.min.js?ver=4.9.4" type="text/javascript"></script>
    <style>img.wp-smiley,
    img.emoji{display:inline !important;border:none !important;box-shadow:none !important;height:1em !important;width:1em !important;margin:0 .07em !important;vertical-align:-0.1em !important;background:none !important;padding:0 !important;}</style>
    <link href="//space-facts.com/wp-content/cache/wpfc-minified/b7a1752262e52bb94d575fa89377b9a9/1518688582index.css" media="all" rel="stylesheet" type="text/css"/>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans%3A400%2C400italic%2C600%2C600italic%2C700%2C700italic%2C300italic%2C300%2C800%2C800italic&amp;ver=4.9.4" id="google-fonts-css" media="all" rel="stylesheet" type="text/css"/>
    <link href="//space-facts.com/wp-content/cache/wpfc-minified/50145cfd8173c9370d583a1959a45389/1518688581index.css" media="all" rel="stylesheet" type="text/css"/>
    <script src="https://space-facts.com/wp-includes/js/jquery/jquery.js?ver=1.12.4"></script>
    <script src="https://space-facts.com/wp-includes/js/jquery/jquery-migrate.min.js?ver=1.4.1"></script>
    <script>
    var wpp_params={"sampling_active":"0","sampling_rate":"100","ajax_url":"https:\/\/space-facts.com\/wp-admin\/admin-ajax.php","action":"update_views_ajax","ID":"17","token":"bd61cee7e6"};
    </script>
    <script src="https://space-facts.com/wp-content/plugins/wordpress-popular-posts/public/js/wpp.js?ver=4.0.13"></script>
    <script src="https://space-facts.com/wp-content/themes/OneShot/js/audio-player.js?ver=4.9.4"></script>
    <link href="https://space-facts.com/wp-json/" rel="https://api.w.org/"/>
    <link href="https://space-facts.com/xmlrpc.php?rsd" rel="EditURI" title="RSD" type="application/rsd+xml"/>
    <link href="https://space-facts.com/wp-includes/wlwmanifest.xml" rel="wlwmanifest" type="application/wlwmanifest+xml"/>
    <meta content="WordPress 4.9.4" name="generator"/>
    <link href="https://wp.me/s2wL07-mars" rel="shortlink"/>
    <link href="https://space-facts.com/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fspace-facts.com%2Fmars%2F" rel="alternate" type="application/json+oembed"/>
    <link href="https://space-facts.com/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fspace-facts.com%2Fmars%2F&amp;format=xml" rel="alternate" type="text/xml+oembed"/>
    <style id="ctcc-css" media="screen">#catapult-cookie-bar{box-sizing:border-box;max-height:0;opacity:0;z-index:99999;overflow:hidden;color:#f5f5f5;position:fixed;left:0;bottom:0;width:100%;background-color:#0a0a0a;}
    #catapult-cookie-bar a{color:#fff;}
    #catapult-cookie-bar .x_close span{background-color:#ffffff;}
    button#catapultCookie{background:#17274e;color:#ffffff;border:0;padding:6px 9px;border-radius:3px;}
    #catapult-cookie-bar h3{color:#f5f5f5;}
    .has-cookie-bar #catapult-cookie-bar{opacity:1;max-height:999px;min-height:30px;}</style>
    <link href="//v0.wordpress.com" rel="dns-prefetch"/>
    <style>body{background-image:none;background-color:#000000;}
    body{color:#f5f5f5;}
    a{color:#a1d0ff;}
    body a:hover{color:#E41B00;text-decoration:none;}
    h1{color:#ffffff;font-size:22px;font-weight:normal;text-transform:capitalize;text-decoration:none;}
    h2{color:#57FF8D;font-size:24px;font-weight:normal;font-style:normal;font-variant:normal;text-transform:capitalize;text-decoration:none;}
    h3{color:#f0f0f0;font-size:22px;font-weight:normal;}
    h4{color:#f0f0f0;font-size:18px;font-weight:normal;}
    h5{font-weight:normal;}
    h6{font-weight:normal;}
    input[type=text], input[type=search], input[type=password], textarea{font-family:Arial, Helvetica, sans-serif;}
    input[type=reset], input[type=submit]{background-color:#1a1a1a;color:#ebebeb;}
    input[type=reset]:hover, input[type=submit]:hover{background-color:#ffffff;color:#000000;}
    #footer a:hover{text-decoration:none;}
    #footer .widgettitle{font-size:22px;}</style>
    <link href="https://space-facts.com/wp-content/themes/OneShot/uploads/favicon/favicon.png" rel="shortcut icon"/>
    <style>@font-face{font-family:'CarbonBlockRegular';src:url('https://space-facts.com/fonts/carbon_bl.eot');src:url('https://space-facts.com/fonts/carbon_bl.eot?#iefix') format('embedded-opentype'), url('https://space-facts.com/fonts/carbon_bl.woff') format('woff'), url('https://space-facts.com/fonts/carbon_bl.ttf') format('truetype'), url('https://space-facts.com/fonts/carbon_bl.svg#CarbonBlockRegular') format('svg');font-weight:normal;font-style:normal;}</style>
    <!--[if lt IE 9]>
    <script src="https://space-facts.com/wp-content/themes/OneShot/js/respond.js"></script>
    <![endif]-->
    <!--[if lt IE 9]>
    <script src="https://css3-mediaqueries-js.googlecode.com/svn/trunk/css3-mediaqueries.js"></script>
    <![endif]-->
    <!--[if lt IE 9]>
    <script src="https://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/><link href="https://space-facts.com/mars/amp/" rel="amphtml"/>
    <link href="//space-facts.com/wp-content/cache/wpfc-minified/f6c6fe674c5e7554c3084c866f53edd1/1518688581index.css" media="screen, projection" rel="stylesheet" type="text/css"/>
    <link href="https://space-facts.com/?custom-css=1c988d133b" id="wp-custom-css" rel="stylesheet" type="text/css"/>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet" type="text/css"/>
    <link href="https://plus.google.com/105688062769412508093/" rel="publisher"/>
    <meta content="727375480" property="fb:admins"/>
    <script type="application/ld+json">{  "@context":"http://schema.org",
    "@type":"WebSite",
    "name":"Space Facts",
    "alternateName":"SpaceFacts.com",
    "url":"https://space-facts.com"
    }</script>
    <script>(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,'script','https://www.google-analytics.com/analytics.js','ga'); ga('create', 'UA-32348920-1', 'auto'); ga('send', 'pageview');</script>
    <link as="script" href="https://adservice.google.com/adsid/integrator.js?domain=space-facts.com" rel="preload"/><script src="https://adservice.google.com/adsid/integrator.js?domain=space-facts.com" type="text/javascript"></script><style type="text/css">.fb_hidden{position:absolute;top:-10000px;z-index:10001}.fb_reposition{overflow:hidden;position:relative}.fb_invisible{display:none}.fb_reset{background:none;border:0;border-spacing:0;color:#000;cursor:auto;direction:ltr;font-family:"lucida grande", tahoma, verdana, arial, sans-serif;font-size:11px;font-style:normal;font-variant:normal;font-weight:normal;letter-spacing:normal;line-height:1;margin:0;overflow:visible;padding:0;text-align:left;text-decoration:none;text-indent:0;text-shadow:none;text-transform:none;visibility:visible;white-space:normal;word-spacing:normal}.fb_reset&gt;div{overflow:hidden}.fb_link img{border:none}@keyframes fb_transform{from{opacity:0;transform:scale(.95)}to{opacity:1;transform:scale(1)}}.fb_animate{animation:fb_transform .3s forwards}
    .fb_dialog{background:rgba(82, 82, 82, .7);position:absolute;top:-10000px;z-index:10001}.fb_reset .fb_dialog_legacy{overflow:visible}.fb_dialog_advanced{padding:10px;border-radius:8px}.fb_dialog_content{background:#fff;color:#333}.fb_dialog_close_icon{background:url(https://static.xx.fbcdn.net/rsrc.php/v3/yq/r/IE9JII6Z1Ys.png) no-repeat scroll 0 0 transparent;cursor:pointer;display:block;height:15px;position:absolute;right:18px;top:17px;width:15px}.fb_dialog_mobile .fb_dialog_close_icon{top:5px;left:5px;right:auto}.fb_dialog_padding{background-color:transparent;position:absolute;width:1px;z-index:-1}.fb_dialog_close_icon:hover{background:url(https://static.xx.fbcdn.net/rsrc.php/v3/yq/r/IE9JII6Z1Ys.png) no-repeat scroll 0 -15px transparent}.fb_dialog_close_icon:active{background:url(https://static.xx.fbcdn.net/rsrc.php/v3/yq/r/IE9JII6Z1Ys.png) no-repeat scroll 0 -30px transparent}.fb_dialog_loader{background-color:#f6f7f9;border:1px solid #606060;font-size:24px;padding:20px}.fb_dialog_top_left,.fb_dialog_top_right,.fb_dialog_bottom_left,.fb_dialog_bottom_right{height:10px;width:10px;overflow:hidden;position:absolute}.fb_dialog_top_left{background:url(https://static.xx.fbcdn.net/rsrc.php/v3/ye/r/8YeTNIlTZjm.png) no-repeat 0 0;left:-10px;top:-10px}.fb_dialog_top_right{background:url(https://static.xx.fbcdn.net/rsrc.php/v3/ye/r/8YeTNIlTZjm.png) no-repeat 0 -10px;right:-10px;top:-10px}.fb_dialog_bottom_left{background:url(https://static.xx.fbcdn.net/rsrc.php/v3/ye/r/8YeTNIlTZjm.png) no-repeat 0 -20px;bottom:-10px;left:-10px}.fb_dialog_bottom_right{background:url(https://static.xx.fbcdn.net/rsrc.php/v3/ye/r/8YeTNIlTZjm.png) no-repeat 0 -30px;right:-10px;bottom:-10px}.fb_dialog_vert_left,.fb_dialog_vert_right,.fb_dialog_horiz_top,.fb_dialog_horiz_bottom{position:absolute;background:#525252;filter:alpha(opacity=70);opacity:.7}.fb_dialog_vert_left,.fb_dialog_vert_right{width:10px;height:100%}.fb_dialog_vert_left{margin-left:-10px}.fb_dialog_vert_right{right:0;margin-right:-10px}.fb_dialog_horiz_top,.fb_dialog_horiz_bottom{width:100%;height:10px}.fb_dialog_horiz_top{margin-top:-10px}.fb_dialog_horiz_bottom{bottom:0;margin-bottom:-10px}.fb_dialog_iframe{line-height:0}.fb_dialog_content .dialog_title{background:#6d84b4;border:1px solid #365899;color:#fff;font-size:14px;font-weight:bold;margin:0}.fb_dialog_content .dialog_title&gt;span{background:url(https://static.xx.fbcdn.net/rsrc.php/v3/yd/r/Cou7n-nqK52.gif) no-repeat 5px 50%;float:left;padding:5px 0 7px 26px}body.fb_hidden{-webkit-transform:none;height:100%;margin:0;overflow:visible;position:absolute;top:-10000px;left:0;width:100%}.fb_dialog.fb_dialog_mobile.loading{background:url(https://static.xx.fbcdn.net/rsrc.php/v3/ya/r/3rhSv5V8j3o.gif) white no-repeat 50% 50%;min-height:100%;min-width:100%;overflow:hidden;position:absolute;top:0;z-index:10001}.fb_dialog.fb_dialog_mobile.loading.centered{width:auto;height:auto;min-height:initial;min-width:initial;background:none}.fb_dialog.fb_dialog_mobile.loading.centered #fb_dialog_loader_spinner{width:100%}.fb_dialog.fb_dialog_mobile.loading.centered .fb_dialog_content{background:none}.loading.centered #fb_dialog_loader_close{color:#fff;display:block;padding-top:20px;clear:both;font-size:18px}#fb-root #fb_dialog_ipad_overlay{background:rgba(0, 0, 0, .45);position:absolute;bottom:0;left:0;right:0;top:0;width:100%;min-height:100%;z-index:10000}#fb-root #fb_dialog_ipad_overlay.hidden{display:none}.fb_dialog.fb_dialog_mobile.loading iframe{visibility:hidden}.fb_dialog_content .dialog_header{-webkit-box-shadow:white 0 1px 1px -1px inset;background:-webkit-gradient(linear, 0% 0%, 0% 100%, from(#738ABA), to(#2C4987));border-bottom:1px solid;border-color:#1d4088;color:#fff;font:14px Helvetica, sans-serif;font-weight:bold;text-overflow:ellipsis;text-shadow:rgba(0, 30, 84, .296875) 0 -1px 0;vertical-align:middle;white-space:nowrap}.fb_dialog_content .dialog_header table{-webkit-font-smoothing:subpixel-antialiased;height:43px;width:100%}.fb_dialog_content .dialog_header td.header_left{font-size:12px;padding-left:5px;vertical-align:middle;width:60px}.fb_dialog_content .dialog_header td.header_right{font-size:12px;padding-right:5px;vertical-align:middle;width:60px}.fb_dialog_content .touchable_button{background:-webkit-gradient(linear, 0% 0%, 0% 100%, from(#4966A6), color-stop(.5, #355492), to(#2A4887));border:1px solid #29487d;-webkit-background-clip:padding-box;-webkit-border-radius:3px;-webkit-box-shadow:rgba(0, 0, 0, .117188) 0 1px 1px inset, rgba(255, 255, 255, .167969) 0 1px 0;display:inline-block;margin-top:3px;max-width:85px;line-height:18px;padding:4px 12px;position:relative}.fb_dialog_content .dialog_header .touchable_button input{border:none;background:none;color:#fff;font:12px Helvetica, sans-serif;font-weight:bold;margin:2px -12px;padding:2px 6px 3px 6px;text-shadow:rgba(0, 30, 84, .296875) 0 -1px 0}.fb_dialog_content .dialog_header .header_center{color:#fff;font-size:16px;font-weight:bold;line-height:18px;text-align:center;vertical-align:middle}.fb_dialog_content .dialog_content{background:url(https://static.xx.fbcdn.net/rsrc.php/v3/y9/r/jKEcVPZFk-2.gif) no-repeat 50% 50%;border:1px solid #555;border-bottom:0;border-top:0;height:150px}.fb_dialog_content .dialog_footer{background:#f6f7f9;border:1px solid #555;border-top-color:#ccc;height:40px}#fb_dialog_loader_close{float:left}.fb_dialog.fb_dialog_mobile .fb_dialog_close_button{text-shadow:rgba(0, 30, 84, .296875) 0 -1px 0}.fb_dialog.fb_dialog_mobile .fb_dialog_close_icon{visibility:hidden}#fb_dialog_loader_spinner{animation:rotateSpinner 1.2s linear infinite;background-color:transparent;background-image:url(https://static.xx.fbcdn.net/rsrc.php/v3/yD/r/t-wz8gw1xG1.png);background-repeat:no-repeat;background-position:50% 50%;height:24px;width:24px}@keyframes rotateSpinner{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}
    .fb_iframe_widget{display:inline-block;position:relative}.fb_iframe_widget span{display:inline-block;position:relative;text-align:justify}.fb_iframe_widget iframe{position:absolute}.fb_iframe_widget_fluid_desktop,.fb_iframe_widget_fluid_desktop span,.fb_iframe_widget_fluid_desktop iframe{max-width:100%}.fb_iframe_widget_fluid_desktop iframe{min-width:220px;position:relative}.fb_iframe_widget_lift{z-index:1}.fb_hide_iframes iframe{position:relative;left:-10000px}.fb_iframe_widget_loader{position:relative;display:inline-block}.fb_iframe_widget_fluid{display:inline}.fb_iframe_widget_fluid span{width:100%}.fb_iframe_widget_loader iframe{min-height:32px;z-index:2;zoom:1}.fb_iframe_widget_loader .FB_Loader{background:url(https://static.xx.fbcdn.net/rsrc.php/v3/y9/r/jKEcVPZFk-2.gif) no-repeat;height:32px;width:32px;margin-left:-16px;position:absolute;left:50%;z-index:4}
    .fb_customer_chat_bounce_in{animation-duration:250ms;animation-name:fb_bounce_in}.fb_customer_chat_bounce_out{animation-duration:250ms;animation-name:fb_fade_out}.fb_invisible_flow{display:inherit;height:0;overflow-x:hidden;width:0}.fb_mobile_overlay_active{background-color:#fff;height:100%;overflow:hidden;position:fixed;visibility:hidden;width:100%}@keyframes fb_fade_out{from{opacity:1}to{opacity:0}}@keyframes fb_bounce_in{0%{opacity:0;transform:scale(.8, .8);transform-origin:100% 100%}10%{opacity:.1}20%{opacity:.2}30%{opacity:.3}40%{opacity:.4}50%{opacity:.5}60%{opacity:.6}70%{opacity:.7}80%{opacity:.8;transform:scale(1.03, 1.03)}90{opacity:.9}100%{opacity:1;transform:scale(1, 1)}}</style></head>
    <body class="post-template-default single single-post postid-17 single-format-standard" data-rsssl="1">
    <div class="pagewidth" id="pagewrap">
    <div id="headerwrap">
    <header class="pagewidth" id="header">
    <hgroup>
    <div id="site-logo"><a href="https://space-facts.com"><img alt="Space Facts" height="122" src="https://space-facts.com/wp-content/uploads/Space-Facts-Logo.png" width="215"/></a></div></hgroup>
    <div id="main-nav-wrap">
    <div class="mobile-button" id="menu-icon"></div><nav>
    <ul class="main-nav" id="main-nav"><li class="menu-item menu-item-type-post_type menu-item-object-page current-menu-ancestor current-menu-parent current_page_parent current_page_ancestor menu-item-has-children menu-item-823" id="menu-item-823"><a href="https://space-facts.com/planets/">Planets</a>
    <ul class="sub-menu">
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-827" id="menu-item-827"><a href="https://space-facts.com/mercury/">Mercury</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-826" id="menu-item-826"><a href="https://space-facts.com/venus/">Venus</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-825" id="menu-item-825"><a href="https://space-facts.com/earth/">Earth</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom current-menu-item menu-item-824" id="menu-item-824"><a href="https://space-facts.com/mars/">Mars</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-828" id="menu-item-828"><a href="https://space-facts.com/jupiter/">Jupiter</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-829" id="menu-item-829"><a href="https://space-facts.com/saturn/">Saturn</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-830" id="menu-item-830"><a href="https://space-facts.com/uranus/">Uranus</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-831" id="menu-item-831"><a href="https://space-facts.com/neptune/">Neptune</a></li>
    <li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-2695" id="menu-item-2695"><a href="https://space-facts.com/gas-giants/">Gas Giants</a></li>
    <li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-2696" id="menu-item-2696"><a href="https://space-facts.com/terrestrial-planets/">Terrestrial Planets</a></li>
    </ul>
    </li>
    <li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-821" id="menu-item-821"><a href="https://space-facts.com/solar-system/">Solar System</a>
    <ul class="sub-menu">
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-832" id="menu-item-832"><a href="https://space-facts.com/the-sun/">The Sun</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-833" id="menu-item-833"><a href="https://space-facts.com/the-moon/">The Moon</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-2587" id="menu-item-2587"><a href="https://space-facts.com/asteroid-belt/">Asteroid Belt</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-2739" id="menu-item-2739"><a href="https://space-facts.com/kuiper-belt/">Kuiper Belt</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-2771" id="menu-item-2771"><a href="https://space-facts.com/oort-cloud/">Oort Cloud</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-1340" id="menu-item-1340"><a href="https://space-facts.com/solar-eclipse/">Solar Eclipses</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-2373" id="menu-item-2373"><a href="https://space-facts.com/comets/">Comets</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-2374" id="menu-item-2374"><a href="https://space-facts.com/asteroids/">Asteroids</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-2589" id="menu-item-2589"><a href="https://space-facts.com/meteorites/">Meteorites</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-2588" id="menu-item-2588"><a href="https://space-facts.com/meteor-showers/">Meteor Showers</a></li>
    </ul>
    </li>
    <li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-820" id="menu-item-820"><a href="https://space-facts.com/galaxies/">Galaxies</a>
    <ul class="sub-menu">
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-3298" id="menu-item-3298"><a href="https://space-facts.com/milky-way/">Milky Way</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-1793" id="menu-item-1793"><a href="https://space-facts.com/andromeda/">Andromeda</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-3301" id="menu-item-3301"><a href="https://space-facts.com/sombrero-galaxy/">Sombrero</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-3450" id="menu-item-3450"><a href="https://space-facts.com/whirlpool-galaxy/">Whirlpool</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-3628" id="menu-item-3628"><a href="https://space-facts.com/triangulum-galaxy/">Triangulum</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-3317" id="menu-item-3317"><a href="https://space-facts.com/magellanic-clouds/">Magellanic Clouds</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-3629" id="menu-item-3629"><a href="https://space-facts.com/pinwheel-galaxy/">Pinwheel</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-3323" id="menu-item-3323"><a href="https://space-facts.com/m87-galaxy/">Messier 87</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-3329" id="menu-item-3329"><a href="https://space-facts.com/antennae-galaxies/">Antennae</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-3514" id="menu-item-3514"><a href="https://space-facts.com/black-holes/">Black Holes</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-3513" id="menu-item-3513"><a href="https://space-facts.com/galaxy-types/">Types of Galaxies</a></li>
    </ul>
    </li>
    <li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-5090" id="menu-item-5090"><a href="https://space-facts.com/moons/">Moons</a>
    <ul class="sub-menu">
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-5091" id="menu-item-5091"><a href="https://space-facts.com/phobos/">Phobos</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-5092" id="menu-item-5092"><a href="https://space-facts.com/deimos/">Deimos</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-5093" id="menu-item-5093"><a href="https://space-facts.com/io/">Io</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-5094" id="menu-item-5094"><a href="https://space-facts.com/europa/">Europa</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-5095" id="menu-item-5095"><a href="https://space-facts.com/ganymede/">Ganymede</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-5096" id="menu-item-5096"><a href="https://space-facts.com/callisto/">Callisto</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-5097" id="menu-item-5097"><a href="https://space-facts.com/titan/">Titan</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-5098" id="menu-item-5098"><a href="https://space-facts.com/triton/">Triton</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-5099" id="menu-item-5099"><a href="https://space-facts.com/charon/">Charon</a></li>
    </ul>
    </li>
    <li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-957" id="menu-item-957"><a href="https://space-facts.com/dwarf-planets/">Dwarf Planets</a>
    <ul class="sub-menu">
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-1493" id="menu-item-1493"><a href="https://space-facts.com/ceres/">Ceres</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-1347" id="menu-item-1347"><a href="https://space-facts.com/pluto/">Pluto</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-1529" id="menu-item-1529"><a href="https://space-facts.com/haumea/">Haumea</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-1513" id="menu-item-1513"><a href="https://space-facts.com/makemake/">Makemake</a></li>
    <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-1528" id="menu-item-1528"><a href="https://space-facts.com/eris/">Eris</a></li>
    </ul>
    </li>
    </ul>
    </nav>
    <div id="top-search"></div></div><meta content="40994c871d405312dfb519222232b26f" name="maValidation"/></header></div><div class="clearfix" id="body">
    <div class=" fb_reset" id="fb-root"><div style="position: absolute; top: -10000px; height: 0px; width: 0px;"><div><iframe allowfullscreen="true" allowtransparency="true" aria-hidden="true" frameborder="0" id="fb_xdm_frame_https" name="fb_xdm_frame_https" scrolling="no" src="https://staticxx.facebook.com/connect/xd_arbiter/r/Ms1VZf1Vg1J.js?version=42#channel=f3d0aedea7aba98&amp;origin=https%3A%2F%2Fspace-facts.com" style="border: none;" tabindex="-1" title="Facebook Cross Domain Communication Frame"></iframe></div></div><div style="position: absolute; top: -10000px; height: 0px; width: 0px;"><div></div></div></div><script>(function(d, s, id){
    var js, fjs=d.getElementsByTagName(s)[0];
    if(d.getElementById(id)) return;
    js=d.createElement(s); js.id=id;
    js.src="//connect.facebook.net/en_GB/sdk.js#xfbml=1&amp;version=v2.3";
    fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));</script>
    <div class="pagewidth clearfix sidebar1" id="layout">
    <div class="widget widget_text oko" id="text-26"> <div class="textwidget"><center>
    <div id="ad-responsive">
    <script async="" src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
    <ins class="adsbygoogle" data-ad-client="ca-pub-4251889121233823" data-ad-format="auto" data-ad-slot="8108869601" data-adsbygoogle-status="done" style="display: block; height: 90px;"><ins id="aswift_0_expand" style="display:inline-table;border:none;height:90px;margin:0;padding:0;position:relative;visibility:visible;width:730px;background-color:transparent;"><ins id="aswift_0_anchor" style="display:block;border:none;height:90px;margin:0;padding:0;position:relative;visibility:visible;width:730px;background-color:transparent;"><iframe allowfullscreen="true" allowtransparency="true" frameborder="0" height="90" hspace="0" id="aswift_0" marginheight="0" marginwidth="0" name="aswift_0" onload="var i=this.id,s=window.google_iframe_oncopy,H=s&amp;&amp;s.handlers,h=H&amp;&amp;H[i],w=this.contentWindow,d;try{d=w.document}catch(e){}if(h&amp;&amp;d&amp;&amp;(!d.body||!d.body.firstChild)){if(h.call){setTimeout(h,0)}else if(h.match){try{h=s.upd(h,i)}catch(e){}w.location.replace(h)}}" scrolling="no" style="left:0;position:absolute;top:0;width:730px;height:90px;" vspace="0" width="730"></iframe><div style="display: block; margin: 0px; padding: 0px; width: 15px; height: 31px; z-index: 2147483647; position: absolute; left: 730px; top: 0px;"><iframe allowtransparency="true" class="goog_xca_frame" frameborder="0" hspace="0" marginheight="0" marginwidth="0" scrolling="no" style="opacity: 1; transition: opacity 0.3s linear; margin: 0px; padding: 0px; width: 15px; height: 31px; z-index: 2147483647; display: block; position: relative; float: right;" vspace="0"></iframe></div></ins></ins></ins>
    <script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div></center></div></div><div id="filter">
    <h1 class="page-title">Mars Facts</h1>
    <div class="left"></div><div class="right"></div></div><div class="list-post" id="content">
    <article class="post clearfix post-17 type-post status-publish format-standard hentry category-planets category-terrestrial-planets tag-mars" id="post-17">
    <span class="post-icon"><span class="post-icon-inner"></span></span>
    <div class="post-content">
    <div class="wp-caption aligncenter" id="attachment_1086" style="max-width: 636px"><img alt="Mars" class="wp-image-1086 size-full" height="626" sizes="(max-width: 626px) 100vw, 626px" src="https://space-facts.com/wp-content/uploads/mars.jpg" srcset="https://space-facts.com/wp-content/uploads/mars.jpg 626w, https://space-facts.com/wp-content/uploads/mars-360x360.jpg 360w, https://space-facts.com/wp-content/uploads/mars-200x200.jpg 200w" title="Mars" width="626"/><p class="wp-caption-text">Mars Mosiac – astrogeology.usgs.gov</p></div><p>Mars is the fourth planet from the <a href="https://space-facts.com/the-sun/">Sun</a> and is the second smallest planet in the solar system. Named after the Roman god of war, Mars is also often described as the “Red Planet” due to its reddish appearance. Mars is a <a href="https://space-facts.com/terrestrial-planets/">terrestrial planet</a> with a thin atmosphere composed primarily of carbon dioxide.</p>
    <h2>Mars Planet Profile</h2>
    <table class="tablepress tablepress-id-mars" id="tablepress-mars">
    <tbody>
    <tr class="row-1 odd">
    <td class="column-1"><strong>Equatorial Diameter:</strong></td><td class="column-2">6,792 km<br/>
    </td>
    </tr>
    <tr class="row-2 even">
    <td class="column-1"><strong>Polar Diameter:</strong></td><td class="column-2">6,752 km<br/>
    </td>
    </tr>
    <tr class="row-3 odd">
    <td class="column-1"><strong>Mass:</strong></td><td class="column-2">6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr class="row-4 even">
    <td class="column-1"><strong>Moons:</strong></td><td class="column-2">2 (<a href="https://space-facts.com/phobos/">Phobos</a> &amp; <a href="https://space-facts.com/deimos/">Deimos</a>)</td>
    </tr>
    <tr class="row-5 odd">
    <td class="column-1"><strong>Orbit Distance:</strong></td><td class="column-2">227,943,824 km (1.52 AU)</td>
    </tr>
    <tr class="row-6 even">
    <td class="column-1"><strong>Orbit Period:</strong></td><td class="column-2">687 days (1.9 years)<br/>
    </td>
    </tr>
    <tr class="row-7 odd">
    <td class="column-1"><strong>Surface Temperature: </strong></td><td class="column-2">-153 to 20 °C</td>
    </tr>
    <tr class="row-8 even">
    <td class="column-1"><strong>First Record:</strong></td><td class="column-2">2nd millennium BC</td>
    </tr>
    <tr class="row-9 odd">
    <td class="column-1"><strong>Recorded By:</strong></td><td class="column-2">Egyptian astronomers</td>
    </tr>
    </tbody>
    </table>
    <div class="diagram-background" id="diagrams">
    <h2>Mars Diagrams</h2>
    <div class="wp-caption aligncenter" id="attachment_4837" style="max-width: 770px"><img alt="Mars size compared to Earth" class="size-full wp-image-4837" height="300" sizes="(max-width: 760px) 100vw, 760px" src="https://space-facts.com/wp-content/uploads/mars-size.png" srcset="https://space-facts.com/wp-content/uploads/mars-size.png 760w, https://space-facts.com/wp-content/uploads/mars-size-360x142.png 360w" width="760"/><p class="wp-caption-text"><span class="mars">Mars</span> size compared to <span class="earth">Earth</span></p></div><div class="wp-caption aligncenter" id="attachment_4836" style="max-width: 770px"><img alt="Mars distance from the Sun" class="size-full wp-image-4836" height="50" src="https://space-facts.com/wp-content/uploads/mars-orbit.png" width="760"/><p class="wp-caption-text"><span class="mars">Mars</span> distance from the <span class="sun">Sun</span> and orbital eccentricity</p></div></div><div id="facts">
    <h2>Facts about Mars</h2>
    <ul>
    <li><strong>Mars and Earth have approximately the same landmass.</strong><br/>
    Even though Mars has only 15% of the <a href="https://space-facts.com/earth/">Earth’s</a> volume and just over 10% of the Earth’s mass, around two thirds of the Earth’s surface is covered in water. Martian surface gravity is only 37% of the Earth’s (meaning you could leap nearly three times higher on Mars).</li>
    <li><strong>Mars is home to the tallest mountain in the solar system.</strong><br/>
    <a href="https://space-facts.com/mars-features/#olympus">Olympus Mons</a>, a shield volcano, is 21km high and 600km in diameter. Despite having formed over billions of years, evidence from volcanic lava flows is so recent many scientists believe it could still be active.</li>
    <li><strong>Only 18 missions to Mars have been successful.</strong><br/>
    As of September 2014 there have been 40 <a href="https://space-facts.com/mars-missions/">missions to Mars</a>, including orbiters, landers and rovers but not counting flybys. The most recent arrivals include the Mars Curiosity mission in 2012, the MAVEN mission, which arrived on September 22, 2014, followed by the Indian Space Research Organization’s MOM Mangalyaan orbiter, which arrived on September 24, 2014. The next missions to arrive will be the European Space Agency’s ExoMars mission, comprising an orbiter, lander, and a rover, followed by NASA’s InSight robotic lander mission, slated for launch in March 2016 and a planned arrival in September, 2016.</li>
    <li><strong>Mars has the largest dust storms in the solar system.</strong><br/>
    They can last for months and cover the entire planet. The seasons are extreme because its elliptical (oval-shaped) orbital path around the Sun is more elongated than most other planets in the <a href="https://space-facts.com/solar-system/">solar system</a>.</li>
    <li><strong>On Mars the Sun appears about half the size as it does on Earth.</strong><br/>
    At the closest point to the Sun, the Martian southern hemisphere leans towards the Sun, causing a short, intensely hot summer, while the northern hemisphere endures a brief, cold winter: at its farthest point from the Sun, the Martian northern hemisphere leans towards the Sun, causing a long, mild summer, while the southern hemisphere endures a lengthy, cold winter.</li>
    <li><strong>Pieces of Mars have fallen to Earth.</strong><br/>
    Scientists have found tiny traces of Martian atmosphere within meteorites violently ejected from Mars, then orbiting the solar system amongst galactic debris for millions of years, before crash landing on Earth. This allowed scientists to begin studying Mars prior to launching space missions.</li>
    <li><strong>Mars takes its name from the Roman god of war.</strong><br/>
    The ancient Greeks called the planet Ares, after their god of war; the Romans then did likewise, associating the planet’s blood-red colour with Mars, their own god of war. Interestingly, other ancient cultures also focused on colour – to China’s astronomers it was ‘the fire star’, whilst Egyptian priests called on ‘Her Desher’, or ‘the red one’. The red colour Mars is known for is due to the rock and dust covering its surface being rich in iron.</li>
    <li><strong>There are signs of liquid water on Mars.</strong><br/>
    For years Mars has been known to have water in the form of ice. The first signs of trickling water are dark stripes or stains on crater wall and cliffs seen in satellite images. Due to Mars’ atmosphere this water would have to be salty to prevent it from freezing or vaporising.</li>
    <li><strong>One day Mars will have a ring.</strong><br/>
    In the next 20-40 million years Mars’ largest moon Phobos will be torn apart by gravitational forces leading to the creation of a ring that could last up to 100 million years.</li>
    </ul></div><div class="contents"><a href="https://space-facts.com/mars/#facts">Facts</a> <a href="https://space-facts.com/mars-missions/">Missions</a> <a href="https://space-facts.com/mars-pictures/">Pictures</a> <a href="https://space-facts.com/moons/#mars">Moons</a> <a href="https://space-facts.com/mars-features/">Features</a> <a href="https://space-facts.com/mars-characteristics/">Characteristics</a></div><div class="sharedaddy sd-sharing-enabled"><div class="robots-nocontent sd-block sd-social sd-social-icon sd-sharing"><div class="sd-content"><ul><li class="share-twitter"><a class="share-twitter sd-button share-icon no-text" data-shared="sharing-twitter-17" href="https://space-facts.com/mars/?share=twitter&amp;nb=1" rel="nofollow" target="_blank" title="Click to share on Twitter"><span></span><span class="sharing-screen-reader-text">Click to share on Twitter (Opens in new window)</span></a></li><li class="share-facebook"><a class="share-facebook sd-button share-icon no-text" data-shared="sharing-facebook-17" href="https://space-facts.com/mars/?share=facebook&amp;nb=1" rel="nofollow" target="_blank" title="Click to share on Facebook"><span><span class="share-count">20</span></span><span class="sharing-screen-reader-text">Click to share on Facebook (Opens in new window)<span class="share-count">20</span></span></a></li><li class="share-google-plus-1"><a class="share-google-plus-1 sd-button share-icon no-text" data-shared="sharing-google-17" href="https://space-facts.com/mars/?share=google-plus-1&amp;nb=1" rel="nofollow" target="_blank" title="Click to share on Google+"><span></span><span class="sharing-screen-reader-text">Click to share on Google+ (Opens in new window)</span></a></li><li class="share-pinterest"><a class="share-pinterest sd-button share-icon no-text" data-shared="sharing-pinterest-17" href="https://space-facts.com/mars/?share=pinterest&amp;nb=1" rel="nofollow" target="_blank" title="Click to share on Pinterest"><span><span class="share-count">5</span></span><span class="sharing-screen-reader-text">Click to share on Pinterest (Opens in new window)<span class="share-count">5</span></span></a></li><li class="share-reddit"><a class="share-reddit sd-button share-icon no-text" data-shared="" href="https://space-facts.com/mars/?share=reddit&amp;nb=1" rel="nofollow" target="_blank" title="Click to share on Reddit"><span></span><span class="sharing-screen-reader-text">Click to share on Reddit (Opens in new window)</span></a></li><li class="share-end"></li></ul></div></div></div></div></article>
    <div class="widget widget_text oko" id="text-33"> <div class="textwidget"><center>
    <script async="" src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
    <ins class="adsbygoogle" data-ad-client="ca-pub-4251889121233823" data-ad-slot="8581451203" data-adsbygoogle-status="done" style="display: inline-block; width: 300px; height: 250px;"><ins id="aswift_1_expand" style="display:inline-table;border:none;height:250px;margin:0;padding:0;position:relative;visibility:visible;width:300px;background-color:transparent;"><ins id="aswift_1_anchor" style="display:block;border:none;height:250px;margin:0;padding:0;position:relative;visibility:visible;width:300px;background-color:transparent;"><iframe allowfullscreen="true" allowtransparency="true" frameborder="0" height="250" hspace="0" id="aswift_1" marginheight="0" marginwidth="0" name="aswift_1" onload="var i=this.id,s=window.google_iframe_oncopy,H=s&amp;&amp;s.handlers,h=H&amp;&amp;H[i],w=this.contentWindow,d;try{d=w.document}catch(e){}if(h&amp;&amp;d&amp;&amp;(!d.body||!d.body.firstChild)){if(h.call){setTimeout(h,0)}else if(h.match){try{h=s.upd(h,i)}catch(e){}w.location.replace(h)}}" scrolling="no" style="left:0;position:absolute;top:0;width:300px;height:250px;" vspace="0" width="300"></iframe><div style="display: block; margin: 0px; padding: 0px; width: 15px; height: 31px; z-index: 2147483647; position: absolute; left: 300px; top: 0px;"><iframe allowtransparency="true" class="goog_xca_frame" frameborder="0" hspace="0" marginheight="0" marginwidth="0" scrolling="no" style="opacity: 1; transition: opacity 0.3s linear; margin: 0px; padding: 0px; width: 15px; height: 31px; z-index: 2147483647; display: block; position: relative; float: right;" vspace="0"></iframe></div></ins></ins></ins>
    <script>(adsbygoogle=window.adsbygoogle||[]).push({});</script>
    </center></div></div><div class="yarpp-related"> <p></p><h2>Similar Facts</h2><p></p> <p><a href="https://space-facts.com/mars-missions/" rel="bookmark" title="Mars Missions">Mars Missions </a> Since the first spacecraft was sent to Mars was launched in 1960, there have been at least 68 missions that have been launched to...</p> <p><a href="https://space-facts.com/mars-curiosity-facts/" rel="bookmark" title="Mars Curiosity Facts">Mars Curiosity Facts </a> With the Mars Curiosity landing just a few hours away I thought it would be a good time to list some facts about the...</p> <p><a href="https://space-facts.com/mars-panorama/" rel="bookmark" title="Mars Panorama">Mars Panorama </a> A 360 degree panorama of the Martian landscape combined from 817 photos taken the Mars Exploration Rover Opportunity has been released by NASA. The photos were taken while the...</p></div></div><aside id="sidebar">
    <div class="widget widget_search" id="search-2"><form action="https://space-facts.com/" id="searchform" method="get"> <input id="s" name="s" placeholder="Search" type="text"/> </form></div><div class="widget widget_text" id="text-22"> <div class="textwidget"><div id="sf-social">
    <sf-social-3 style="padding-left:8%;">
    <iframe allowtransparency="true" class="twitter-follow-button twitter-follow-button" data-twttr-rendered="true" frameborder="0" id="twitter-widget-0" scrolling="no" src="https://platform.twitter.com/widgets/follow_button.f399ce91824b7ff2ece442a414e1a813.en.html#_=1430672116366&amp;dnt=true&amp;id=twitter-widget-0&amp;lang=en&amp;screen_name=_SpaceFacts&amp;show_count=true&amp;show_screen_name=true&amp;size=m" style="position: static; visibility: visible; width:100%; height: 20px;" title="Twitter Follow Button"></iframe>
    </sf-social-3>
    <div id="sf-social-1">
    <div class="fb-like fb_iframe_widget" data-action="like" data-href="https://space-facts.com/" data-layout="button_count" data-share="false" data-show-faces="false" fb-iframe-plugin-query="action=like&amp;app_id=&amp;container_width=100&amp;href=https%3A%2F%2Fspace-facts.com%2F&amp;layout=button_count&amp;locale=en_GB&amp;sdk=joey&amp;share=false&amp;show_faces=false" fb-xfbml-state="rendered"><span style="vertical-align: bottom; width: 73px; height: 20px;"><iframe allowfullscreen="true" allowtransparency="true" class="" frameborder="0" height="1000px" name="f286fe493a9c844" scrolling="no" src="https://www.facebook.com/v2.3/plugins/like.php?action=like&amp;app_id=&amp;channel=https%3A%2F%2Fstaticxx.facebook.com%2Fconnect%2Fxd_arbiter%2Fr%2FMs1VZf1Vg1J.js%3Fversion%3D42%23cb%3Df3eb271d3a06d2%26domain%3Dspace-facts.com%26origin%3Dhttps%253A%252F%252Fspace-facts.com%252Ff3d0aedea7aba98%26relation%3Dparent.parent&amp;container_width=100&amp;href=https%3A%2F%2Fspace-facts.com%2F&amp;layout=button_count&amp;locale=en_GB&amp;sdk=joey&amp;share=false&amp;show_faces=false" style="border: none; visibility: visible; width: 73px; height: 20px;" title="fb:like Facebook Social Plugin" width="1000px"></iframe></span></div></div><div id="sf-social-2">
    <div id="___plusone_0" style="text-indent: 0px; margin: 0px; padding: 0px; background: transparent; border-style: none; float: none; line-height: normal; font-size: 1px; vertical-align: baseline; display: inline-block; width: 32px; height: 20px;"><iframe data-gapiattached="true" frameborder="0" hspace="0" id="I0_1522185709107" marginheight="0" marginwidth="0" name="I0_1522185709107" ng-non-bindable="" scrolling="no" src="https://apis.google.com/se/0/_/+1/fastbutton?usegapi=1&amp;size=medium&amp;origin=https%3A%2F%2Fspace-facts.com&amp;url=https%3A%2F%2Fspace-facts.com%2F&amp;gsrc=3p&amp;ic=1&amp;jsh=m%3B%2F_%2Fscs%2Fapps-static%2F_%2Fjs%2Fk%3Doz.gapi.en_US.9Iv2zI3hhA4.O%2Fm%3D__features__%2Fam%3DAQE%2Frt%3Dj%2Fd%3D1%2Frs%3DAGLTcCMpvfgYHgs56VN-05ik_fHHjzO8Cg#_methods=onPlusOne%2C_ready%2C_close%2C_open%2C_resizeMe%2C_renderstart%2Concircled%2Cdrefresh%2Cerefresh%2Conload&amp;id=I0_1522185709107&amp;_gfid=I0_1522185709107&amp;parent=https%3A%2F%2Fspace-facts.com&amp;pfname=&amp;rpctoken=24486533" style="position: static; top: 0px; width: 32px; margin: 0px; border-style: none; left: 0px; visibility: visible; height: 20px;" tabindex="0" title="G+" vspace="0" width="100%"></iframe></div></div></div></div></div><div class="widget widget_text" id="text-46"> <div class="textwidget"><div class="box-container">
    <div id="ad">
    <script async="" src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
    <ins class="adsbygoogle" data-ad-client="ca-pub-4251889121233823" data-ad-slot="3665370407" data-adsbygoogle-status="done" style="display:inline-block;width:160px;height:600px"><ins id="aswift_2_expand" style="display:inline-table;border:none;height:600px;margin:0;padding:0;position:relative;visibility:visible;width:160px;background-color:transparent;"><ins id="aswift_2_anchor" style="display:block;border:none;height:600px;margin:0;padding:0;position:relative;visibility:visible;width:160px;background-color:transparent;"><iframe allowfullscreen="true" allowtransparency="true" frameborder="0" height="600" hspace="0" id="aswift_2" marginheight="0" marginwidth="0" name="aswift_2" onload="var i=this.id,s=window.google_iframe_oncopy,H=s&amp;&amp;s.handlers,h=H&amp;&amp;H[i],w=this.contentWindow,d;try{d=w.document}catch(e){}if(h&amp;&amp;d&amp;&amp;(!d.body||!d.body.firstChild)){if(h.call){setTimeout(h,0)}else if(h.match){try{h=s.upd(h,i)}catch(e){}w.location.replace(h)}}" scrolling="no" style="left:0;position:absolute;top:0;width:160px;height:600px;" vspace="0" width="160"></iframe></ins></ins></ins>
    <script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div><div class="widget popular-posts" id="wpp2">
    <h3>Top Facts</h3>
    <div class="widget popular-posts" id="wpp3">
    <ul class="wpp-list">
    <li><a href="https://space-facts.com/mercury/" target="_self" title="Mercury Facts"><img alt="Mercury Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/216-first_image-20x20.png" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/mercury/" target="_self" title="Mercury Facts">Mercury Facts</a> <span class="wpp-meta post-stats"></span></li>
    <li><a href="https://space-facts.com/earth/" target="_self" title="Earth Facts"><img alt="Earth Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/270-first_image-20x20.png" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/earth/" target="_self" title="Earth Facts">Earth Facts</a> <span class="wpp-meta post-stats"></span></li>
    <li><a href="https://space-facts.com/mars/" target="_self" title="Mars Facts"><img alt="Mars Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/17-first_image-20x20.jpg" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/mars/" target="_self" title="Mars Facts">Mars Facts</a> <span class="wpp-meta post-stats"></span></li>
    <li><a href="https://space-facts.com/jupiter/" target="_self" title="Jupiter Facts"><img alt="Jupiter Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/8-first_image-20x20.png" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/jupiter/" target="_self" title="Jupiter Facts">Jupiter Facts</a> <span class="wpp-meta post-stats"></span></li>
    <li><a href="https://space-facts.com/uranus/" target="_self" title="Uranus Facts"><img alt="Uranus Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/314-first_image-20x20.jpg" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/uranus/" target="_self" title="Uranus Facts">Uranus Facts</a> <span class="wpp-meta post-stats"></span></li>
    <li><a href="https://space-facts.com/venus/" target="_self" title="Venus Facts"><img alt="Venus Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/238-first_image-20x20.png" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/venus/" target="_self" title="Venus Facts">Venus Facts</a> <span class="wpp-meta post-stats"></span></li>
    <li><a href="https://space-facts.com/saturn/" target="_self" title="Saturn Facts"><img alt="Saturn Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/261-first_image-20x20.png" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/saturn/" target="_self" title="Saturn Facts">Saturn Facts</a> <span class="wpp-meta post-stats"></span></li>
    <li><a href="https://space-facts.com/neptune/" target="_self" title="Neptune Facts"><img alt="Neptune Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/191-first_image-20x20.png" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/neptune/" target="_self" title="Neptune Facts">Neptune Facts</a> <span class="wpp-meta post-stats"></span></li>
    </ul>
    <ul class="wpp-list">
    <li><a href="https://space-facts.com/mars-curiosity-facts/" target="_self" title="Mars Curiosity Facts"><img alt="Mars Curiosity Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/749-first_image-20x20.jpg" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/mars-curiosity-facts/" target="_self" title="Mars Curiosity Facts">Mars Curiosit...</a> <span class="wpp-meta post-stats"></span></li>
    <li><a href="https://space-facts.com/solar-system-information/" target="_self" title="Solar System Planets &amp; Dwarf Planets Information Chart"><img alt="Solar System Planets &amp; Dwarf Planets Information Chart" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/1380-first_image-20x20.png" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/solar-system-information/" target="_self" title="Solar System Planets &amp; Dwarf Planets Information Chart">Solar System...</a> <span class="wpp-meta post-stats"></span></li>
    <li><a href="https://space-facts.com/films-set-on-other-planets/" target="_self" title="The Ultimate List of Films Set in Space or on Other Planets"><img alt="The Ultimate List of Films Set in Space or on Other Planets" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/1200-first_image-20x20.jpg" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/films-set-on-other-planets/" target="_self" title="The Ultimate List of Films Set in Space or on Other Planets">The Ultimate...</a> <span class="wpp-meta post-stats"></span></li>
    <li><a href="https://space-facts.com/the-moon/" target="_self" title="Moon Facts"><img alt="Moon Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/576-first_image-20x20.png" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/the-moon/" target="_self" title="Moon Facts">Moon Facts</a> <span class="wpp-meta post-stats"></span></li>
    <li><a href="https://space-facts.com/the-sun/" target="_self" title="Sun Facts"><img alt="Sun Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/504-first_image-20x20.jpg" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/the-sun/" target="_self" title="Sun Facts">Sun Facts</a> <span class="wpp-meta post-stats"></span></li>
    <li><a href="https://space-facts.com/orbital-periods-planets/" target="_self" title="Orbital Periods of the Planets"><img alt="Orbital Periods of the Planets" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/2386-first_image-20x20.png" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/orbital-periods-planets/" target="_self" title="Orbital Periods of the Planets">Orbital Perio...</a> <span class="wpp-meta post-stats"></span></li>
    <li><a href="https://space-facts.com/jupiters-galilean-moons-profile-gifs/" target="_self" title="Jupiter’s Galilean Moons (Profile Gifs)"><img alt="Jupiter's Galilean Moons (Profile Gifs)" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/5329-first_image-20x20.gif" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/jupiters-galilean-moons-profile-gifs/" target="_self" title="Jupiter’s Galilean Moons (Profile Gifs)">Jupiter’...</a> <span class="wpp-meta post-stats"></span></li>
    <li><a href="https://space-facts.com/pluto/" target="_self" title="Pluto Facts"><img alt="Pluto Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/1250-first_image-20x20.png" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/pluto/" target="_self" title="Pluto Facts">Pluto Facts</a> <span class="wpp-meta post-stats"></span></li>
    </ul></div></div></div></div><div class="widget feature-posts" id="wpx-feature-posts-3"><h4 class="widgettitle">Blog</h4><ul class="feature-posts-list"><li><a class="feature-posts-title" href="https://space-facts.com/jupiters-galilean-moons-profile-gifs/">Jupiter’s Galilean Moons (Profile Gifs)</a> <br/><span class="post-excerpt">NASA’s Juno Spacecraft will arrive at Jupiter in the next few day after ...</span></li><li><a class="feature-posts-title" href="https://space-facts.com/planets-moons-star-wars/">The Planets and Moons of Star Wars to Scale</a> <br/><span class="post-excerpt">I like Star Wars, Star Wars is set in space, my website is about space, hence I ...</span></li><li><a class="feature-posts-title" href="https://space-facts.com/planet-orbits/">Planet Orbits</a> <br/><span class="post-excerpt">An orbit is the path an object takes in space as it revolves around another ...</span></li><li><a class="feature-posts-title" href="https://space-facts.com/pluto-information-infographic/">Pluto Size, Composition, Distance from Sun &amp; Moons</a> <br/><span class="post-excerpt">Size: The New Horizons mission has verified that Pluto is the largest of the ...</span></li><li><a class="feature-posts-title" href="https://space-facts.com/new-horizons-spacecraft-mission/">New Horizons Mission &amp; Spacecraft Facts</a> <br/><span class="post-excerpt">NASA’s New Horizons spacecraft is on a mission to collect data and ...</span></li></ul></div></div></aside></div></div></div><div id="footerwrap">
    <footer class="pagewidth clearfix" id="footer">
    <div class="footer-widgets pagewidth clearfix">
    <div class="col col3-1 first">
    <div class="widget widget_text" id="text-40"><h4 class="widgettitle">Planets</h4> <div class="textwidget"><div class="link-box">
    <ul class="wpp-list">
    <li><a href="https://space-facts.com/mercury/" target="_self" title="Mercury Facts"><img alt="Mercury Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/216-first_image-20x20.png" title="Mercury Facts" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/mercury/" target="_self" title="Mercury Facts">Mercury</a> </li>
    <li><a href="https://space-facts.com/venus/" target="_self" title="Venus Facts"><img alt="Venus Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/238-first_image-20x20.png" title="Venus Facts" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/venus/" target="_self" title="Venus Facts">Venus</a> </li>
    <li><a href="https://space-facts.com/earth/" target="_self" title="Earth Facts"><img alt="Earth Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/270-first_image-20x20.png" title="Earth Facts" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/earth/" target="_self" title="Earth Facts">Earth</a> </li>
    <li><a href="https://space-facts.com/mars/" target="_self" title="Mars Facts"><img alt="Mars Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/17-first_image-20x20.jpg" title="Mars Facts" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/mars/" target="_self" title="Mars Facts">Mars</a> </li>
    </ul></div><div class="link-box"> <ul class="wpp-list"> <li><a href="https://space-facts.com/jupiter/" target="_self" title="Jupiter Facts"><img alt="Jupiter Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/8-first_image-20x20.png" title="Jupiter Facts" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/jupiter/" target="_self" title="Jupiter Facts">Jupiter</a> </li> <li><a href="https://space-facts.com/saturn/" target="_self" title="Saturn Facts"><img alt="Saturn Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/261-first_image-20x20.png" title="Saturn Facts" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/saturn/" target="_self" title="Saturn Facts">Saturn</a> </li> <li><a href="https://space-facts.com/uranus/" target="_self" title="Uranus Facts"><img alt="Uranus Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/314-first_image-20x20.jpg" title="Uranus Facts" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/uranus/" target="_self" title="Uranus Facts">Uranus</a> </li> <li><a href="https://space-facts.com/neptune/" target="_self" title="Neptune Facts"><img alt="Neptune Facts" class="wpp-thumbnail wpp_cached_thumb wpp_first_image" height="20" src="https://space-facts.com/wp-content/uploads/wordpress-popular-posts/191-first_image-20x20.png" title="Neptune Facts" width="20"/></a> <a class="wpp-post-title" href="https://space-facts.com/neptune/" target="_self" title="Neptune Facts">Neptune</a> </li> </ul></div></div></div></div><div class="col col3-1">
    <div class="widget widget_tumblr_recent_photos" id="tumblr-recent-photos"><h4 class="widgettitle">Space Tumblr</h4><div id="tumblr_recent_photos"><ul><a href="http://space-facts.tumblr.com/post/157654119490" target="_blank"><img alt="http://space-facts.tumblr.com/post/157654119490" border="0" src="https://78.media.tumblr.com/087bab04575662fb8a6f3234232c5e2e/tumblr_olvr9h19W31rkd9uho1_75sq.jpg" style="float:center; margin-right:12px; margin-bottom:8px;"/></a><a href="http://space-facts.tumblr.com/post/146912434420" target="_blank"><img alt="http://space-facts.tumblr.com/post/146912434420" border="0" src="https://78.media.tumblr.com/409d8fddf5a9d638e02fe61aaee6cfe4/tumblr_o9sipilZHq1rxrsvso1_75sq.gif" style="float:center; margin-right:12px; margin-bottom:8px;"/></a><a href="http://space-facts.tumblr.com/post/143548308471" target="_blank"><img alt="http://space-facts.tumblr.com/post/143548308471" border="0" src="https://78.media.tumblr.com/feb83e3ee88b0cbd5efd43cca22836e7/tumblr_o6chhsTN6Z1rxrsvso2_75sq.jpg" style="float:center; margin-right:12px; margin-bottom:8px;"/></a><a href="http://space-facts.tumblr.com/post/143390787920" target="_blank"><img alt="http://space-facts.tumblr.com/post/143390787920" border="0" src="https://78.media.tumblr.com/10bda20f5be4f0f998a5bdbfd0bd39a4/tumblr_nny13ciZYn1rxrsvso3_75sq.jpg" style="float:center; margin-right:12px; margin-bottom:8px;"/></a><a href="http://space-facts.tumblr.com/post/139870991040" target="_blank"><img alt="http://space-facts.tumblr.com/post/139870991040" border="0" src="https://78.media.tumblr.com/9a8aa967537903e2e92ef257ce368fdf/tumblr_o2st0t7kle1rxrsvso10_75sq.png" style="float:center; margin-right:12px; margin-bottom:8px;"/></a><a href="http://space-facts.tumblr.com/post/139557997445" target="_blank"><img alt="http://space-facts.tumblr.com/post/139557997445" border="0" src="https://78.media.tumblr.com/d1f2b3fbcb2108f0be21b31024cb99e7/tumblr_o2revwudcW1rxrsvso1_75sq.gif" style="float:center; margin-right:12px; margin-bottom:8px;"/></a><a href="http://space-facts.tumblr.com/post/135003045958" target="_blank"><img alt="http://space-facts.tumblr.com/post/135003045958" border="0" src="https://78.media.tumblr.com/d133b97db3ebf5cafcd41d099fdedd81/tumblr_nz4ysymELZ1rxrsvso3_r1_75sq.png" style="float:center; margin-right:12px; margin-bottom:8px;"/></a><a href="http://space-facts.tumblr.com/post/124188493425" target="_blank"><img alt="http://space-facts.tumblr.com/post/124188493425" border="0" src="https://78.media.tumblr.com/62555b76c8744dc345de7153d739b12f/tumblr_nrjvgqOvzS1rxrsvso1_75sq.png" style="float:center; margin-right:12px; margin-bottom:8px;"/></a></ul></div></div></div><div class="col col3-1">
    <div class="widget widget_text" id="text-36"><h4 class="widgettitle">More</h4> <div class="textwidget"><div class="footer-links"> <p><a href="https://space-facts.com/blog/">Blog</a> - Space articles, diagrams and graphics</p> <p><a href="https://space-facts.com/faq/">FAQ</a> - Frequently asked questions about space</p> <p><a href="https://space-facts.com/posters/">Posters</a> - Posters about space and the planets</p></div></div></div><div class="widget widget_lsi_widget" id="lsi_widget-2"><ul class="lsi-social-icons icon-set-lsi_widget-2"><li class="lsi-social-twitter"><a href="https://twitter.com/_SpaceFacts" rel="nofollow" target="_blank" title="Twitter"><i class="lsicon lsicon-twitter"></i></a></li><li class="lsi-social-facebook"><a href="https://www.facebook.com/spacefact" rel="nofollow" target="_blank" title="Facebook"><i class="lsicon lsicon-facebook"></i></a></li><li class="lsi-social-gplus"><a href="https://plus.google.com/+Spacefacts1/posts" rel="nofollow" target="_blank" title="Google+"><i class="lsicon lsicon-gplus"></i></a></li><li class="lsi-social-pinterest"><a href="http://www.pinterest.com/spacefacts/" rel="nofollow" target="_blank" title="Pinterest"><i class="lsicon lsicon-pinterest"></i></a></li><li class="lsi-social-tumblr"><a href="http://space-facts.tumblr.com/" rel="nofollow" target="_blank" title="Tumblr"><i class="lsicon lsicon-tumblr"></i></a></li><li class="lsi-social-rss"><a href="https://space-facts.com/feed/" rel="nofollow" target="_blank" title="RSS"><i class="lsicon lsicon-rss"></i></a></li></ul></div></div></div></footer></div><div class="footwidth" id="footerwraptext">
    <div class="pagewidth">
    <div class="footer-text clearfix">
    © <a href="https://space-facts.com">Space Facts</a> 2018
    | <a href="https://space-facts.com/privacy-policy/">Privacy</a> | <a href="https://space-facts.com/about/">About</a> | <a href="https://space-facts.com/contact/">Contact</a>
    <script>(function(){
    var po=document.createElement('script'); po.type='text/javascript'; po.async=true;
    po.src='https://apis.google.com/js/plusone.js';
    var s=document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
    })();</script>
    <div style="display:none"></div><script>window.WPCOM_sharing_counts={"https:\/\/space-facts.com\/mars\/":17};</script>
    <link href="//space-facts.com/wp-content/cache/wpfc-minified/f8fcaee0e0437125c2d9f601a7259067/1518688589index.css" media="all" rel="stylesheet" type="text/css"/>
    <style id="lsi-style-inline-css">.icon-set-lsi_widget-2{text-align:left !important;}
    .icon-set-lsi_widget-2 a, 
    .icon-set-lsi_widget-2 a:visited, 
    .icon-set-lsi_widget-2 a:focus{border-radius:2px;background:#000000 !important;color:#FFFFFF !important;font-size:20px !important;}
    .icon-set-lsi_widget-2 a:hover{background:#cc3d00 !important;color:#FFFFFF !important;}
    .lsi-social-twitter a:hover{background:#55ACEE !important;}
    .lsi-social-facebook a:hover{background:#3b5998 !important;}
    .lsi-social-gplus a:hover{background:#dd4b39 !important;}
    .lsi-social-pinterest a:hover{background:#ce2029 !important;}
    .lsi-social-tumblr a:hover{background:#35465c !important;}
    .lsi-social-rss a:hover{background:#2bb24c !important;}</style>
    <script src="https://s0.wp.com/wp-content/js/devicepx-jetpack.js?ver=201807"></script>
    <script>
    var mPS2id_params={"instances":{"mPS2id_instance_0":{"selector":"a[rel='m_PageScroll2id']","autoSelectorMenuLinks":"false","scrollSpeed":3000,"autoScrollSpeed":"true","scrollEasing":"easeInOutExpo","scrollingEasing":"easeInOutCirc","pageEndSmoothScroll":"true","stopScrollOnUserAction":"false","layout":"vertical","offset":0,"highlightSelector":"","clickedClass":"mPS2id-clicked","targetClass":"mPS2id-target","highlightClass":"mPS2id-highlight","forceSingleHighlight":"false","keepHighlightUntilNext":"false","highlightByNextTarget":"false","appendHash":"false","scrollToHash":"false","scrollToHashForAll":"false","scrollToHashDelay":0,"disablePluginBelow":0,"adminDisplayWidgetsId":"true","adminTinyMCEbuttons":"true","unbindUnrelatedClickEvents":"false","normalizeAnchorPointTargets":"false"}},"total_instances":"1","shortcode_class":"_ps2id"};
    </script>
    <script src="//space-facts.com/wp-content/cache/wpfc-minified/e7f1a84ac5e30e1d03c940bebc358c1d/1518688582index.js"></script>
    <script>
    var ctcc_vars={"expiry":"30","method":"1","version":"1"};
    </script>
    <script src="//space-facts.com/wp-content/cache/wpfc-minified/e9ccc251c0a0a7cf741e4fab2037737e/1518688582index.js"></script>
    <script src="https://space-facts.com/wp-includes/js/comment-reply.min.js?ver=4.9.4"></script>
    <script src="https://space-facts.com/wp-includes/js/wp-embed.min.js?ver=4.9.4"></script>
    <script>
    var sharing_js_options={"lang":"en","counts":"1"};
    </script>
    <script src="//space-facts.com/wp-content/cache/wpfc-minified/27d86dcf3f53b39f9f97ea2811941138/1518688589index.js"></script>
    <script>var windowOpen;
    jQuery(document.body).on('click', 'a.share-twitter', function(){
    if('undefined'!==typeof windowOpen){
    windowOpen.close();
    }
    windowOpen=window.open(jQuery(this).attr('href'), 'wpcomtwitter', 'menubar=1,resizable=1,width=600,height=350');
    return false;
    });
    var windowOpen;
    jQuery(document.body).on('click', 'a.share-facebook', function(){
    if('undefined'!==typeof windowOpen){
    windowOpen.close();
    }
    windowOpen=window.open(jQuery(this).attr('href'), 'wpcomfacebook', 'menubar=1,resizable=1,width=600,height=400');
    return false;
    });
    var windowOpen;
    jQuery(document.body).on('click', 'a.share-google-plus-1', function(){
    if('undefined'!==typeof windowOpen){
    windowOpen.close();
    }
    windowOpen=window.open(jQuery(this).attr('href'), 'wpcomgoogle-plus-1', 'menubar=1,resizable=1,width=480,height=550');
    return false;
    });</script>
    <script async="" defer="" src="https://stats.wp.com/e-201807.js"></script>
    <script>_stq=window._stq||[];
    _stq.push([ 'view', {v:'ext',j:'1:5.7.1',blog:'37359843',post:'17',tz:'0',srv:'space-facts.com'} ]);
    _stq.push([ 'clickTrackerInit', '37359843', '17' ]);</script>
    <script>jQuery(document).ready(function($){
    if(!catapultReadCookie("catAccCookies")){
    $("html").addClass("has-cookie-bar");
    $("html").addClass("cookie-bar-bottom-bar");
    $("html").addClass("cookie-bar-bar");
    }
    ctccFirstPage();
    });</script>
    <div id="catapult-cookie-bar"><div class="ctcc-inner"><span class="ctcc-left-side">We use cookies to personalise content and ads and to improve your browsing experience. <a class="ctcc-more-info-link" href="https://space-facts.com/privacy-policy/" tabindex="0" target="_blank">More info.</a></span><span class="ctcc-right-side"><button id="catapultCookie" onclick="catapultAcceptCookies();" tabindex="0">Okay, thanks</button></span></div></div></div></div></div><iframe aria-hidden="true" id="oauth2relay325109623" name="oauth2relay325109623" src="https://accounts.google.com/o/oauth2/postmessageRelay?parent=https%3A%2F%2Fspace-facts.com&amp;jsh=m%3B%2F_%2Fscs%2Fapps-static%2F_%2Fjs%2Fk%3Doz.gapi.en_US.9Iv2zI3hhA4.O%2Fm%3D__features__%2Fam%3DAQE%2Frt%3Dj%2Fd%3D1%2Frs%3DAGLTcCMpvfgYHgs56VN-05ik_fHHjzO8Cg#rpctoken=1915397321&amp;forcesecure=1" style="width: 1px; height: 1px; position: absolute; top: -100px;" tabindex="-1"></iframe><img alt=":)" height="5" id="wpstats" src="https://pixel.wp.com/g.gif?v=ext&amp;j=1%3A5.7.1&amp;blog=37359843&amp;post=17&amp;tz=0&amp;srv=space-facts.com&amp;host=space-facts.com&amp;ref=&amp;rand=0.01000218205137271" width="6"/><div style="display: block; margin: 0px; padding: 0px; width: 15px; height: 31px; z-index: 2147483647; position: absolute; left: 980px; top: 498px;"><iframe allowtransparency="true" class="goog_xca_frame" frameborder="0" hspace="0" marginheight="0" marginwidth="0" scrolling="no" style="opacity: 1; transition: opacity 0.3s linear; margin: 0px; padding: 0px; width: 15px; height: 31px; z-index: 2147483647; display: block; position: relative; float: right;" vspace="0"></iframe></div></body></html><!-- WP Fastest Cache file was created in 3.85910105705 seconds, on 15-02-18 9:57:46 -->




```python
#get the entire table
table_data = soup.find('table', class_="tablepress tablepress-id-mars")
```


```python
#find all instances of table row
table_all = table_data.find_all('tr')

#set up lists to hold td elements which alternate between label and value
labels = []
values = []

#for each tr element append the first td element to labels and the second to values
for tr in table_all:
    td_elements = tr.find_all('td')
    labels.append(td_elements[0].text)
    values.append(td_elements[1].text)
```


```python
#make a data frame and view
mars_facts_df = pd.DataFrame({
    "Label": labels,
    "Values": values
})
```


```python
mars_facts_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Label</th>
      <th>Values</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Equatorial Diameter:</td>
      <td>6,792 km\n</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Polar Diameter:</td>
      <td>6,752 km\n</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mass:</td>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Moons:</td>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Orbit Distance:</td>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Orbit Period:</td>
      <td>687 days (1.9 years)\n</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Surface Temperature:</td>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>7</th>
      <td>First Record:</td>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Recorded By:</td>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
# get html code for DataFrame
fact_table = mars_facts_df.to_html(header = False, index = False)
fact_table
```




    '<table border="1" class="dataframe">\n  <tbody>\n    <tr>\n      <td>Equatorial Diameter:</td>\n      <td>6,792 km\\n</td>\n    </tr>\n    <tr>\n      <td>Polar Diameter:</td>\n      <td>6,752 km\\n</td>\n    </tr>\n    <tr>\n      <td>Mass:</td>\n      <td>6.42 x 10^23 kg (10.7% Earth)</td>\n    </tr>\n    <tr>\n      <td>Moons:</td>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <td>Orbit Distance:</td>\n      <td>227,943,824 km (1.52 AU)</td>\n    </tr>\n    <tr>\n      <td>Orbit Period:</td>\n      <td>687 days (1.9 years)\\n</td>\n    </tr>\n    <tr>\n      <td>Surface Temperature:</td>\n      <td>-153 to 20 °C</td>\n    </tr>\n    <tr>\n      <td>First Record:</td>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <td>Recorded By:</td>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>'



## Mars Hemispheres


```python
# new url
usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

browser.visit(usgs_url)

usgs_html = browser.html

soup = BeautifulSoup(usgs_html, "html.parser")

# gets class holding hemisphere picture
items = soup.find("div",{"class":"collapsible results"}).find_all("div",{"class":"item"})

#setup list to hold dictionaries
hemisphere_image_urls =[]

for item in items:
    img_main_url = "https://astrogeology.usgs.gov"+item.find("a")["href"]
    img_title = item.find("div",{"class":"description"}).find("a").find("h3").text
    browser.visit(img_main_url)
    time.sleep(2)
    img_soup = BeautifulSoup(browser.html,"html.parser")
    download_item = img_soup.find("div",{"class":"downloads"})
    hemisphere_item = {
    "title":img_title,
    "img_url": download_item.find("li").find("a")["href"]
    }
    hemisphere_image_urls.append(hemisphere_item)

print(hemisphere_image_urls)
        
```

    [{'title': 'Cerberus Hemisphere Enhanced', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'}, {'title': 'Schiaparelli Hemisphere Enhanced', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'}, {'title': 'Syrtis Major Hemisphere Enhanced', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}, {'title': 'Valles Marineris Hemisphere Enhanced', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]
    