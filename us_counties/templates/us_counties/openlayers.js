    // All of the data we need into a list
    var featureData = [{% for obj in object_list %}
        ['{{ obj.full_name }}', '{{ obj.simple_polygon_900913.wkt }}']{% if not forloop.last %},{% endif %}{% endfor %}
    ];
    
    var style = new OpenLayers.Style({
        strokeColor : '#007AAA', 
        strokeWidth: 1,
        strokeOpacity: 0.7,
        fillColor : '#007AAA', 
        fillOpacity : 0.50
    });
    var styleMap = new OpenLayers.StyleMap({
        'default': style, 
        'temporary': new OpenLayers.Style({fillOpacity : 1})
    });

    // Functions that will translate the data into OpenLayers features
    var wkt_f = new OpenLayers.Format.WKT();
    var createFeature = function (data) {
        var feature = wkt_f.read(data[1]);
        feature.data = {'name': data[0]};
        return feature;
    };

    var options = {
        projection: new OpenLayers.Projection("EPSG:900913"),
        units: "m",
        maxResolution: 156543.0339
    };

    window.onload = function(){
        // Initialize the map
        map = new OpenLayers.Map('map-canvas', options);
        // Create OpenStreetMap tile layer
        var tileLayer = new OpenLayers.Layer.OSM( "Simple OSM Map");
        map.addLayer(tileLayer);
        // Loop through the data, translate them to features
        featureArray = [];
        $.each(featureData, function (i, value) {
            featureArray.push(createFeature(value));
        });
        // Load those features on the layer
        var vectorLayer = new OpenLayers.Layer.Vector("Counties");
        vectorLayer.styleMap = styleMap;
        vectorLayer.addFeatures(featureArray);
        // Load the layer on the map
        map.addLayer(vectorLayer);
        map.zoomToExtent(vectorLayer.getDataExtent());

        // When you mouseover a polygon
        var highlighted = function (event) {
            $('#selected-object').html(event.feature.data.name)
        };
        var unhighlighted = function (event) {
            $('#selected-object').html('');
        };
        var highlightControl = new OpenLayers.Control.SelectFeature(vectorLayer, {
            hover: true,
            highlightOnly: true,
            renderIntent: "temporary",
            eventListeners: {
                featurehighlighted: highlighted,
                featureunhighlighted: unhighlighted
            }});
        map.addControl(highlightControl);
        highlightControl.activate();
    }
