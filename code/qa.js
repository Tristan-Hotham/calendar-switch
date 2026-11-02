// QA: open index.html at desktop and phone widths, log console errors, take screenshots to qa/.
// Run from the study root with a static server (python3 -m http.server 8931; set PORT to change).
// MapLibre from a local npm copy (the CDN is not reachable from the build container); tiles and fonts are blocked here.
// OFFLINE=1 also blocks MapLibre itself, to check that the page degrades gracefully.
const { chromium } = require("playwright");
const fs = require("fs");
const ML = process.env.MAPLIBRE_DIST || "/tmp/ml/node_modules/maplibre-gl/dist";
fs.mkdirSync("qa", { recursive: true });
(async () => {
  const b = await chromium.launch({ args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
  const errs = [];
  const sizes = process.env.ONLY ? [[process.env.ONLY, process.env.ONLY === "phone" ? 390 : 1280, 860]] : [["desktop", 1280, 900], ["phone", 390, 844]];
  for (const [nm, vw, vh] of sizes) {
    const p = await b.newPage({ viewport: { width: vw, height: vh }, deviceScaleFactor: nm === "phone" ? 2 : 1 });
    await p.route(/arcgisonline|googleapis|gstatic/, r => r.abort());
    if (process.env.OFFLINE) await p.route(/maplibre-gl/, r => r.abort());
    else {
      await p.route(/maplibre-gl\.js$/, r => r.fulfill({ path: ML + "/maplibre-gl.js" }));
      await p.route(/maplibre-gl\.css$/, r => r.fulfill({ path: ML + "/maplibre-gl.css" }));
    }
    p.on("console", m => { if (m.type() === "error" && !/ERR_FAILED|net::|Failed to fetch|AJAXError/.test(m.text())) errs.push(nm + ": " + m.text()); });
    p.on("pageerror", e => errs.push(nm + " pageerror: " + e.message));
    await p.goto("http://localhost:" + (process.env.PORT || 8931) + "/index.html", { waitUntil: "load" });
    const pre = process.env.OFFLINE ? "offline_" : "";
    if (process.env.OFFLINE) {
      await p.waitForTimeout(1500);
      console.log(nm, "offline message:", await p.textContent("#map"));
      await p.screenshot({ path: `qa/${pre}${nm}_top.png` }); await p.locator("#atlas").screenshot({ path: `qa/${pre}${nm}_map.png` });
      await p.locator("#curveChart").scrollIntoViewIfNeeded(); await p.locator("#curveChart").screenshot({ path: `qa/${pre}${nm}_curves.png` });
      await p.close(); continue;
    }
    for (let k = 0; k < 60 && !(await p.evaluate(() => !!window.map && !document.getElementById("loading"))); k++) await p.waitForTimeout(500);
    console.log(nm, "map ready:", await p.evaluate(() => !!window.map && !document.getElementById("loading")));
    await p.waitForTimeout(1500);
    await p.screenshot({ path: `qa/${nm}_top.png` });
    const shot = async (sel, f) => { await p.locator(sel).scrollIntoViewIfNeeded(); await p.waitForTimeout(700); await p.locator(sel).screenshot({ path: `qa/${nm}_${f}.png` }); };
    await shot("#atlas", "map_cal_2026");
    console.log(nm, "states set:", await p.evaluate(() => Object.keys(SITE.units).filter(i => map.getFeatureState({ source: "world", id: i }).c).length));
    await p.evaluate(() => setYear(1760)); await p.waitForTimeout(600); await shot("#atlas", "map_cal_1760");
    await p.evaluate(() => setYear(1710)); await p.waitForTimeout(600);
    console.log(nm, "Sweden 1710:", await p.evaluate(() => map.getFeatureState({ source: "world", id: "SWE" }).c));
    await p.click("#play"); await p.waitForTimeout(1500); await p.click("#play");
    console.log(nm, "after play year:", await p.textContent("#yv"));
    await p.click('#tabs [data-k="road"]'); await p.evaluate(() => setYear(1950)); await p.waitForTimeout(700); await shot("#atlas", "map_road_1950");
    await p.evaluate(() => setYear(2026)); await p.waitForTimeout(500); await shot("#atlas", "map_road_2026");
    await p.click('#tabs [data-k="metric"]'); await p.evaluate(() => setYear(1900)); await p.waitForTimeout(600); await shot("#atlas", "map_metric_1900");
    await p.click('#tabs [data-k="vote"]'); await p.evaluate(() => setYear(1930)); await p.waitForTimeout(600); await shot("#atlas", "map_vote_1930");
    await p.click('#measureRow [data-v="full"]'); await p.waitForTimeout(400); await shot("#atlas", "map_vote_1930_equal"); await p.click('#measureRow [data-v="first"]');
    // search and popup
    await p.click('#tabs [data-k="cal"]'); await p.evaluate(() => setYear(2026));
    await p.fill("#q", "United King"); await p.waitForTimeout(400); await p.keyboard.press("Enter"); await p.waitForTimeout(1600); await shot("#atlas", "popup_uk");
    console.log(nm, "popup:", (await p.evaluate(() => (document.querySelector(".maplibregl-popup-content") || {}).innerText || "none")).slice(0, 200).replace(/\n/g, " | "));
    await p.fill("#q", "Sweden"); await p.waitForTimeout(400); await p.keyboard.press("Enter"); await p.waitForTimeout(1500); await shot("#atlas", "popup_sweden");
    // click on the map: the Netherlands, a sub-national province
    await p.evaluate(() => { map.jumpTo({ center: [5.3, 52.1], zoom: 5.5 }); setYear(1600); }); await p.waitForTimeout(1200);
    const box = await p.locator("#map").boundingBox(); const pt = await p.evaluate(() => map.project([5.9, 52.1]));
    await p.mouse.click(box.x + pt.x, box.y + pt.y); await p.waitForTimeout(700); await shot("#atlas", "click_gelderland_1600");
    console.log(nm, "sub popup:", (await p.evaluate(() => (document.querySelector(".maplibregl-popup-content") || {}).innerText || "none")).slice(0, 120).replace(/\n/g, " | "));
    await p.evaluate(() => { map.jumpTo({ center: [12, 30], zoom: 1.15 }); setYear(2026); if (window.popup) popup.remove(); });
    await p.click(".lyrBtn"); await p.waitForTimeout(300); await shot("#map", "layers_panel"); await p.click(".lyrBtn");
    await p.click("#curveMode [data-m='pop']"); await p.waitForTimeout(300);
    for (const c of ["curveChart", "daysChart", "roadChart", "metricChart", "voteChart", "holdTable", "ctyTable"]) await shot("#" + c, c);
    await p.click("#curveMode [data-m='n']");
    if (nm === "phone") {
      await p.click("#theme"); await p.waitForTimeout(1200); await shot("#atlas", "dark_map"); await shot("#curveChart", "dark_curves");
      await p.click("#theme");
    }
    await p.locator("#atlas").scrollIntoViewIfNeeded(); await p.click(".mfs-btn"); await p.waitForTimeout(1500); await p.screenshot({ path: `qa/${nm}_fullscreen.png` });
    console.log(nm, "fullscreen:", await p.evaluate(() => !!document.fullscreenElement || !!document.querySelector(".mfs-fake")));
    await p.click(".mfs-btn"); await p.waitForTimeout(500);
    const ov = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    console.log(nm, "horizontal overflow px:", ov);
    await p.close();
  }
  console.log("errors:", errs.length ? errs : "none");
  await b.close();
})();
