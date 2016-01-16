// GLOBALS
var map;
var markers = [];
var prices = [];
var allowBubble = true;


function getRecords() {
    $(function() {

        $.getJSON('/get_recent_ads', function(data) {

            $.each(data, function(link, values) {

                addMarker(link, values);

            });

            addHeader();

        });

    });
};


function CenterControl(controlDiv, map) {

    // Set CSS for the control border.
    var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = 'rgba(255,255,255,.8)';
    controlUI.style.border = '2px solid rgba(255,255,255,.8)';
    controlUI.style.borderRadius = '3px';
    controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
    controlUI.style.cursor = 'pointer';
    controlUI.style.marginBottom = '22px';
    controlUI.style.textAlign = 'center';
    controlUI.title = 'Click to refresh';
    controlDiv.appendChild(controlUI);

    // Set CSS for the control interior.
    var controlText = document.createElement('div');
    controlText.style.color = 'rgb(25,25,25)';
    controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
    controlText.style.fontSize = '25px';
    controlText.style.lineHeight = '35px';
    controlText.style.paddingLeft = '5px';
    controlText.style.paddingRight = '5px';

    controlText.innerHTML = 'Found ' + prices.length + ' rooms for rent in Wroclaw';
    controlUI.appendChild(controlText);

}


function initMap() {

    var mapOptions = {
        center: new google.maps.LatLng(51.11, 17.03),
        zoom: 12,
        maxZoom: 16,
        minZoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        disableDefaultUI: true
    };

    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    infoWindow = new google.maps.InfoWindow();

    google.maps.event.addListener(map, 'click', function() {
        infoWindow.close();
    });

    // fit the map
    // var bounds = new google.maps.LatLngBounds();
    // map.fitBounds(bounds);

    // Load markers after the creation of map
    getRecords();

}


function addHeader() {

    // CLUSTERING
    var mcOptions = {gridSize: 25, maxZoom: 13};
    var markerCluster = new MarkerClusterer(map, markers, mcOptions);

    // ADD HEADER
    var centerControlDiv = document.createElement('div');
    var centerControl = new CenterControl(centerControlDiv, map);
    centerControlDiv.index = 1;
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerControlDiv);

}


function addMarker(link, values) {

    var lat = values["coords"].split(',')[0];
    var lon = values["coords"].split(',')[1];

    var price = values["price"];
    var title = values["title"];
    var age = values["age"];
    var latlng = new google.maps.LatLng(lat, lon);

    var marker = createMarker(latlng, link, price, title, age);
    markers.push(marker);
    prices.push(price);

    //
    //bounds.extend(latlng);

}


function createMarker(latlng, link, price, title, age) {

    var marker = new google.maps.Marker({

        map: map,
        position: latlng,
        opacity: 1 - (age * 0.035)

    });

    if (allowBubble) {

        google.maps.event.addListener(marker, 'click', function() {

            var contentString = '<p><b>' + title +'</b><br>' +
                                'Price: ' + price + '<br>' +
                                'Available: <a href="' + link + '" target="_blank">HERE</a></p>';

            infoWindow.setContent(contentString);
            infoWindow.open(map, marker);

        });

    }

    return marker;

}


function filterMarkers(value) {

    for (i = 0; i < prices.length; i++) {

        if (prices[i] < value || value == 0) {

            markers[i].setVisible(true);

        } else {

            markers[i].setVisible(false);

        };

    }

}


// wait with init after website is loaded
// google.maps.event.addDomListener(window, 'load', getRecords);
