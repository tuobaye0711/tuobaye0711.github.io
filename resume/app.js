(function () {
    let codes = `
/* 
 * 创意灵感来源于codepen作者Jake Albaugh 
 *
 * 项目名code-printer，已在github上开源
 *   
 * 与同类作品不同的是，本项目在支持CSS特效展示的同时，还支持部分JS操作
 *
 * 接下来就开始我的个人简介啦
 */

* {
    -webkit-transition: all 1s;
}
                   
 /* 首先，我先画一张背景板 */
 
body {
    background-color: #3D5F8F;
    color: #B6E7DC;
    font-size: 14px; line-height: 1.4;
    margin: 0;
    -webkit-font-smoothing: subpixel-antialiased;
}

/* 然后，准备我们的“打印纸” */
 
#my-code {
    overflow: auto;
    position: fixed; width: 70%;
    margin: 0;
    top: 55px; bottom: 20px; left: 15%;
    transition: left 500ms, width 500ms, opacity 500ms;
    background-color: #111111; color: #f9f9f9;
    border: 1px solid rgba(0,0,0,0.2);
    padding: 24px 12px;
    box-sizing: border-box;
    border-radius: 2px;
    box-shadow:
        0px 0px 0px 1px rgba(255,255,255,0.2),
        0px 4px 0px 2px rgba(0,0,0,0.1);
}

/* 
 * 现在还很丑，我们把代码高亮一下就好看了
 *  
 * 就用我平时IDE里用的Monokai主题给我们的代码配色吧
 */

pre em:not(.comment) { font-style: normal; }

.comment       { color: #75715e; }
.selector      { color: #a6da27; }
.selector .key { color: #a6da27; }
.selector .int { color: #a6da27; }
.key           { color: #64d9ef; }
.int           { color: #fd971c; }
.hex           { color: #f92772; }
.hex .int      { color: #f92772; }
.value         { color: #fefefe; }
.var           { color: #66d9e0; }
.operator      { color: #f92772; }
.string        { color: #d2cc70; }
.method        { color: #f9245c; }
.run-command   { color: #ae81ff; }

/* 
 * 是不是很漂亮？             
 *
 * 光打印CSS还是有点无趣，不如来点JS代码？          
 *
 * 走起！               
 */
~\`

/* 我要操作DOM，给这个页面加个标题 */
var title = document.createElement("h1");
title.id = "title";

/* 恩，起个名字 */
title.innerHTML = "<a>这是<em>张海龙</em>的个人简介</a>";

/* 做点小动作 */
title.childNodes[0].href = "https://github.com/tuobaye0711/code-printer";
title.childNodes[0].target = "view_window";

/* 最后把他添加到DOM里面 */
document.body.appendChild(title);
             
/* 
 * 如果我们的JS边打印边执行的话，我们的控制台肯定被报错刷屏了
 * 
 * 因此我们使用一个波浪号来控制代码执行
 * 
 * 听我号令，执行！
 */

 ~                 

/*
 * 怎么样？ 
 * 
 * 标题已经添加到DOM里了，但是有点丑
 * 
 * 再换成CSS代码，修饰一下吧
 */
\`

#title {
  position: fixed; width: 100%; 
  top: 0; left: 0; right: 0;
  font-size: 14px; line-height: 1;
  font-weight: 100; text-align: center;
  padding: 10px; margin: 0;
  z-index: 10;
  background-color: #111111;
  border-top: 1px solid rgba(255,255,255,0.2);
  transition: opacity 500ms;
}

#title a {
    text-decoration: none;
    color: white;
}

#title em { 
  font-style: normal;
  color: #ff2eed;
}

/*
 * 偷偷地告诉你，点击文字可以直接跳转到项目地址哦
 *
 * 希望好心的你能star&fork一下哦
 */

/*
 * 调整一下布局
 *                       
 * 我准备进入正题了
 */

#my-code { left: 20px; width: calc(50% - 30px); }

#iframe {
  position: fixed;
  display: block;
  border: 0;
  background-color: white;
  border-radius: 2px;
  width: calc(50% - 30px); height: calc(100% - 75px);
  transition: left 500ms, width 500ms;
  top: 55px; bottom: 20px; left: 100%; 
  box-shadow: 
    0px 0px 0px 1px rgba(255,255,255,0.2),
    0px 4px 0px 2px rgba(0,0,0,0.1);
}
~\`
/* 这部分还得用JS来实现 */

/* 首先，创建一个iframe */
var iframe = document.createElement("iframe");

/* 把我的简历附上 */
iframe.src = "resume/lndex.html";

/* 附上ID */
iframe.id = "iframe"

/* 加到DOM上 */
document.body.appendChild(iframe); ~
\`
/* 上吧皮卡丘！ */
#iframe { left: calc(50% + 10px); }
                                             
/*
 * emmm...                            
 *   
 * 等等！                                             
 *                   
 * 我好像拿错东西了...
 *
 * 这是我的照骗（逃）
 *
 * 赶紧换掉，换掉！                                            
 */
~\`
document.getElementById("iframe").src = "resume/index.html"; ~\`

/*
 * 很好，这正是我要的效果                                            
 *                        
 * 如果您想下载我的简历怎么办                                            
 *         
 * 别急
 *
 * 给您加个下载链接                                           
 */

 \`
 var download_link = document.createElement("a");
 download_link.id = "download_link";
 download_link.innerHTML = "简历下载";
 download_link.href = "resume/resume.pdf";
 download_link.download = "张海龙_前端开发";
 
 document.body.appendChild(download_link);
 
 ~\`
 
 /* 最后简单调整一下 */
  
#download_link {
  position: fixed;
  top: 0;
  right: 10px;
  z-index: 15;
  font-size: 1.1em;
  color: #d17aff;
  line-height: 1;
  padding: 10px;
}
 
感谢您的耐心观看٩(๑>◡<๑)۶

`;
    // 速度控制
    let speed = 16;

    let $body = document.getElementsByTagName("body")[0];

    // 简便的创建方法，可以直接附加id
    let createElement = function (tag, id) {
        let el = document.createElement(tag);
        if (id) {
            el.id = id;
        }
        return el;
    };

    // 主要元素
    let _style_elem = createElement("style", "style-elem");
    let _code_pre = createElement("pre", "my-code");
    let _script_area = createElement("div", "script-area");

    // 把主元素添加到body上
    $body.appendChild(_style_elem);
    $body.appendChild(_code_pre);
    $body.appendChild(_script_area);

    // 获取主元素
    let $style_elem = document.getElementById("style-elem");
    let $code_pre = document.getElementById("my-code");
    let $script_area = document.getElementById("script-area");

    // 状态控制
    let openComment = false;
    let openInteger = false;
    let openString = false;
    let prevAsterisk = false;
    let prevSlash = false;

    // 脚本语法高亮处理
    let jsHighlight = function (string, which) {
        let s;

        // 数字结尾时，给数字两端封上<em class="int"></em>的标签
        if (openInteger && !which.match(/[0-9\.]/) && !openString && !openComment) {
            s = string.replace(/([0-9\.]*)$/, "<em class=\"int\">$1</em>" + which);

            // 注释状态开启
        } else if (which === '*' && !openComment && prevSlash) {
            openComment = true;
            s = string + which;

            // 注释状态关闭
        } else if (which === '/' && openComment && prevAsterisk) {
            openComment = false;
            s = string.replace(/(\/[^(\/)]*\*)$/, "<em class=\"comment\">$1/</em>");

            // 给var两端封上<em class="var"></em>的标签
        } else if (which === 'r' && !openComment && string.match(/[\n ]va$/)) {
            s = string.replace(/va$/, "<em class=\"var\">var</em>");

            // 给操作符两端封上<em class="operator"></em>的标签
        } else if (which.match(/[\!\=\-\?]$/) && !openString && !openComment) {
            s = string + "<em class=\"operator\">" + which + "</em>";
            // 把 . 和 ( 中间的字符串两端封上<em class="method"></em>
        } else if (which === "(" && !openString && !openComment) {
            s = string.replace(/(\.)?(?:([^\.\n]*))$/, "$1<em class=\"method\">$2</em>(");

            // 给 " 两端加<em class="string"></em>
        } else if (which === '"' && !openComment) {
            s = openString ? string.replace(/(\"[^"\\]*(?:\\.[^"\\]*)*)$/, "<em class=\"string\">$1\"</em>") : string + which;

            // 给 ~ 两端加<em class="run-command"></em>
        } else if (which === "~" && !openComment) {
            s = string + "<em class=\"run-command\">" + which + "</em>";
        } else {
            s = string + which;
        }

        // 返回经过格式化的字符串
        return s;
    };

    // 样式语法高亮处理
    let cssHighlight = function (string, which) {
        let regular_match, formatted_string, s;

        // 数字结尾时，给数字两端封上<em class="int"></em>的标签
        if (openInteger && !which.match(/[0-9\.\%pxems]/) && !openString && !openComment) {
            formatted_string = string.replace(/([0-9\.\%pxems]*)$/, "<em class=\"int\">$1</em>");
        } else {
            formatted_string = string;
        }

        // 注释状态开启
        if (which === '*' && !openComment && prevSlash) {
            openComment = true;
            s = formatted_string + which;

            // 注释状态关闭
        } else if (which === '/' && openComment && prevAsterisk) {
            openComment = false;
            s = formatted_string.replace(/(\/[^(\/)]*\*)$/, "<em class=\"comment\">$1/</em>");

            // 给CSS属性名两端封上<em class="key"></em>的标签
        } else if (which === ':') {
            s = formatted_string.replace(/([a-zA-Z- ^\n]*)$/, '<em class="key">$1</em>:');

            // 给CSS属性值两端封上<em class="int"></em>的标签
        } else if (which === ';') {
            // 检测16进制码
            regular_match = /((#[0-9a-zA-Z]{6})|#(([0-9a-zA-Z]|\<em class\=\"int\"\>|\<\/em\>){12,14}|([0-9a-zA-Z]|\<em class\=\"int\"\>|\<\/em\>){8,10}))$/;

            // 如果是16进制，两端封上<em class="hex"></em>的标签
            if (formatted_string.match(regular_match)) {
                s = formatted_string.replace(regular_match, '<em class="hex">$1</em>;');
            } else {
                // 如果不是16进制，两端封上<em class="value"></em>的标签
                s = formatted_string.replace(/([^:]*)$/, '<em class="value">$1</em>;');
            }
            // 给选择器两端封上<em class="selector"></em>的标签
        } else if (which === '{') {
            s = formatted_string.replace(/(.*)$/, '<em class="selector">$1</em>{');
        } else {

            s = formatted_string + which;
        }
        // 返回经过格式化的字符串
        return s;
    };

    let isJs = false;

    let unformatted_code = "";

    // 打印单个字符
    let printChar = function (which) {
        let char, formatted_code, prior_block_match, prior_comment_match, script_tag;

        // 通过 ` 来切换 CSS/JS 代码
        if (which === "`") {
            // 重置为空字符串，防止打印出来
            which = "";
            isJs = !isJs;
        }

        if (isJs) {
            // 使用JS

            // 通过 ~ 来执行一个代码块
            if (which === "~" && !openComment) {
                script_tag = createElement("script");
                // two matches based on prior scenario
                prior_comment_match = /(?:\*\/([^\~]*))$/;
                prior_block_match = /([^~]*)$/;
                if (unformatted_code.match(prior_comment_match)) {
                    script_tag.innerHTML = unformatted_code.match(prior_comment_match)[0].replace("*/", "") + "\n\n";
                } else {
                    script_tag.innerHTML = unformatted_code.match(prior_block_match)[0] + "\n\n";
                }
                $script_area.innerHTML = "";
                $script_area.appendChild(script_tag);
            }
            char = which;
            formatted_code = jsHighlight($code_pre.innerHTML, char);
        } else {

            // 使用CSS
            char = which === "~" ? "" : which;
            $style_elem.innerHTML += char;
            formatted_code = cssHighlight($code_pre.innerHTML, char);
        }

        // 设置状态
        prevAsterisk = which === "*";
        prevSlash = (which === "/") && !openComment;
        openInteger = which.match(/[0-9]/) || (openInteger && which.match(/[\.\%pxems]/)) ? true : false;
        if (which === '"') {
            openString = !openString;
        }

        unformatted_code += which;

        // 打印字符
        return $code_pre.innerHTML = formatted_code;
    };

    // 遍历打印全部codes
    let printCodes = function (message, index, interval) {
        if (index < message.length) {
            // 自动滚动到底部
            $code_pre.scrollTop = $code_pre.scrollHeight;
            printChar(message[index++]);
            return setTimeout((function () {
                return printCodes(message, index, interval);
            }), speed);
        }
    };

    // 脚本初始化
    printCodes(codes, 0, speed);

}).call(this);