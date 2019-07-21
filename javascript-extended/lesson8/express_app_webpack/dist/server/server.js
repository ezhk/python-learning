!function(e){var t={};function n(r){if(t[r])return t[r].exports;var o=t[r]={i:r,l:!1,exports:{}};return e[r].call(o.exports,o,o.exports,n),o.l=!0,o.exports}n.m=e,n.c=t,n.d=function(e,t,r){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(n.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)n.d(r,o,function(t){return e[t]}.bind(null,o));return r},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="/",n(n.s=2)}([function(e,t){e.exports=require("fs")},function(e,t){e.exports=require("express")},function(e,t,n){var r=n(1),o=n(0),u=n(3),i=r();i.use(r.json()),i.use("/",r.static("dist/public")),i.use("/api/cart",u),i.get("/api/products",function(e,t){o.readFile("dist/server/db/products.json","utf8",function(e,n){e?t.send({result:0,text:"error"}):t.send(n)})}),i.listen(3e3,function(){return console.log("Started at port 3000...")})},function(e,t,n){var r=n(1),o=n(0),u=n(4),i=r.Router();i.get("/",function(e,t){o.readFile("dist/server/db/userCart.json","utf8",function(e,n){e?t.send({result:0,text:"error"}):t.send(n)})}),i.post("/",function(e,t){u(e,t,"add","dist/server/db/userCart.json")}),i.put("/:id",function(e,t){u(e,t,"change","dist/server/db/userCart.json")}),i.delete("/:id",function(e,t){u(e,t,"remove","dist/server/db/userCart.json")}),e.exports=i},function(e,t,n){var r=n(0),o=n(5),u=n(6),i={add:o.add,change:o.change,remove:o.remove};e.exports=function(e,t,n,o){r.readFile(o,"utf8",function(s,a){if(s)t.send({result:0,text:"error"});else{var c=i[n](JSON.parse(a),e),d=c.name,f=c.newCart;r.writeFile(o,f,function(e){e?t.send({result:0,text:"error"}):(u(d,n),t.send({result:1,text:"ok"}))})}})}},function(e,t){e.exports={add:function(e,t){return e.contents.push(t.body),{name:t.body.product_name,newCart:JSON.stringify(e,null,4)}},change:function(e,t){var n=e.contents.find(function(e){return e.id_product===+t.params.id});return n.quantity+=t.body.quantity,{name:n.product_name,newCart:JSON.stringify(e,null,4)}},remove:function(e,t){var n=e.contents.find(function(e){return e.id_product===+t.params.id});return e.contents.splice(e.contents.indexOf(n),1),{name:n.product_name,newCart:JSON.stringify(e,null,4)}}}},function(e,t,n){var r=n(7),o=n(0);e.exports=function(e,t){o.readFile("dist/server/db/stats.json","utf8",function(n,u){if(n)console.log(n);else{var i=JSON.parse(u);i.push({prod_name:e,action:t,time:r().format("MMMM Do YYYY, h:mm:ss a")}),o.writeFile("dist/server/db/stats.json",JSON.stringify(i,null,4),function(e){e&&console.log(e)})}})}},function(e,t){e.exports=require("moment")}]);