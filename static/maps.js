// GLOBALS
var map;
var markers = [];
var allowBubble = false;


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
    controlUI.title = 'Click to achieve nothing';
    controlDiv.appendChild(controlUI);

    // Set CSS for the control interior.
    var controlText = document.createElement('div');
    controlText.style.color = 'rgb(25,25,25)';
    controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
    controlText.style.fontSize = '25px';
    controlText.style.lineHeight = '35px';
    controlText.style.paddingLeft = '5px';
    controlText.style.paddingRight = '5px';

    controlText.innerHTML = 'Found ' + markers.length + ' rooms for rent in Wroclaw';
    controlUI.appendChild(controlText);

}


function initMap() {

    var mapOptions = {
        center: new google.maps.LatLng(51.11, 17.03),
        zoom: 12,
        maxZoom: 16,
        minZoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        disableDefaultUI: true,
        styles: [{ featureType: "poi", elementType: "labels", stylers: [{ visibility: "off" }]}]
    };

    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    infoWindow = new google.maps.InfoWindow();
    infoWindow2 = new google.maps.InfoWindow();

    var myOptions = {
        disableAutoPan: true,
        zIndex: null,
        boxStyle: {
          opacity: 1
        },
        closeBoxMargin: "10px 10px 10px 10px",
        // infoBoxClearance: new google.maps.Size(1, 1),
        isHidden: false,
        pane: "floatPane",
        enableEventPropagation: true
    };

    infobox = new InfoBox(myOptions);

    $(document).on('click', '.panel-heading', function() {
        $(".panel-body").hide();
        // $(".panel-heading").click(function() {
        //     console.log(this);
        //     $(".panel-body").hide();
            $(this).next(".panel-body").show()
        // });
    });

    // Event click not cooperate with mark clusterer!
    google.maps.event.addListener(map, 'click', function(event) {
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
    var mcOptions = {gridSize: 20, maxZoom: 16, zoomOnClick: true, minimumClusterSize: 1, averageCenter: false};
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

    var latlng = new google.maps.LatLng(lat, lon);

    var marker = createMarker(latlng, link, values);
    markers.push(marker);

    //
    //bounds.extend(latlng);

}


function createMarker(latlng, link, values) {

    var contentString = '<div class="btn-group" role="group">';
    var contentli = '<div class="panel-heading"><strong>'+values.title+'</strong></div>'+
                    '<div class="panel-body" >Link: <a href="'+link+'">Ogloszenie dostepne na OLX.pl</a><br>' +
                    'Cena: '+values.price+'<br>';

    keys = ["Rodzaj pokoju", "Umeblowane"];
    for (var i in keys) {
        if (keys[i] in values) {
            contentli += keys[i]+' : '+values[keys[i]]+'<br>';
        };
    };

    contentli += '</div>';
    contentString += '</ul></div>';

    var marker = new google.maps.Marker(
        {
            map: map,
            position: latlng,
            // link: link,
            // header: values["title"],
            // price: values["price"],
            age: values["age"],
            content: contentli,
        }
    );


    if (allowBubble) {

        google.maps.event.addListener(marker, 'click', function() {

            infoWindow.setContent(contentString);
            infoWindow2.close();
            infoWindow.open(map, marker);

        });

    }

    return marker;

}


function filterMarkers(value) {

    for (i = 0; i < markers.length; i++) {

        if (markers.price[i] < value || value == 0) {

            markers[i].setVisible(true);

        } else {

            markers[i].setVisible(false);

        };

    }

}


// wait with init after website is loaded
// google.maps.event.addDomListener(window, 'load', getRecords);
google.maps.event.addDomListener(window, 'load', initMap);
