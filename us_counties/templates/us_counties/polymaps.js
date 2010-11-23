var data, map, yMax, xMax, yMin, xMin;
window.onload = function() {
    var po = org.polymaps;
    map = po.map()
        .container(document.getElementById("map-canvas").appendChild(po.svg("svg")))
        .zoomRange([1, 6])
        .zoom(4)
        .add(po.interact());
    map.add(po.image().url("http://s3.amazonaws.com/com.modestmaps.bluemarble/{Z}-r{Y}-c{X}.jpg"));
    data = po.geoJson()
        .url("/us-counties/json/?state={{ state }}")
        .tile(false)
        .on("load", load);
    map.add(data);
    map.add(po.compass().pan("none"));
}

Array.max = function( array ){
    return Math.max.apply( Math, array );
};
Array.min = function( array ){
    return Math.min.apply( Math, array );
};

function load(e) {
  var x = Array();
  var y = Array();
  for (var i = 0; i < e.features.length; i++) {
    var feature = e.features[i];
    feature.element.setAttribute("id", i);
    feature.element.setAttribute("class", "county");
    feature.element.setAttribute("name", feature.data.properties.name);
    //feature.element.on("mouseover", function(){console.log(i);});
    //feature.element.setAttribute
    var coords = feature.data.geometry.coordinates;
    var polygons = $.map(coords, function(a){return a});
    var points = $.map(polygons, function(a){return a});
    $.map(points, function(a){
        if(!isNaN(a[0])){x.push(a[0])}; 
        if(!isNaN(a[1])){y.push(a[1])};
    });
  }
  xMax = Array.max(x);
  xMin = Array.min(x);
  yMax = Array.max(y);
  yMin = Array.min(y);
  map.extent([{lon:xMin,lat:yMin},{lon:xMax,lat:yMax}])
    $(".county").hover(
      function () {
        $('#selected-object').html($(this).attr('name'));
        var o = $('#' + $(this).attr("id"));
        $(this).css("fill", "#DDD");
      },
      function () {
        $('#selected-object').html('');
        $(this).css("fill", "#007AAA");
      }
    );
}

