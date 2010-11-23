var data, map, yMax, xMax, yMin, xMin;
window.onload = function() {
    // Create the map
    var po = org.polymaps;
    map = po.map()
        .container(document.getElementById("map-canvas").appendChild(po.svg("svg")))
        .zoomRange([1, 7])
        .zoom(4)
        .add(po.interact());
    // Add the tile layer
    map.add(po.image().url("http://s3.amazonaws.com/com.modestmaps.bluemarble/{Z}-r{Y}-c{X}.jpg"));
    // Add the data layer
    data = po.geoJson()
        .url("/us-counties/json/?state={{ state }}")
        .tile(false)
        .on("load", load);
    map.add(data);
    // Add some extras
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
    // Set all the data we need into the element
    var feature = e.features[i];
    feature.element.setAttribute("id", i);
    feature.element.setAttribute("class", "county");
    feature.element.setAttribute("name", feature.data.properties.name);
    // Flatten the coordinates and add them to our master list for extent
    // calculation
    var coords = feature.data.geometry.coordinates;
    var polygons = $.map(coords, function(a){return a});
    var points = $.map(polygons, function(a){return a});
    $.map(points, function(a){
        if(!isNaN(a[0])){x.push(a[0])}; 
        if(!isNaN(a[1])){y.push(a[1])};
    });
  }
  // Set the extent
  xMax = Array.max(x);
  xMin = Array.min(x);
  yMax = Array.max(y);
  yMin = Array.min(y);
  map.extent([{lon:xMin,lat:yMin},{lon:xMax,lat:yMax}])
  // Set the event handlers
    $(".county").hover(
      function () {
        // Set the headline
        $('#selected-object').html($(this).attr('name'));
        // Change the fill
        $(this).css("fill", "#DDD");
      },
      function () {
        $('#selected-object').html('');
        $(this).css("fill", "#007AAA");
      }
    );
}

