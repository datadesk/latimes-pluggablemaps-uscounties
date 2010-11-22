var data, map;
window.onload = function() {
    var po = org.polymaps;
    map = po.map()
        .container(document.getElementById("map-canvas").appendChild(po.svg("svg")))
        .zoomRange([1, 6])
        .zoom(4)
        .add(po.interact());
    map.add(po.image().url("http://s3.amazonaws.com/com.modestmaps.bluemarble/{Z}-r{Y}-c{X}.jpg"));
    data = po.geoJson().url("/us-counties/json/?state={{ state }}").tile(false);
    map.add(data);
    map.add(po.compass().pan("none"));
}


