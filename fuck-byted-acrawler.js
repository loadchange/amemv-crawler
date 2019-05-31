generateSignature = function(userId){
! function(t) {
    this.navigator = {
        userAgent: "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
    }
    if (t.__M = t.__M || {}, !t.__M.require) {
        var e, n, i = {},
            o = {},
            a = {},
            u = {},
            c = {},
            s = {},
            f = function(t, e, n) {
                var r = i[t] || (i[t] = []);
                r.push(e);
                var o, a = c[t] || c[t + ".js"] || {},
                    u = a.pkg;
                o = u ? s[u].url || s[u].uri : a.url || a.uri || t,
                    l(o, n && function() {
                        n(t)
                    })
            };
        n = function(t, e) {
                "function" != typeof e && (e = arguments[2]),
                    t = t.replace(/\.js$/i, ""),
                    o[t] = e;
                var n = i[t];
                if (n) {
                    for (var r = 0, a = n.length; a > r; r++)
                        n[r]();
                    delete i[t]
                }
            },
            e = function(t) {
                if (t && t.splice)
                    return e.async.apply(this, arguments);
                t = e.alias(t);
                var n = a[t];
                if (n)
                    return n.exports;
                var r = o[t];
                if (!r)
                    throw "[ModJS] Cannot find module `" + t + "`";
                n = a[t] = {
                    exports: {}
                };
                var i = "function" == typeof r ? r.apply(n, [e, n.exports, n]) : r;
                return i && (n.exports = i),
                    n.exports && !n.exports["default"] && Object.defineProperty && Object.isExtensible(n.exports) && Object.defineProperty(n.exports, "default", {
                        value: n.exports
                    }),
                    n.exports
            },
            e.async = function(n, r, i) {
                function a(t) {
                    for (var n, r = 0, h = t.length; h > r; r++) {
                        var p = e.alias(t[r]);
                        p in o ? (n = c[p] || c[p + ".js"],
                            n && "deps" in n && a(n.deps)) : p in s || (s[p] = !0,
                            l++,
                            f(p, u, i),
                            n = c[p] || c[p + ".js"],
                            n && "deps" in n && a(n.deps))
                    }
                }

                function u() {
                    if (0 === l--) {
                        for (var i = [], o = 0, a = n.length; a > o; o++)
                            i[o] = e(n[o]);
                        r && r.apply(t, i)
                    }
                }
                "string" == typeof n && (n = [n]);
                var s = {},
                    l = 0;
                a(n),
                    u()
            },
            e.resourceMap = function(t) {
                var e, n;
                n = t.res;
                for (e in n)
                    n.hasOwnProperty(e) && (c[e] = n[e]);
                n = t.pkg;
                for (e in n)
                    n.hasOwnProperty(e) && (s[e] = n[e])
            },
            e.alias = function(t) {
                return t.replace(/\.js$/i, "")
            },
            e.timeout = 5e3,
            t.__M.define = n,
            t.__M.require = e
    }
}(this)
__M.define("douyin_falcon:node_modules/byted-acrawler/dist/runtime", function(l, e) { Function(function(l) { return 'e(e,a,r){(b[e]||(b[e]=t("x,y","x "+e+" y")(r,a)}a(e,a,r){(k[r]||(k[r]=t("x,y","new x[y]("+Array(r+1).join(",x[y]")(1)+")")(e,a)}r(e,a,r){n,t,s={},b=s.d=r?r.d+1:0;for(s["$"+b]=s,t=0;t<b;t)s[n="$"+t]=r[n];for(t=0,b=s=a;t<b;t)s[t]=a[t];c(e,0,s)}c(t,b,k){u(e){v[x]=e}f{g=,ting(bg)}l{try{y=c(t,b,k)}catch(e){h=e,y=l}}for(h,y,d,g,v=[],x=0;;)switch(g=){case 1:u(!)4:f5:u((e){a=0,r=e;{c=a<r;c&&u(e[a]),c}}(6:y=,u((y8:if(g=,lg,g=,y===c)b+=g;else if(y!==l)y9:c10:u(s(11:y=,u(+y)12:for(y=f,d=[],g=0;g<y;g)d[g]=y.charCodeAt(g)^g+y;u(String.fromCharCode.apply(null,d13:y=,h=delete [y]14:59:u((g=)?(y=x,v.slice(x-=g,y:[])61:u([])62:g=,k[0]=65599*k[0]+k[1].charCodeAt(g)>>>065:h=,y=,[y]=h66:u(e(t[b],,67:y=,d=,u((g=).x===c?r(g.y,y,k):g.apply(d,y68:u(e((g=t[b])<"<"?(b--,f):g+g,,70:u(!1)71:n72:+f73:u(parseInt(f,3675:if(){bcase 74:g=<<16>>16g76:u(k[])77:y=,u([y])78:g=,u(a(v,x-=g+1,g79:g=,u(k["$"+g])81:h=,[f]=h82:u([f])83:h=,k[]=h84:!085:void 086:u(v[x-1])88:h=,y=,h,y89:u({e{r(e.y,arguments,k)}e.y=f,e.x=c,e})90:null91:h93:h=0:;default:u((g<<16>>16)-16)}}n=this,t=n.Function,s=Object.keys||(e){a={},r=0;for(c in e)a[r]=c;a=r,a},b={},k={};r'.replace(/[-]/g, function(e) { return l[15 & e.charCodeAt(0)] }) }("v[x++]=v[--x]t.charCodeAt(b++)-32function return ))++.substrvar .length(),b+=;break;case ;break}".split("")))()('gr$Daten Иb/s!l y͒yĹg,(lfi~ah`{mv,-n|jqewVxp{rvmmx,&effkx[!cs"l".Pq%widthl"@q&heightl"vr*getContextx$"2d[!cs#l#,*;?|u.|uc{uq$fontl#vr(fillTextx$$龘ฑภ경2<[#c}l#2q*shadowBlurl#1q-shadowOffsetXl#$$limeq+shadowColorl#vr#arcx88802[%c}l#vr&strokex[ c}l"v,)}eOmyoZB]mx[ cs!0s$l$Pb<k7l l!r&lengthb%^l$1+s$jl  s#i$1ek1s$gr#tack4)zgr#tac$! +0o![#cj?o ]!l$b%s"o ]!l"l$b*b^0d#>>>s!0s%yA0s"l"l!r&lengthb<k+l"^l"1+s"jl  s&l&z0l!$ +["cs\'(0l#i\'1ps9wxb&s() &{s)/s(gr&Stringr,fromCharCodes)0s*yWl ._b&s o!])l l Jb<k$.aj;l .Tb<k$.gj/l .^b<k&i"-4j!+& s+yPo!]+s!l!l Hd>&l!l Bd>&+l!l <d>&+l!l 6d>&+l!l &+ s,y=o!o!]/q"13o!l q"10o!],l 2d>& s.{s-yMo!o!]0q"13o!]*Ld<l 4d#>>>b|s!o!l q"10o!],l!& s/yIo!o!].q"13o!],o!]*Jd<l 6d#>>>b|&o!]+l &+ s0l-l!&l-l!i\'1z141z4b/@d<l"b|&+l-l(l!b^&+l-l&zl\'g,)gk}ejo{cm,)|yn~Lij~em["cl$b%@d<l&zl\'l $ +["cl$b%b|&+l-l%8d<@b|l!b^&+ q$sign ', [Object.defineProperty(e, "__esModule", { value: !0 })]) });;
_bytedAcrawler = __M.require("douyin_falcon:node_modules/byted-acrawler/dist/runtime");

const signature = _bytedAcrawler.sign(userId)
console.log(signature);
return signature;}
var _ = process.argv.splice(2)
generateSignature(_[0]);
