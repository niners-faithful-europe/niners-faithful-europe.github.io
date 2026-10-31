function poster(LED){
LED=LED||"NEU: CAREER ANY/A, WAS DIE BESTENLISTE VERRÄT";
let o='';
const R='#C8102E',RD='#9E0C24',RK='#5A0916',G='#E4C06E',GP='#F0CF84',CR='#F6E9C8',K='#141416',K2='#232326',K3='#2E2E32',K4='#3E3E44';
const SX=30; // stadium shift right
// SKY
o+=`<g class="ly0">`;
[[0,110,'#17171A'],[110,90,'#3A0710'],[200,90,RK],[290,80,'#8E0B22'],[370,76,R],[446,52,'#D9493A'],[498,44,'#E39A4C'],[542,32,GP]].forEach(([y,h,c])=>o+=`<rect x="-40" y="${y}" width="1680" height="${h+1}" fill="${c}"/>`);
o+=`</g>`;
// SUN, clouds, far hills (Alps left, bay hills right)
o+=`<g class="ly1">`;
o+=`<clipPath id="sunclip"><rect x="0" y="0" width="1600" height="572"/></clipPath><g clip-path="url(#sunclip)"><circle cx="796" cy="548" r="84" fill="#F8E6B0"/>`;
[[506,4],[522,6],[538,8],[556,10]].forEach(([y,h])=>o+=`<rect x="700" y="${y}" width="200" height="${h}" fill="#E39A4C" opacity=".55"/>`);
o+=`</g>`;
[[70,170,380,16,.35],[140,194,240,10,.25],[980,150,380,14,.3],[1220,280,300,12,.35],[420,300,220,10,.3]].forEach(([x,y,w,h,a])=>o+=`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${h/2}" fill="${GP}" opacity="${a}"/>`);
o+=`<path d="M-40 572 L40 492 L90 522 L170 452 L230 500 L300 462 L360 506 L430 474 L500 520 L560 498 L640 572 Z" fill="#4A1520"/>`;
o+=`<path d="M152 470 L170 452 L190 470 L180 466 L170 474 Z M286 474 L300 462 L314 476 L300 480 Z" fill="${CR}" opacity=".55"/>`;
o+=`<path d="M1040 572 Q1180 510 1320 528 Q1480 540 1640 496 L1640 572 Z" fill="#4A1520"/>`;
o+=`</g>`;
// WATER
o+=`<g class="ly1"><rect x="-40" y="570" width="1680" height="400" fill="${K}"/>`;
let gl='';for(let i=0;i<16;i++){const y=588+i*14,w=140-i*6;gl+=`M${796-w/2+(i%2)*12} ${y}h${w}`;}
o+=`<path d="${gl}" stroke="${G}" stroke-width="3" opacity=".55" stroke-linecap="round"/>`;
let gs='';[[120,640,40],[380,690,60],[560,650,30],[1000,700,36],[260,760,50],[620,790,40]].forEach(([x,y,w])=>gs+=`M${x} ${y}h${w}`);
o+=`<path d="${gs}" stroke="${GP}" stroke-width="2" opacity=".3" stroke-linecap="round"/></g>`;
// EUROPE
o+=`<g class="ly2">`;
const BR='#7A3E2E',BRD='#55291F',GL='#A9B6C2',GLD='#7D8A97',CU='#5B9A80',ST='#47474E',STL='#5E5E66';
o+=`<path d="M-40 590 L600 590 L620 604 L-40 604 Z" fill="${K3}"/>`;
// Elbphilharmonie: Kaispeicher aus Backstein, Glaskörper, Wellendach
o+=`<rect x="18" y="526" width="194" height="66" fill="${BR}"/>`;
let kw='';for(let r=0;r<3;r++)for(let c=0;c<15;c++)kw+=`<rect x="${26+c*12.4}" y="${534+r*19}" width="5" height="9" fill="${BRD}"/>`;o+=kw;
o+=`<rect x="18" y="466" width="194" height="60" fill="${GL}"/>`;
let gw='';for(let r=0;r<3;r++)for(let c=0;c<13;c++)gw+=`<path d="M${25+c*14.6} ${476+r*17} q5 -5 10 0" fill="none" stroke="${r==1&&c%3==0?G:'#E9EEF2'}" stroke-width="2" opacity=".85"/>`;o+=gw;
o+=`<path d="M18 470 L18 452 Q34 444 50 450 Q66 426 88 444 Q108 414 132 440 Q150 422 168 436 Q186 424 212 438 L212 470 Z" fill="${CR}"/>`;
o+=`<rect x="18" y="524" width="194" height="3" fill="${GLD}"/>`;
// Kölner Dom
o+=`<g fill="${ST}"><rect x="234" y="512" width="104" height="80"/><rect x="234" y="400" width="32" height="112"/><rect x="306" y="400" width="32" height="112"/><path d="M234 400 L250 286 L266 400 Z M306 400 L322 286 L338 400 Z M266 512 L286 478 L306 512 Z"/><rect x="249" y="272" width="2" height="16"/><rect x="321" y="272" width="2" height="16"/></g>`;
o+=`<g fill="${STL}"><rect x="258" y="400" width="8" height="112"/><rect x="330" y="400" width="8" height="112"/><path d="M250 286 L266 400 L258 400 Z M322 286 L338 400 L330 400 Z"/></g>`;
let cr='';for(let k=1;k<7;k++){const y=400-k*16;const dx=16*(1-k*16/114);cr+=`M${250-dx} ${y}l-4 -3M${250+dx} ${y}l4 -3M${322-dx} ${y}l-4 -3M${322+dx} ${y}l4 -3`;}o+=`<path d="${cr}" stroke="${ST}" stroke-width="2"/>`;
o+=`<g fill="${G}" opacity=".55"><path d="M243 470 V440 Q250 426 257 440 V470 Z M315 470 V440 Q322 426 329 440 V470 Z M244 380 V362 Q250 352 256 362 V380 Z M316 380 V362 Q322 352 328 362 V380 Z"/></g><circle cx="286" cy="530" r="10" fill="none" stroke="${G}" stroke-width="2" opacity=".7"/><path d="M276 530h20M286 520v20" stroke="${G}" stroke-width="1" opacity=".7"/>`;
// Frauenkirche
o+=`<path d="M386 592 L386 520 L401 486 L416 520 L416 592 Z" fill="${BRD}"/>`;
o+=`<g fill="${BR}"><rect x="360" y="452" width="28" height="140"/><rect x="414" y="452" width="28" height="140"/></g><g fill="${BRD}"><rect x="381" y="452" width="7" height="140"/><rect x="435" y="452" width="7" height="140"/></g>`;
o+=`<g fill="${CU}"><path d="M359 453 Q356 426 374 416 Q392 426 389 453 Z M413 453 Q410 426 428 416 Q446 426 443 453 Z"/></g><g fill="${G}"><rect x="372" y="402" width="4" height="14"/><rect x="426" y="402" width="4" height="14"/><circle cx="374" cy="400" r="3"/><circle cx="428" cy="400" r="3"/></g>`;
o+=`<g fill="${G}" opacity=".5"><rect x="368" y="470" width="8" height="14" rx="4"/><rect x="422" y="470" width="8" height="14" rx="4"/></g>`;
// Riesenrad Wien mit roten Waggons
o+=`<g fill="none" stroke="${CR}"><circle cx="505" cy="494" r="56" stroke-width="2.5"/><circle cx="505" cy="494" r="47" stroke-width="1"/><path d="M505 438V550M449 494H561M465 454L545 534M545 454L465 534" stroke-width="1.2"/><path d="M476 592L505 494L534 592M484 562H526" stroke-width="3"/></g><circle cx="505" cy="494" r="6" fill="${CR}"/>`;
let gd='';for(let k=0;k<15;k++){const a=k*2*Math.PI/15;gd+=`<rect x="${(505+56*Math.cos(a)-6).toFixed(1)}" y="${(494+56*Math.sin(a)-2).toFixed(1)}" width="12" height="9" rx="1.5" fill="${R}" stroke="${CR}" stroke-width="1"/>`;}o+=gd;
// Stephansdom: Südturm und gemustertes Dach
o+=`<path d="M570 592 L572 476 L581 370 L590 476 L592 592 Z" fill="${ST}"/><path d="M581 370 L590 476 L592 592 L584 592 Z" fill="${STL}"/><rect x="580" y="358" width="2" height="14" fill="${ST}"/>`;
o+=`<clipPath id="sroof"><path d="M592 592 L592 540 L610 498 L628 540 L628 592 Z"/></clipPath><path d="M592 592 L592 540 L610 498 L628 540 L628 592 Z" fill="${RD}"/>`;
let zz='';for(let r=0;r<6;r++){let y=510+r*12;let d=`M590 ${y}`;for(let x=590;x<630;x+=8)d+=` L${x+4} ${y-5} L${x+8} ${y}`;zz+=`<path d="${d}" fill="none" stroke="${r%2?G:CU}" stroke-width="2.2"/>`;}o+=`<g clip-path="url(#sroof)">${zz}</g>`;
o+=`</g>`;
// GOLDEN GATE (center, sun between towers)
o+=`<g class="ly2">`;
o+=`<path d="M630 586 L1000 566 L1000 574 L630 596 Z" fill="${RD}"/><path d="M630 586 L1000 566" stroke="${R}" stroke-width="2.5"/>`;
const tower=(x,top,bot,lw,gap)=>{let t='';t+=`<rect x="${x-gap/2-lw}" y="${top}" width="${lw}" height="${bot-top}" fill="${R}"/><rect x="${x+gap/2}" y="${top}" width="${lw}" height="${bot-top}" fill="${RD}"/>`;[0,.14,.3,.48].forEach(f=>t+=`<rect x="${x-gap/2-lw}" y="${top+f*(bot-top)}" width="${gap+2*lw}" height="${Math.max(3,lw*.7)}" fill="${R}"/>`);return t;};
o+=`<path d="M630 572 Q660 480 690 404 Q796 560 906 420 Q940 490 1000 562" fill="none" stroke="${R}" stroke-width="3"/>`;
let su='';const deck=x=>586-(x-630)*20/370;
for(let k=1;k<14;k++){const t=k/14,x=(1-t)*(1-t)*690+2*t*(1-t)*796+t*t*906,y=(1-t)*(1-t)*404+2*t*(1-t)*560+t*t*420;su+=`M${x.toFixed(1)} ${y.toFixed(1)}V${deck(x).toFixed(1)}`;}
o+=`<path d="${su}" stroke="${R}" stroke-width="1.2" opacity=".9"/>`;
o+=tower(690,396,606,7,13)+tower(906,412,600,6,11);
o+=`</g>`;
// SF SKYLINE
o+=`<g class="ly2">`;
o+=`<path d="M1230 600 Q1290 540 1370 566 L1370 600 Z" fill="${K3}"/>`;
[[1010,500,40,K4],[1056,470,46,K3],[1170,430,36,K3],[1260,480,40,K4],[1310,500,44,K3]].forEach(([x,y,w,c])=>o+=`<rect x="${x}" y="${y}" width="${w}" height="${600-y}" fill="${c}"/>`);
o+=`<path d="M1110 600 L1134 262 L1158 600 Z" fill="${K3}"/><path d="M1134 262 L1158 600 L1134 600 Z" fill="${K2}"/><rect x="1132.5" y="228" width="3" height="36" fill="${K3}"/>`;
o+=`<path d="M1196 600 V290 Q1224 224 1252 290 V600 Z" fill="${K2}"/><path d="M1238 268 Q1248 278 1252 290 V600 H1238 Z" fill="${G}" opacity=".35"/>`;
o+=`<rect x="1300" y="452" width="20" height="74" fill="${CR}" opacity=".85"/><rect x="1296" y="444" width="28" height="10" fill="${CR}" opacity=".85"/><rect x="1303" y="432" width="14" height="12" fill="${CR}" opacity=".85"/>`;
let wd='';[[1060,480,3,8],[1174,440,2,10],[1014,510,2,6],[1264,490,2,7]].forEach(([x,y,c,r])=>{for(let i=0;i<c;i++)for(let j=0;j<r;j++)if((i+j)%3)wd+=`<rect x="${x+6+i*12}" y="${y+6+j*14}" width="4" height="5" fill="${G}" opacity=".7"/>`;});
o+=wd+`</g>`;
// BOAT (moves Europe -> Bay)
o+=`<g class="ly3"><g class="boat"><g transform="translate(250 716)"><path d="M0 0 L64 0 L54 14 L8 14 Z" fill="${CR}"/><path d="M30 -2 L30 -64 L58 -6 Z" fill="${CR}"/><path d="M27 -2 L27 -50 L6 -6 Z" fill="${G}"/><path d="M30 -64 L30 -72 L42 -68 Z" fill="${R}"/><path d="M-6 18 h76" stroke="${GP}" stroke-width="2" opacity=".35"/></g></g></g>`;
// STADIUM (shifted right)
o+=`<g class="ly3"><g transform="translate(${SX} 40) scale(.94)">`;
o+=`<path d="M700 770 L1540 752 L1800 752 L1800 1000 L560 1000 L640 860 Z" fill="${K3}"/><path d="M700 770 L1540 752" stroke="${G}" stroke-width="2" opacity=".5"/>`;
o+=`<clipPath id="bowl2"><path d="M880 600 L1470 572 L1500 660 L1210 700 L1190 640 Z"/></clipPath><path d="M880 600 L1470 572 L1500 660 L1210 700 L1190 640 Z" fill="${R}"/>`;
let rw='';for(let i=0;i<12;i++){const y=606+i*9;rw+=`M860 ${y} L1510 ${y-28+i*1.5}`;}let ai='';for(let x=900;x<1500;x+=34)ai+=`M${x} 570 L${x-18} 710`;
o+=`<g clip-path="url(#bowl2)"><path d="${rw}" stroke="#E2384F" stroke-width="2"/><path d="${ai}" stroke="${RD}" stroke-width="3"/></g>`;
o+=`<path d="M876 598 L1472 570" stroke="${CR}" stroke-width="4"/><path d="M880 590 L1470 562" stroke="${CR}" stroke-width="1.5"/>`;
let tk='';for(let x=890;x<1470;x+=20)tk+=`M${x} ${598-(x-876)*28/596}v-9`;o+=`<path d="${tk}" stroke="${CR}" stroke-width="1.2"/>`;
o+=`<g clip-path="url(#bowl2)"><path d="M860 646 L1510 620 L1510 632 L860 658 Z" fill="#5A0916"/><path d="M860 660 L1510 634" stroke="${CR}" stroke-width="1.2" opacity=".6"/></g>`;
let lp='';[[930,596],[1060,590],[1190,584],[1320,578],[1440,572]].forEach(([x,y])=>{lp+=`<rect x="${x-1.5}" y="${y-70}" width="3" height="70" fill="${K}"/><rect x="${x-12}" y="${y-84}" width="24" height="14" fill="${K}"/>`;for(let i=0;i<4;i++)for(let j=0;j<2;j++)lp+=`<rect x="${x-10+i*5.5}" y="${y-82+j*6}" width="3" height="3" fill="#FFF6D8"/>`;});o+=lp;
o+=`<clipPath id="fld"><path d="M1150 700 L1320 690 L1326 776 L1150 784 Z"/></clipPath><path d="M1150 700 L1320 690 L1326 776 L1150 784 Z" fill="#3F7F4C"/>`;
let yl='';for(let x=1160;x<1330;x+=16)yl+=`M${x} 690 L${x+10} 790`;o+=`<g clip-path="url(#fld)"><path d="${yl}" stroke="#FFFFFF" stroke-width="1.6" opacity=".8"/><path d="M1150 736 L1326 728" stroke="#FFFFFF" stroke-width="1" stroke-dasharray="3 5" opacity=".7"/></g>`;
o+=`<path d="M1300 640 L1500 628 L1506 770 L1306 776 Z" fill="${CR}"/>`;let eg='';for(let i=0;i<7;i++)for(let j=0;j<6;j++)eg+=`<rect x="${1314+i*27}" y="${650+j*20-i*0.8}" width="17" height="11" fill="${i%3==1?R:K4}"/>`;o+=eg;
o+=`<path d="M1356 636 V650 M1450 630 V646" stroke="${CR}" stroke-width="4"/><path d="M1330 560 L1470 552 L1474 630 L1334 636 Z" fill="${K}" stroke="${G}" stroke-width="3"/><path d="M1346 574 L1458 568 L1460 586 L1348 592 Z" fill="${R}"/><path d="M1350 606 L1420 602 M1350 618 L1446 613" stroke="${G}" stroke-width="5" stroke-linecap="round"/>`;
o+=`<path d="M1180 650 L1210 640 L1210 770 L1180 790 Z" fill="#D8CDB2"/>`;
o+=`<path d="M780 600 L1180 650 L1180 790 L780 760 Z" fill="${CR}"/>`;
o+=`<path d="M860 640 L1100 668 L1100 770 L860 752 Z" fill="#8E8572"/>`;
o+=`<path d="M800 640 L840 645 L840 718 L800 714 Z M1120 676 L1160 681 L1160 754 L1120 750 Z" fill="${R}"/>`;
let fn='';for(let x=790;x<1180;x+=26){const y=600+(x-780)*50/400;fn+=`M${x} ${(y+1).toFixed(1)}V${(760+(x-780)*30/400).toFixed(1)}`;}o+=`<path d="${fn}" stroke="#FFFFFF" stroke-width="3.4"/>`;
o+=`<path d="M786 600 L700 770 M900 616 L830 770 M1020 632 L960 776 M1140 646 L1090 782" stroke="#FFFFFF" stroke-width="1.8" opacity=".85"/>`;
o+=`<path d="M780 600 L1180 650 L1180 670 L780 620 Z" fill="${K}"/>`;
o+=`<clipPath id="led2"><path d="M784 602 L1176 651 L1176 668 L784 619 Z"/></clipPath><g clip-path="url(#led2)"><g transform="matrix(1 0.125 0 1 0 0)"><g class="ledrun"><text x="790" y="514" textLength="660" lengthAdjust="spacingAndGlyphs" fill="${G}" font-family="Hanken Grotesk, Arial, sans-serif" font-size="13" font-weight="700">${LED}   ◆   BERLIN 02:14   SANTA CLARA 17:14   ◆</text><text x="1450" y="514" textLength="660" lengthAdjust="spacingAndGlyphs" fill="${G}" font-family="Hanken Grotesk, Arial, sans-serif" font-size="13" font-weight="700">${LED}   ◆   BERLIN 02:14   SANTA CLARA 17:14   ◆</text></g></g></g>`;
o+=`<path d="M834 590 V604 M936 603 V616" stroke="${CR}" stroke-width="3"/><path d="M810 548 L960 566 L960 606 L810 588 Z" fill="${K}" stroke="${G}" stroke-width="2.5"/><path d="M822 560 L948 575 L948 586 L822 571 Z" fill="${R}"/><path d="M826 580 L900 589" stroke="${G}" stroke-width="4" stroke-linecap="round"/>`;
o+=`<path d="M780 594 L1180 644 L1180 652 L780 602 Z" fill="#5B8A4E"/>`;
o+=`</g>`;
o+=`</g>`;
return o;}
module.exports=poster;
