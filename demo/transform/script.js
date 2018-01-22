(function () {
   let wrapperEL = document.getElementsByTagName("body")[0];
   let staticEL = document.getElementById("static-block");
   let targetEL = document.getElementById("target-block");

    ctrl.btn.onclick = function () {
        targetEL.style['transform'] = "translate3d(" + ctrl.tx.value + "px, " + ctrl.ty.value + "px, " + ctrl.tz.value + "px) scale(" + ctrl.sx.value + ", " + ctrl.sy.value + ") rotateX(" + ctrl.rx.value + "deg) rotateY(" + ctrl.ry.value + "deg) rotateZ(" + ctrl.rz.value + "deg) skew(" + ctrl.skx.value + "deg, " + ctrl.sky.value + "deg)"
    };
    document.getElementById("reset").addEventListener("click", function () {
        targetEL.style['transform'] = 'none'
    })
})();