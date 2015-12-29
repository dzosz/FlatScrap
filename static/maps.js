var map;
var allow_bubble;

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

  controlText.innerHTML = '' + links.length + ' rooms for rent in Wroclaw';
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

	// var bounds = new google.maps.LatLngBounds();

	var markers = [];
  	for (i = 0; i < links.length; i++) {
  		var ad = links[i];

  		var lat = ad["coords"].split(',')[0];
  		var lon = ad["coords"].split(',')[1];

  		var link = ad["link"];
  		var price = ad["price"];
  		var title = ad["title"];
  		var latlng = new google.maps.LatLng(lat, lon);

  		var marker = createMarker(latlng, link, price, title, lat, lon);

  		markers.push(marker);
		//bounds.extend(latlng);
  	}
	// fit the map
  	// map.fitBounds(bounds);
    var mcOptions = {gridSize: 25, maxZoom: 13};
    var markerCluster = new MarkerClusterer(map, markers, mcOptions);

    var centerControlDiv = document.createElement('div');
    var centerControl = new CenterControl(centerControlDiv, map);

    centerControlDiv.index = 1;
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerControlDiv);

}

function createMarker(latlng, link, price, title, lat, lon) {

	var marker = new google.maps.Marker({
		map: map,
		position: latlng
  	});

	if (allow_bubble) {
		google.maps.event.addListener(marker, 'click', function() {

			var contentString = '<p><b>' + title +'</b><br>Price: ' + price + '<br>Available here: <a href="' + link + '" target="_blank">LINK</a></p>';

		  	infoWindow.setContent(contentString);
		  	infoWindow.open(map, marker);
		});
	}
	return marker;
}

// wait with init after website is loaded
// google.maps.event.addDomListener(window, 'load', initMap);
