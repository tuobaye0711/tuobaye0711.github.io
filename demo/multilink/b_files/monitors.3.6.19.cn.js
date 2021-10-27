var monitors=function(t){"use strict";var D=function(){return(D=Object.assign||function(t){for(var n,e=1,r=arguments.length;e<r;e++)for(var o in n=arguments[e])Object.prototype.hasOwnProperty.call(n,o)&&(t[o]=n[o]);return t}).apply(this,arguments)};function k(t){var n="function"==typeof Symbol&&Symbol.iterator,e=n&&t[n],r=0;if(e)return e.call(t);if(t&&"number"==typeof t.length)return{next:function(){return{value:(t=t&&r>=t.length?void 0:t)&&t[r++],done:!t}}};throw new TypeError(n?"Object is not iterable.":"Symbol.iterator is not defined.")}function H(t,n){var e="function"==typeof Symbol&&t[Symbol.iterator];if(!e)return t;var r,o,i=e.call(t),a=[];try{for(;(void 0===n||0<n--)&&!(r=i.next()).done;)a.push(r.value)}catch(t){o={error:t}}finally{try{r&&!r.done&&(e=i.return)&&e.call(i)}finally{if(o)throw o.error}}return a}function c(){for(var t=[],n=0;n<arguments.length;n++)t=t.concat(H(arguments[n]));return t}function a(t){return"object"==typeof t&&null!==t&&!i(t)}function r(t){return"[object Object]"===(t=t,Object.prototype.toString.call(t))}function h(t){return"function"==typeof t}function s(t){return"[object String]"===Object.prototype.toString.call(t)}function i(t){return"[object Array]"===Object.prototype.toString.call(t)}function u(t){return"number"==typeof t}function n(t,n){if(a(t))for(var e in t)r=t,o=e,Object.prototype.hasOwnProperty.call(r,o)&&n.call(null,e,t[e]);var r,o}function o(){return a(window)&&!!a(window.performance)}function e(){return!(!h(requestAnimationFrame)||!h(cancelAnimationFrame))}function f(){return!(!window.setTimeout||!h(setTimeout))}function l(t){var e,t=function(t){if(!a(t))return{};var e={};return n(t,function(t,n){a(n)||i(n)?e[t]=JSON.stringify(n):e[t]=n}),e}(t),t=(e={},n(t,function(t,n){e[encodeURIComponent(t)]=encodeURIComponent(n)}),e),r=[];return n(t,function(t,n){r.push(t+"="+n)}),r.join("&")}function m(t){var n=document.createElement("a");n.href=t;t=n.pathname||"/";return"/"!==t[0]&&(t="/"+t),{href:n.href,protocol:n.protocol.slice(0,-1),hostname:n.hostname,host:n.host,search:n.search,pathname:t,hash:n.hash}}function g(){}function B(t){"complete"!==document.readyState?window.addEventListener("load",function(){setTimeout(function(){t()},0)},!1):t()}function U(n,e){h(n)&&(h(window.addEventListener)&&(window.addEventListener("unload",n),window.addEventListener("beforeunload",n),window.addEventListener("pagehide",n)),h(document.addEventListener)&&document.addEventListener("visibilitychange",function(t){h(e)?e(t):"hidden"===document.visibilityState&&n(t)}))}function d(){return(new Date).getTime()}var p=(v.post=function(t,n,e){var r=e&&e.success||g,o=e&&e.fail||g,e=new XMLHttpRequest;e.open("POST",t,!0),e.setRequestHeader("Content-Type","application/json"),e.send(JSON.stringify(n)),e.onload=function(){try{var t;this.responseText?(t=JSON.parse(this.responseText),r(t)):r({})}catch(t){o()}},e.onerror=function(){o()},e.onabort=function(){o()}},v.get=function(t,n){var e=n&&n.success||g,r=n&&n.fail||g,o=n&&n.getResponse||g,i=n&&n.getResponseText||g,a=new XMLHttpRequest;n&&n.withCredentials&&(a.withCredentials=n.withCredentials),a.open("GET",t),a.send(),a.onload=function(){o(null==this?void 0:this.response),i(this.responseText);try{var t;this.responseText?(t=JSON.parse(this.responseText),e(t)):e({})}catch(t){r()}},a.onerror=function(){r()},a.onabort=function(){r()}},v.prototype.getCommonParams=function(){return{timestamp:Date.now()}},v);function v(t){var n=this;this.postEvent=function(t){t=D(D({},t),n.getCommonParams());v.post(n.url,t)},this.getEvent=function(t){t=l(D(D({},t),n.getCommonParams())),t=n.url+"?"+t;v.get(t)},this.getURL=function(){return n.url},this.options=t,this.url=this.options.reportURL}function q(n){return function(t){return n===t}}function Q(t){return t}function y(){return h(Date)?Math.round(Date.now()/1e3):0}function b(t,e){if(!a(t))return{};if(!h(e))return{};var r={};return n(t,function(t,n){e(n)&&(r[t]=n)}),r}function w(t){var n,e,r,o,i=null;return a(t)?("timer"===t.type&&(i=a(n=t.event)&&s(n.name)&&u(n.value)?{metrics_type:"timer",event_name:"default",metrics:((e={})[n.name]=n.value,e),category:b(n.tags,s),timestamp:y()}:{}),"counter"===t.type&&(i=a(o=t.event)&&s(o.name)&&u(o.value)?{metrics_type:"counter",event_name:"default",metrics:((r={})[o.name]=o.value,r),category:b(o.tags,s),timestamp:y()}:{}),"log"===t.type&&(i=a(r=t.event)&&s(r.value)?{metrics_type:"log",event_name:"default",log_content:r.value,log_level:null!==(o=r.level)&&void 0!==o?o:"info",category:b(r.tags,s),timestamp:y()}:{}),i="custom"===t.type?a(t=t.event)&&s(t.event_name)?{metrics_type:"custom",event_name:t.event_name,metrics:b(t.metrics,u),category:b(t.tags,s),timestamp:y()}:{}:i):i}function z(r){var o=function(){for(var t=[],n=0;n<arguments.length;n++)t[n]=arguments[n];var e=r.apply(void 0,c(t));return o.returns=e,o.resolved=!0,o.subs&&o.subs.forEach(function(t){return t()}),e};return o.then=G(o).then,o}var G=function(){for(var n=[],t=0;t<arguments.length;t++)n[t]=arguments[t];function a(){return n.every(function(t){return t.resolved})}return Object.defineProperty({then:function(e){function r(){return t.apply(void 0,c(n.map(function(t){return t.returns})))}var o,i,t=z(function(){for(var t=[],n=0;n<arguments.length;n++)t[n]=arguments[n];return i?o:(i=!0,o=e.apply(void 0,c(t)))});return a()?setTimeout(r):n.forEach(function(t){function n(){return a()&&r()}t.subs?t.subs.push(n):t.subs=[n]}),G(t)}},"resolved",{get:a})};function T(){try{return new Headers,new Request(""),new Response,window.fetch}catch(t){}}function _(){if(a(window))return window}function S(){if(a(document))return document}function C(){if(_()&&a(window.performance))return window.performance}function R(){if(_()&&h(window.MutationObserver))return window.MutationObserver}function x(){if(_()&&h(window.PerformanceObserver))return window.PerformanceObserver}function A(i,a,u){return function(){for(var t=[],n=0;n<arguments.length;n++)t[n]=arguments[n];if(!i)return g;var e=i[a],r=u.apply(void 0,c([e],t)),o=r;return h(o)&&(o=function(){for(var n=[],t=0;t<arguments.length;t++)n[t]=arguments[t];try{return r.apply(this,n)}catch(t){return h(e)&&e.apply(this,n)}}),i[a]=o,function(t){t&&o!==i[a]||(i[a]=e)}}}function V(t,n,e,r){void 0===n&&(n={}),void 0===r&&(r=[]);try{var o=t.apply(void 0,c(r));return o&&o(n,e)||[]}catch(t){return[]}}function L(t,n){var e=t&&new t(n);return[function(t,n){e&&t&&e.observe(t,n)},function(){return e&&e.disconnect()}]}function N(e,o,n,i){var r=e&&new e(function(t,r){t.getEntries?t.getEntries().forEach(function(t,n,e){return o(t,n,e,r)}):i&&i(),n&&r.disconnect()});return[function(){for(var n=[],t=0;t<arguments.length;t++)n[t]=arguments[t];if(!e||!r)return i&&i();try{n.forEach(function(t){-1<e.supportedEntryTypes.indexOf(t)&&r.observe({type:t,buffered:!0})})}catch(t){try{r.observe({entryTypes:n})}catch(t){}}},function(){return r&&r.disconnect()}]}function W(e){var t=e&&e.timing||void 0;return[t,function(){return e&&e.now?e.now():(Date.now?Date.now():+new Date)-(t&&t.navigationStart||0)},function(t){var n=(e||{}).getEntriesByType;return h(n)&&n.call(e,t)||[]},function(){var t=(e||{}).clearResourceTimings;h(t)&&t.call(e)},function(t){var n=(e||{}).getEntriesByName;return h(n)&&n.call(e,t)||[]}]}function X(d,p,v){var t;return void 0===d&&(d=S()),void 0===p&&(p=R()),void 0===v&&(v=null===(t=function(){var t=C();if(t&&a(t.timing))return t.timing}())||void 0===t?void 0:t.navigationStart),function(t,r){function n(){return u.push({time:Date.now()-a,score:M(d&&d.body,1,!1,s)})}var e,o,i,a=Date.now(),u=[],s=E.concat(t.ignoreTags||[]),c=H((f=!0,l=window.requestAnimationFrame,t=window.cancelAnimationFrame,o=!h(l)||f&&document&&document.hidden?function(t){return t(0),0}:l,i=h(t)?t:g,[function(t){e&&i(e),e=o(t)},o,i]),1)[0],f=H(L(p,function(){return c(n)}),2),l=f[0],m=f[1],t=function(t){void 0===t&&(t=0),m();var n,e,n=(n=(e=H(void 0===(n=u)?[]:n))[0],(e=e.slice(1))&&e.reduce(function(t,n){var e=H(t,2),r=e[0],t=e[1],e=n.score-r.score;return[n,n.time>=r.time&&t.rate<e?{time:n.time,rate:e}:t]},[n,{time:null==n?void 0:n.time,rate:0}])[1].time||0),t={name:"FMPMonitor",type:"post",event:{ev_type:"fmp",fmp:n?n+t:0}};return r&&r(t),t},f=a-(v||0);return l(d,{subtree:!0,childList:!0}),[m,t,t.bind(null,f)]}}function I(n){function e(){return window.clearTimeout(a)}function r(t){t<i||!o||(e(),a=window.setTimeout(o,t-n()),i=t)}var o,i=-1/0,a=void 0;return[function(t,n){o=t,r(n)},function(){e(),o=void 0},r]}function O(t,a){var u=["img","script","iframe","link","audio","video","source"],n=(t=H(L(t,function(t){var n,e;try{for(var r=k(t),o=r.next();!o.done;o=r.next()){var i=o.value;("childList"===i.type&&function t(n,e){var r,o;try{for(var i=k(n),a=i.next();!a.done;a=i.next()){var u=a.value;if(e.includes(u.nodeName.toLowerCase())||u.children&&t(u.children,e))return 1}}catch(t){r={error:t}}finally{try{a&&!a.done&&(o=i.return)&&o.call(i)}finally{if(r)throw r.error}}}(i.addedNodes,u)||"attributes"===i.type&&u.includes(i.target.nodeName.toLowerCase()))&&a(i)}}catch(t){n={error:t}}finally{try{o&&!o.done&&(e=r.return)&&e.call(r)}finally{if(n)throw n.error}}}),2))[0];return[function(){return n(document,{attributes:!0,childList:!0,subtree:!0,attributeFilter:["href","src"]})},t[1]]}function F(t){var t=(n=t||{}).domContentLoadedEventEnd,n=n.navigationStart;return t?t-(void 0===n?0:n):null}function P(e){return function(){for(var t=[],n=0;n<arguments.length;n++)t[n]=arguments[n];return this._method=t[0],e.apply(this,t)}}function j(r,o,i){var a=0;return function(){for(var t=[],n=0;n<arguments.length;n++)t[n]=arguments[n];if("GET"!==this._method)return r.apply(this,t);var e=a+=2;return o(e,Date.now()),A(this,"onreadystatechange",function(n){return function(t){n&&n.call(this,t),4===this.readyState&&i(e)}})(),r.apply(this,t)}}function J(i,a,u){var s=1;return function(){for(var t,o=[],n=0;n<arguments.length;n++)o[n]=arguments[n];return"GET"!==((null===(t=o[0])||void 0===t?void 0:t.method)||(null===(t=o[1])||void 0===t?void 0:t.method)||"GET")?i.apply(void 0,c(o)):new Promise(function(n,e){var r=s+=2;a(r,Date.now()),i.apply(void 0,c(o)).then(function(t){u(r),n(t)},function(t){u(r,t),e(t)})})}}function Y(E,M,T,_){return function(t,n,e,r){var s,c,o,i,a,u,f,l,m,d=H([s=[],c=[],function(a,u){return function(t){var n=t.startTime,e=t.duration,r=t.fetchStart,o=t.responseEnd,i=t.entryType;"longtask"===i?(s.push({start:n,end:n+e}),a&&a(t)):"resource"===i&&(c.push({start:r,end:o}),u&&u(t))}}],3),p=d[0],v=d[1],h=d[2],g=H((o=E,i=M,u=H([a={},function(t,n){return a[t]=n},function(t){return delete a[t]}],3),g=u[0],d=u[1],u=u[2],f=i&&A(i.prototype,"open",P)(),l=i&&A(i.prototype,"send",j)(d,u),m=o&&A(o,"fetch",J)(d,u),[g,function(){f&&f(!0),l&&l(!0),m&&m(!0)}]),2),y=g[0],b=g[1],g=H(t&&O(_,function(){return e(r()+5e3)})||[],2),t=g[0],w=g[1];t&&t();function S(){return function(t,n,e){var r,o,i,a;if(2<t.length)return e();var u=[];try{for(var s=k(n),c=s.next();!c.done;c=s.next()){var f=c.value;u.push([f.start,0],[f.end,1])}}catch(t){r={error:t}}finally{try{c&&!c.done&&(o=s.return)&&o.call(s)}finally{if(r)throw r.error}}try{for(var l=k(t),m=l.next();!m.done;m=l.next()){var d=m.value;u.push([d,0])}}catch(t){i={error:t}}finally{try{m&&!m.done&&(a=l.return)&&a.call(l)}finally{if(i)throw i.error}}u.sort(function(t,n){return t[0]-n[0]});for(var p=t.length,v=u.length-1;0<=v;v--){var h=H(u[v],2),g=h[0];switch(h[1]){case 0:p--;break;case 1:if(2<++p)return g}}return 0}(function(t){for(var n=Object.keys(t),e=[],r=0;r<n.length;r++){var o=t[n[r]];"number"==typeof o&&e.push(o)}return e}(y),v,r)}var g=H(N(T,h(function(t){var n=t.startTime,t=t.duration;return e(n+t+5e3)},function(){return e(S()+5e3)}),!1,function(){return p.notSupport=!0}),2),t=g[0],L=g[1];return t("longtask","resource"),n.forEach(h()),[p,function(){b(),L(),w&&w()},S]}}function K(w,S,L,E,M){return void 0===w&&(w=function(){if(h(XMLHttpRequest))return XMLHttpRequest}()),void 0===S&&(S=T()&&_()),void 0===L&&(L=x()),void 0===E&&(E=R()),void 0===M&&(M=C()),function(t,n,e){function r(t){var n=function(t,n,e,r,o){if(r-e<5e3)return null;o=0===o.length?t:o[o.length-1].end;return r-o<5e3?null:Math.max(o,n)}(((n=m("first-contentful-paint")[0])?n.startTime:F(f))||0,u||F(f)||0,y(),l()+(t?0:5e3),h);return t?n?(b(),void t(Math.round(n))):v(l()+1e3):(b(),n)}var o=t.useMutationObserver,i=t.preLongTaskObserver,a=t.isAsync,a=void 0===a?0:a,t=t.minValue,u=void 0===t?null:t,t=i||{},i=t.precollect,s=void 0===i?[]:i,c=t.observer,t=H(W(M),5),f=t[0],l=t[1],m=t[4],t=H(I(l),3),d=t[0],p=t[1],v=t[2],a=H(Y(S,w,L,E)(o,a?[]:s,v,l),3),h=a[0],g=a[1],y=a[2],b=function(){p(),g(),e&&e(),c&&c.disconnect(),s.length=0};return[function(t){if(h.notSupport)return t();var n=h[h.length-1];d(function(){return r(t)},Math.max(y()+5e3,n?n.end:0))},h,v,function(){return!h.notSupport&&r()||0}]}}var E=["SCRIPT","STYLE","META","HEAD"],M=function(t,e,n,r){if(!t||-1<r.indexOf(t.tagName))return 0;var o=t.children,o=void 0===o?[]:o,o=[].slice.call(o).reduceRight(function(t,n){return t+M(n,e+1,0<t,r)},0);if(o<=0&&!n){if(!h(t.getBoundingClientRect))return 0;n=t.getBoundingClientRect()||{},t=n.height;if(n.top>window.innerHeight||t<=0)return 0}return o+1+.5*e};function Z(){return Date.now()}var $=(tt.prototype.begin=function(){this.currentTime=Z(),this.beginTime=Z(),this.frames=0},tt.prototype.frame=function(){return this.currentTime=Z(),this.currentTime-this.beginTime},tt.prototype.end=function(){var t;return this.frames++,this.currentTime=Z(),this.currentTime>=this.beginTime+this.duration&&(t=this.frames*this.duration/(this.currentTime-this.beginTime),this.beginTime=this.currentTime,this.frames=0),t},tt);function tt(t){this.beginTime=Z(),this.frames=0,this.duration=null!=t?t:1e3,this.currentTime=Z()}var nt;(Dt=nt=nt||{}).once="once",Dt.repeat="repeat",Dt.frame="frame";var et="FPSMonitor",rt=(ot.prototype.setup=function(t){e()&&(this.fpsInstance=new $(1e3),this.callback=t||g,this.fpsInstance.begin(),this.mode!==nt.repeat?this.mode!==nt.frame?this.mode===nt.once&&this.animateOnce():this.animateId=requestAnimationFrame(this.animateFrame.bind(this)):this.animateRepeat())},ot.prototype.animateRepeat=function(){var t;e()&&(void 0!==(t=this.fpsInstance.end())&&(this.fpsList.push(t),this.sendFps(t)),this.animateId=requestAnimationFrame(this.animateRepeat))},ot.prototype.animateOnce=function(){if(e()){var t=this.fpsInstance.end();if(void 0!==t)return this.fpsList.push(t),this.sendFps(t),void(this.fpsList.length>=Math.floor(this.onceTime/1e3)&&cancelAnimationFrame(this.animateId));this.animateId=requestAnimationFrame(this.animateOnce)}},ot.prototype.animateFrame=function(){var t;!e()||void 0!==(t=this.fpsInstance.frame())&&(this.sendFrame(t),cancelAnimationFrame(this.animateId))},ot.prototype.sendFps=function(t){h(this.callback)&&this.callback({name:this.name,type:"post",event:{ev_type:"fps",fps:t}})},ot.prototype.sendFrame=function(t){h(this.callback)&&this.callback({name:this.name,type:"post",event:{ev_type:"frame_duration",frame:t}})},ot.monitorName=et,ot);function ot(t){var n,e=this;this.name=et,this.callback=g,this.fpsInstance=null,this.animateId=0,this.fpsList=[],this.mode="once",this.onceTime=1e3,this.getFps=function(){return e.fpsList},t&&(this.mode=null!==(n=t.mode)&&void 0!==n?n:nt.once,this.onceTime=null!==(t=t.onceTime)&&void 0!==t?t:1e3)}function it(t){try{for(var n,e=t,r=[],o=0,i=0,a=" > ".length;e&&o++<5&&!("html"===(n=function(t){var n,e,r,o,i=t,a=[];if(!i||!i.tagName)return"";a.push(i.tagName.toLowerCase()),i.id&&a.push("#"+i.id);t=i.className;if(t&&s(t))for(n=t.split(/\s+/),o=0;o<n.length;o++)a.push("."+n[o]);var u=["type","name","title","alt"];for(o=0;o<u.length;o++)e=u[o],(r=i.getAttribute(e))&&a.push("["+e+'="'+r+'"]');return a.join("")}(e))||1<o&&80<=i+r.length*a+n.length);)r.push(n),i+=n.length,e=e.parentNode;return r.reverse().join(" > ")}catch(t){return"<unknown>"}}var at="FPSJankTimesMonitor",ut=(st.prototype.setup=function(t){void 0===t&&(t=g),f()&&(this.callback=t,this.start())},st.prototype.getHistoryFrameList=function(){return this.historyFrameList},st.prototype.start=function(){this.fpsMonitor.setup(this.getFrameList.bind(this))},st.prototype.getFrameList=function(t){var n=this,e=t.event.frame,r=100<e,o=this.frameList.length,t={frame:e,isJank:r,timestamp:d()};this.historyFrameList.push(t),this.historyFrameList.length>(this.options.maxFrameListCount||30)&&this.historyFrameList.shift();e=this.frameList[o-1]||{},r=!t.isJank&&e.isJank,o=!t.isJank&&!e.isJank;t.isJank&&!e.isJank||r||t.isJank&&e.isJank?this.frameList.push(t):o&&(this.frameList=[t]),r&&(this.report(),this.frameList=[t]),this.timerId=window.setTimeout(function(){n.start()},100)},st.prototype.shouldReport=function(t){for(var n=0,e=0;e<t.length;e++){var r=t[e];if(200<r.frame)return!0;if(r.isJank&&n++,3<=n)return!0}return!1},st.prototype.report=function(){var t;this.shouldReport(this.frameList)&&(t={name:this.name,type:"post",event:{ev_type:"fps_jank_times",list:this.frameList,breadcrumbs:null!==(t=null===(t=this.breadcrumbMonitor)||void 0===t?void 0:t.getBreadcrumbs())&&void 0!==t?t:[],memory:null!==(t=null===(t=this.memoryRecordMonitor)||void 0===t?void 0:t.getMemoryQueue())&&void 0!==t?t:[]}},this.callback(t))},st.monitorName=at,st);function st(t){var e=this;this.name=at,this.historyFrameList=[],this.callback=g,this.onLeave=function(){var t,n;f()&&(1<e.frameList.length&&(e.report(),null!==(n=(t=e.options).report)&&void 0!==n&&n.call(t)),e.frameList=[],window.clearTimeout(e.timerId))},this.onShow=function(){f()&&(e.historyFrameList=[],e.frameList=[],e.start())},this.visibilityChange=function(){"hidden"===document.visibilityState&&e.onLeave(),"visible"===document.visibilityState&&e.onShow()},t.breadcrumbMonitor&&(this.breadcrumbMonitor=t.breadcrumbMonitor),t.memoryRecordMonitor&&(this.memoryRecordMonitor=t.memoryRecordMonitor),this.options=null!=t?t:{},this.fpsMonitor=new rt({mode:"frame"}),this.frameList=[],this.timerId=0,U(this.onLeave,this.visibilityChange)}function ct(n,o){return void 0===n&&(n=x()),void 0===o&&(o=C()),function(t,e){var r=H(W(o),3)[2];return(0,H(N(n,function(t){var n=t.processingStart,t=t.startTime;return e&&e({name:"FIDMonitor",fid:Math.round(n-t)})},!0),1)[0])(ht),[function(){var t=r(ht)[0]||{},n=t.processingStart,t=t.startTime;return t?Math.round(n-t):0}]}}function ft(a){return void 0===a&&(a=x()),function(t){var n=[],e=t.isAsync,r=t.preLongTaskObserver,o=H(N(a,function(t){return n.push(t)}),2),t=o[0],i=o[1];return!e&&r&&(r.precollect||[]).forEach(function(t){"longtask"===t.entryType&&n.push(t)}),t("longtask"),[function(){i();var t=n.reduce(function(t,n){n=n.duration;return t<n?n:t},0);return{name:"MPFIDMonitor",mpfid:Math.round(t)}}]}}function lt(n,t){return(t=t.filter(function(t){return t.name===n})[0])?Math.round(t.startTime):0}function mt(o,u){return void 0===o&&(o=x()),void 0===u&&(u=C()),function(t,i){function n(){var t=e("paint");return{fp:lt(yt,t),fcp:lt(gt,t)}}var a={},e=H(W(u),3)[2],r=n();return r.fcp&&r.fp?i&&i(r):(0,H(N(o,function(t,n,e,r){var o=t.name,t=t.startTime;a[o]=Math.round(t),a[yt]&&a[gt]&&(i&&i({fp:a[yt],fcp:a[gt]}),r.disconnect())},!1,function(){return i&&i(n())}),1)[0])("paint"),[n]}}function dt(t,n){var e=[];if(t.forEach(function(t){h(n)&&n(t)||e.push(t)}),e.length)return{name:"ResourcePerformanceMonitor",type:"post",event:{ev_type:"resource_performance",resources:e}}}function pt(s,c){return void 0===s&&(s=C()),void 0===c&&(c=x()),function(t,n){function r(t){(t=dt(t,a))&&n&&n(t)}function e(){return u("resource")}var o=(t=void 0===t?{}:t).isAsync,i=void 0===o?0:o,o=t.observe,o=void 0!==o&&o,a=t.checkIgnore,t=H(W(s),4),u=t[2],t=t[3];return i&&t(),o&&(r(e()),(0,H(N(c,function(t,n,e){return 0===n&&r(e)}),1)[0])("resource")),[function(){return dt(e())}]}}function vt(t){var n=D({},t);return[function(t){t=(n=t?D(D({},n),t):n).fmp;n.fmp=t?Math.max(Math.round(t),n.fcp||0):void 0},function(){return{name:wt,type:"post",event:n}},function(t){return n=D({},t)}]}var ht="first-input",gt="first-contentful-paint",yt="first-paint",bt={ev_type:"perf",isAsync:0,dns:0,tcp:0,request:0,response:0,processing:0,blank:0,domready:0,load:0,has_resource:0,domparse:0,resource:0,ttfb:0,redirect:0,tti:0,upload_reason:"sample",network_type:"",timing:{},navigation_timing:{},navigation:{},resources:[]},wt="PerformanceMonitor",St="StaticErrorMonitor";function Lt(t){return t="link"===(n=t).tagName.toLowerCase()?"href":"src",h(n.getAttribute)?n.getAttribute(t)||"":n[t]||"";var n}function Et(t,n,e){var r,o=n||window.event||{};try{r=o.target||o.srcElement||{}}catch(t){return}var i=r.tagName;if(s(i)){n=Lt(r);if(n&&n!==e)return{name:St,type:"get",event:Mt(n,i.toLowerCase(),t)}}}var Mt=function(t,n,e){var r=m(t),t={ev_type:"static",st_type:n,st_src:t,st_protocol:r.protocol,st_domain:r.hostname,st_path:r.pathname},e=e&&function(t,n){var e=n.length;if(e)for(var r=e-1;-1<r;r--){var o=n[r];if(o.name===t)return o}}(r.href,e);return e&&(t.timing=e),t},Tt="StaticSRIErrorMonitor";function _t(i,n,a,e){return function(o){var t;h(a.all)&&a.all([e(o,{cache:"force-cache"}).then(function(t){return t.ok?t:new Response}),(t=o+"?vt="+Date.now(),e(t,{cache:"no-store"}).then(function(t){return t.ok?t:new Response}))]).then(function(t){var t=H(t,2),e=t[0],r=t[1];if(200===e.status&&200===r.status)return a.all([e.text(),r.text()]).then(function(t){var n=t[0]||e.status+","+r.status;return[n.length,t[1].length,n,o]})}).then(function(t){var n,e,r;t&&i&&(e=(n=H(t,3))[0],r=n[1],n[2]&&e!==r&&i({name:Tt,type:"get",event:function(t,n,e,r){return{ev_type:"static_sri",sri:{error_file_size:t,real_file_size:n,error_file_context:e,static_file_src:r,static_file_url:m(r).href||""}}}.apply(void 0,c(t))}))}).catch(function(t){n&&n(t)})}}function kt(o,i){return function(t){var n,e,r=t||i.event||{};try{n=r.target||r.srcElement||{}}catch(r){return}(h((e=n).getAttribute)?e.getAttribute("integrity"):e.integrity)&&(e=h((t=n).getAttribute)?t.getAttribute("src"):t.src||t.href||"",t=(null===(t=n.tagName)||void 0===t?void 0:t.toLowerCase())||"",e&&t&&e!==location.href&&o(e))}}var Ct="MemoryRecordMonitor",Rt=(xt.prototype.reportInternal=function(){var t=window.performance.memory;this.add({jsHeapSizeLimit:t.jsHeapSizeLimit,totalJSHeapSize:t.totalJSHeapSize,usedJSHeapSize:t.usedJSHeapSize,timestamp:d()})},xt.prototype.start=function(){this.reportInternal()},xt.prototype.add=function(t){this.memoryQueue.length>=this.maxQueue&&this.memoryQueue.shift(),this.memoryQueue.push(t),this.emit&&this.emit()},xt.monitorName=Ct,xt);function xt(t){var n,e=this;this.name=Ct,this.emit=null,this.timeInstance=null,this.isUnavailable=function(){return!(o()&&window.performance.memory&&f())},this.setup=function(){e.isUnavailable()||(e.timeInstance=window.setInterval(function(){e.start()},e.timeout))},this.report=function(){return e.memoryQueue.map(function(t){return D({},t)})},this.getMemoryQueue=function(){return e.memoryQueue},this.onLeave=function(){e.isUnavailable()||(e.timeInstance&&(window.clearInterval(e.timeInstance),e.timeInstance=null),e.memoryQueue=[])},this.onShow=function(){e.isUnavailable()||(e.memoryQueue=[],e.timeInstance=window.setInterval(function(){e.start()},e.timeout))},this.visibilityChange=function(){"hidden"===document.visibilityState&&e.onLeave(),"visible"===document.visibilityState&&e.onShow()},this.timeout=null!==(n=null==t?void 0:t.interval)&&void 0!==n?n:1e3,this.maxQueue=null!==(t=null==t?void 0:t.maxQueue)&&void 0!==t?t:10,this.memoryQueue=[],U(this.onLeave,this.visibilityChange)}var At="EmitMonitor",Nt=(It.prototype.setup=function(t){this.callback=t||g},It.prototype.buildCustomTimeLog=function(t,n,e){return function(t){var n=t.name,e=t.tag,t=t.value;if(n&&t){t={ev_type:"custom",cm_name:n=h(n.toString)?n.toString():"",cm_type:"time",cm_value:t=+t};return e&&(e=h(e.toString)?e.toString():"",t.cm_tag=e),{name:"SentCustomTime",type:"get",event:t}}}({name:t,tag:n,value:e})},It.prototype.buildCustomCountLog=function(t,n){return function(t){var n=t.name,t=t.tag;if(n){n={ev_type:"custom",cm_name:n=h(n.toString)?n.toString():"",cm_type:"count"};return t&&(t=h(t.toString)?t.toString():"",n.cm_tag=t),{name:"SentCustomCount",type:"get",event:n}}}({name:t,tag:n})},It.prototype.buildEmitSingleEvent=function(t){t=w(t);if(t&&(!t||t.event_name))return{name:this.name,type:"post",event:{ev_type:"flexible",flexible_data_list:[t]}}},It.monitorName=At,It);function It(){var o=this;this.name=At,this.callback=g,this.handOut=function(){for(var t=[],n=0;n<arguments.length;n++)t[n]=arguments[n];var e=o.buildEvent.apply(o,c(t));o.callback(e)},this.buildEvent=function(){for(var t=[],n=0;n<arguments.length;n++)t[n]=arguments[n];if("sendCustomCountLog"===t[0])return o.buildCustomCountLog(t[1],t[2]);if("sendCustomTimeLog"===t[0])return o.buildCustomTimeLog(t[1],t[2],t[3]);if("send"===t[0]){if("count"===t[1])return o.buildCustomCountLog(t[2].category,t[2].action);if("timing"===t[1])return o.buildCustomTimeLog(t[2].category,t[2].action,t[2].value)}if("emit"===t[0]&&t[1]&&t[2]){var e={type:t[1],event:t[2]};return o.buildEmitSingleEvent(e)}},this.send=function(t,n,e){var r=e.action,e=e.value;"count"===t&&o.sendCustomCountLog(n,r),"timing"===t&&o.sendCustomTimeLog(n,r,e)},this.sendCustomTimeLog=function(t,n,e){e=o.buildCustomTimeLog(t,n,e);o.callback(e)},this.sendCustomCountLog=function(t,n){n=o.buildCustomCountLog(t,n);return o.callback(n),n},this.emitEvent=function(t){t=o.buildEmitSingleEvent(t);o.callback(t)}}function Ot(o){function i(n,e){var r;return function(t){a=void 0,t&&r!==t&&e({event:r=t,name:n})}}var a;return[i,function(r){return function(t){var n;try{n=t.target}catch(t){return}var e=n&&n.tagName;e&&("INPUT"===e||"TEXTAREA"===e||n.isContentEditable)&&(a||i("input",r)(t),clearTimeout(a),a=window.setTimeout(function(){a=void 0},o))}}]}function Ft(n,e){return function(t){if(e)try{n(t)}catch(t){}}}function Pt(t){if(t=t.error)return t}function jt(t){var n;try{"reason"in t?n=t.reason:"detail"in t&&"reason"in t.detail&&(n=t.detail.reason)}catch(t){}if(n)return n}function Jt(e){return function(t){if(!function(t){switch(Object.prototype.toString.call(t)){case"[object Error]":case"[object Exception]":case"[object DOMException]":return 1;default:return t instanceof Error}}(t)?(r(t)&&(n={message:JSON.stringify(t)}),s(t)&&(n={message:t})):n=t,n){var n={ev_type:"js_exception",exception:{message:(n=n).message,name:n.name,fileName:n.fileName,lineNumber:n.lineNumber,columnNumber:n.columnNumber,stack:n.stack,stacktrace:n.stacktrace,framesToPop:n.framesToPop},breadcrumbs:e()};return{name:Bt,type:"post",event:n}}}}var Dt=function(n,e,t,r){var i=(o.prototype.setup=function(t){this.monitor=V(e,this.props,t,r)},o.monitorName=n,o);function o(t){this.props=t,this.name=n}return t.forEach(function(t,o){return i.prototype[t]=function(){for(var t,n,e=[],r=0;r<arguments.length;r++)e[r]=arguments[r];return null===(n=null===(t=this.monitor)||void 0===t?void 0:t[o])||void 0===n?void 0:n.call.apply(n,c([t],e))}}),i},Ht=Dt("BreadcrumbMonitor",function(i){return void 0===i&&(i=S()),function(t){var e,n=H(Ot(100),2),r=n[0],o=n[1],n=H(function(n){void 0===n&&(n=20);var e=[];return[function(){return e},function(t){t=D(D({},t),{timestamp:d()});e=0<=n?c(e,[t]).slice(-n):c(e,[t])}]}(t.maxBreadcrumbs),2),t=n[0],n=n[1],n=(e=n,function(t){var n;try{n=t.event.target?it(t.event.target):it(t.event)}catch(t){n="<unknown>"}0!==n.length&&e({category:"ui."+t.name,message:n})});return i&&(i.addEventListener("click",r("click",Ft(n,"dom"))),i.addEventListener("keypress",o(Ft(n,"dom")))),[t]}},["getBreadcrumbs"]),Bt="JSExceptionMonitor",Ut=Dt(Bt,function(i){return void 0===i&&(i=_()),function(t,e){var n=t.getBreadcrumbs,r=t.enableCatchGlobalJSError,o=Jt(function(){return n&&n()||[]}),t=function(n){return function(t){t=n(t),t=t&&o(t);t&&e&&e(t)}};return(void 0===r||r)&&i&&(i.addEventListener("error",t(Pt)),i.addEventListener("unhandledrejection",t(jt))),[o]}},["buildEvent"]),qt=Dt(wt,function(J){return void 0===J&&(J=C()),function(t,u){function r(t){if(h=0,u){v=!1;var n=m.isAsync;w(m),n||_()||y({bounced:!0});var e=C().mpfid,r=k(),o=r&&r.event.resources,i=function(t,n){if(t&&n){var e=t.domainLookupEnd,r=t.domainLookupStart,o=t.connectEnd,i=t.connectStart,a=t.responseEnd,u=t.responseStart,s=t.requestStart,c=t.domComplete,f=t.domLoading,l=t.domInteractive,m=t.navigationStart,d=t.loadEventEnd,p=t.loadEventStart,v=t.secureConnectionStart,s={dns:e-r,tcp:o-i,request:u-s,response:a-u,processing:c-f,blank:a-m,domready:l-m,load:d-m,domparse:l-a,resource:p-t.domContentLoadedEventEnd,ttfb:u-s,redirect:t.redirectEnd-t.redirectStart};v&&(s.ssl=o-v);n=n("navigation")[0];return(n||t)&&(s.navigation=n||t),t&&(s.timing=t),n&&(s.navigation_timing=n),s}}(S,E),r=function(t,n,e,r){if(!t)return 0;var o,i=H(t,3),a=i[0],t=i[1],u=i[2];return a(),n?t().event.fmp||0:(o=[[q(1),function(){return u().event.fmp}],[q(2),function(){return r()}]],function(t){for(var n=0;n<o.length;){if(o[n][0](t))return o[n][1](t);n+=1}}(e)||0)}(f,n,s,function(){return N().fcp});y(D(D(D({},m),i),{mpfid:e,resources:o,has_resource:o?1:0,fmp:r})),m.load&&y({load:m.load});var a=function(){g=null,T(n,b())};if(g=function(){y({fid:x()}),y(N()),y({tti:Math.round(F()-p)}),a()},R.then(function(t){return y({fid:t})}),A.then(y),I.then(function(t){return y({tti:t})}),t)return y(N()),a();O(I),P.then(function(){return setTimeout(a)})}}var e,o,n,i=t.preLongTaskObserver,a=t.TTIMonitor,s=t.renderType,c=t.report,f=t.fmpMonitor,t=t.performanceAuto,l=void 0===t||t,m=D({},bt),d=a||K,p=0,v=!0,h=0,g=null,t={isAsync:0,preLongTaskObserver:i},a=H(vt(m),3),y=a[0],b=a[1],w=a[2],a=H(W(J),3),S=a[0],L=a[1],E=a[2],a=H((e=u,o=!1,[function(){return o},function(t,n){if(!t){if(o)return;o=!0}e&&e(n)}]),2),M=a[0],T=a[1],_=(n=!1,B(function(){return n=!0}),function(){return n}),k=H(V(pt),1)[0],C=H(V(ft,t),1)[0],R=z(function(t){return t.fid}),x=H(V(ct,0,R),1)[0],A=z(Q),N=H(V(mt,0,A),1)[0],I=z(function(t){if(t&&0<t)return Math.max(Math.round(t-p),0)}),t=H(V(d,t),4),O=t[0],F=t[3],P=G(I,A);B(function(){return l&&(h=setTimeout(r,200))}),U(function(){M()||(r(!0),c&&c())});var j=function(){l=!1,clearTimeout(h),h=0};return[function(){g?g():!h&&M()||(_()||j(),r(),g()),m.isAsync=1,n=H(vt(m),3),y=n[0],b=n[1],w=n[2],v=!0,p=Math.round(L());var t={isAsync:1,preLongTaskObserver:i},n=H(V(pt,t),1);k=n[0],n=H(V(ft,t),1),C=n[0],t=H(V(d,D(D({},t),{minValue:p})),4),O=t[0],F=t[3],I=z(function(t){if(t&&0<t)return Math.max(Math.round(t-p),0)});var e={fp:0,fcp:0};N=function(){return e},(A=z(Q))(e),P=G(I,A),f=V(X)},function(){v&&_()&&!h&&(m.isAsync&&(m.load=Math.round(L()-p)),h=setTimeout(r,200))},function(){return P.resolved||r(!("complete"===document.readyState)),b()},j]}},["initAsync","send","getPerformance","stopAutoPerf"]),Qt=Dt(St,function(o,i,a){return void 0===o&&(o=_()),void 0===i&&(i=C()),void 0===a&&(a=null===location||void 0===location?void 0:location.href),function(t,n){function e(){return r("resource")}var r=H(W(i),3)[2];return o&&o.addEventListener("error",function(t){t=Et(e(),t,a||"");t&&n&&n(t)},!0),[function(t){return Et(e(),t,a||"")}]}},["buildEvent"]),zt=Dt(Tt,function(e,r,o){if(void 0===e&&(e=_()),void 0===r&&(r=function(){if("Promise"in window)return Promise}()),void 0===o&&(o=T()),e&&o&&r)return function(t,n){t=kt(_t(n,t.onError,r,o),e);return e.addEventListener("error",t,!0),[t]}},["staticSRIErrorLog"]);function Gt(t,n){return a(t)?a(n)?D(D({},t),{overrides:n}):t:{}}function Vt(t,n){var e;return t.forEach(function(t){t.name===n&&(e=t)}),e}var Wt=function(r){void 0===r&&(r=window);var o=0;return{setSchedule:function(t,n){var e=this;o=r.setTimeout(function(){t(),e.setSchedule(t,n)},n)},clearSchedule:function(){r.clearTimeout(o)},getTimer:function(){return o}}}(),Xt="WorkerMonitor",Yt=(Kt.prototype.setup=function(){h(window.Worker)&&this.loadWorker()},Kt.prototype.loadWorker=function(){var e=this;p.get(this.options.workerLink,{getResponseText:function(t){var n;e.worker||(n=new Worker(window.URL.createObjectURL(new Blob([t],{type:"text/javascript"}))),e.worker=n,document.addEventListener("visibilitychange",function(){e.sendVisibilityChange({worker:n,visibilityState:document.visibilityState})}),Wt.setSchedule(function(){e.heartBeat({worker:n,reportURL:e.options.reportURL,commonParams:e.options.commonParams})},2e3))}})},Kt.prototype.sendVisibilityChange=function(t){var n=t.worker,t=t.visibilityState;n.postMessage({type:"visibilityChange",visibilityState:t})},Kt.prototype.heartBeat=function(t){var n=t.worker,e=t.reportURL,t=t.commonParams;n.postMessage({type:"heartBeat",reportURL:e,commonParams:D(D({},t||{}),{url:window.location.href}),breadcrumbs:null!==(e=null===(e=null===(t=null===(e=this.options)||void 0===e?void 0:e.breadcrumbMonitor)||void 0===t?void 0:t.getBreadcrumbs)||void 0===e?void 0:e.call(t))&&void 0!==e?e:[],memory:null!==(e=null===(e=null===(t=this.options.memoryRecordMonitor)||void 0===t?void 0:t.getMemoryQueue)||void 0===e?void 0:e.call(t))&&void 0!==e?e:[],frames:null!==(t=null===(e=null===(t=this.options.fpsJankTimesMonitor)||void 0===t?void 0:t.getHistoryFrameList)||void 0===e?void 0:e.call(t))&&void 0!==t?t:[]})},Kt.monitorName=Xt,Kt);function Kt(t){this.name=Xt,this.options=t,this.worker=null}var Zt,$t,tn,nn,en,rn,Dt=(on.prototype.setup=function(){var n=this;this.options.sendEvent&&this.monitors.forEach(function(t){(n.installedMonitors[t.name]=t).setup(n.options.sendEvent)})},on.version="3.6.19",on);function on(t){var o=this;this.getInstalledMonitors=function(){return o.installedMonitors},this.init=function(){var t,n=o.options.config;n.flags.enableStaticError&&o.monitors.push(new Qt),n.flags.enablePerformance&&(t=(t=o.options.fmpMonitor)&&[t.disconnect.bind(t),t.getFmp.bind(t),t.getLoadFmp.bind(t)],o.monitors.push(new qt({fmpMonitor:t,performanceAuto:n.commonParams.performanceAuto,renderType:n.monitors.BaseMonitor.appTypeSetting.renderType,report:function(){return o.options.report()},preLongTaskObserver:{precollect:null!==(t=null===(t=null===(t=window.Slardar)||void 0===t?void 0:t.lt)||void 0===t?void 0:t.e)&&void 0!==t?t:[],observer:null===(t=null===(t=window.Slardar)||void 0===t?void 0:t.lt)||void 0===t?void 0:t.o}}))),n.flags.enableMemoryRecord&&o.monitors.push(new Rt),n.flags.enableBreadcrumb&&o.monitors.push(new Ht),n.flags.enableFPSJankTimesMonitor&&o.monitors.push(new ut({breadcrumbMonitor:Vt(o.monitors,"BreadcrumbMonitor"),memoryRecordMonitor:Vt(o.monitors,"MemoryRecordMonitor"),report:function(){return o.options.report()}})),o.monitors.push(new Nt),n.flags.enableCatchJSErrorV2&&o.monitors.push(new Ut({enableCatchGlobalJSError:o.options.config.flags.enableCatchGlobalJSError,breadcrumbMonitor:Vt(o.monitors,"BreadcrumbMonitor")})),o.monitors.push(new zt({onError:function(t){o.options.captureException(t)}})),n.flags.enableCrash&&o.monitors.push(new Yt({reportURL:n.commonParams.reportURLSingle,commonParams:n.commonParams,workerLink:"https://sf6-scmcdn-tos.pstatp.com/goofy/slardar/fe/sdk/plugins/worker.3.6.19.cn.js",breadcrumbMonitor:Vt(o.monitors,"BreadcrumbMonitor"),memoryRecordMonitor:Vt(o.monitors,"MemoryRecordMonitor"),fpsJankTimesMonitor:Vt(o.monitors,"FPSJankTimesMonitor")})),o.setup(),o.handlePreCollect()},this.handlePreCollect=function(){var t=o.options.collect,n=null!==(n=null==t?void 0:t.emit)&&void 0!==n?n:[];i(n)&&n.forEach(function(t){var n,e;null!=t&&t.event&&(n=t.event,e=t.params,t=Gt(null===(t=Vt(o.monitors,"EmitMonitor"))||void 0===t?void 0:t.buildEvent.apply(t,c(null!=n?n:{})),e),null!==(e=(n=o.options).sendEvent)&&void 0!==e&&e.call(n,t))});n=null!==(n=null==t?void 0:t.exception)&&void 0!==n?n:[];i(n)&&n.forEach(function(t){var n,e;t&&t.exception&&(n=t.exception,e=t.params,t=Gt(null===(t=Vt(o.monitors,"JSExceptionMonitor"))||void 0===t?void 0:t.buildEvent(n),e),null!==(e=(n=o.options).sendEvent)&&void 0!==e&&e.call(n,t))});t=null!==(t=null==t?void 0:t.staticError)&&void 0!==t?t:[];i(t)&&t.forEach(function(t){var n,e,r;null!=t&&t.event&&(e=t.event,r=t.params,t=Gt(null===(n=Vt(o.monitors,"StaticErrorMonitor"))||void 0===n?void 0:n.buildEvent(e||{}),r),null!==(r=(n=o.options).sendEvent)&&void 0!==r&&r.call(n,t),null!==(t=Vt(o.monitors,"StaticSRIErrorMonitor"))&&void 0!==t&&t.staticSRIErrorLog(e))})},this.options=t,this.monitors=[],this.installedMonitors={}}return Zt={pluginName:"SetMonitors",version:Dt.version,plugin:Dt},window.__SLARDAR__||(window.__SLARDAR__={}),window.__SLARDAR__&&((nn={version:$t=Zt.plugin.version})[Zt.pluginName]=Zt.plugin,tn=nn,nn=null!==(nn=window.__SLARDAR__.plugins)&&void 0!==nn?nn:[],rn=!(en=[]),nn.forEach(function(t){t.version===$t&&("SetMonitors"!==Zt.pluginName||t.SetMonitors||(t[Zt.pluginName]=Zt.plugin),"SetSentryMonitors"!==Zt.pluginName||t.SetSentryMonitors||(t[Zt.pluginName]=Zt.plugin),"SetHeatmap"!==Zt.pluginName||t.SetHeatmap||(t[Zt.pluginName]=Zt.plugin),"SetHeatmapDraw"!==Zt.pluginName||t.SetHeatmapDraw||(t[Zt.pluginName]=Zt.plugin),"SetHeatmapMouseDraw"!==Zt.pluginName||t.SetHeatmapMouseDraw||(t[Zt.pluginName]=Zt.plugin),"SetHeatmapScrollDraw"!==Zt.pluginName||t.SetHeatmapScrollDraw||(t[Zt.pluginName]=Zt.plugin),rn=!0),en.push(t)}),rn||en.push(tn),window.__SLARDAR__.plugins=en),t.SetMonitors=Dt,Object.defineProperty(t,"__esModule",{value:!0}),t}({});
