// Map containers read their position from data-lat / data-lng / data-zoom when present.
(function () {
    var DEFAULT_CENTER = [-0.108968, 51.492933];
    var DEFAULT_ZOOM = 14;

    function initMap(id) {
        var container = document.getElementById(id);
        if (!container || typeof mapboxgl === 'undefined') {
            return;
        }

        var lat = parseFloat(container.getAttribute('data-lat'));
        var lng = parseFloat(container.getAttribute('data-lng'));
        var zoom = parseFloat(container.getAttribute('data-zoom'));
        var center = (isFinite(lat) && isFinite(lng)) ? [lng, lat] : DEFAULT_CENTER;

        mapboxgl.accessToken = window.MAPBOX_ACCESS_TOKEN;

        var map = new mapboxgl.Map({
            container: id,
            style: 'mapbox://styles/mapbox/light-v11',
            center: center,
            zoom: isFinite(zoom) ? zoom : DEFAULT_ZOOM
        });

        var el = document.createElement('div');
        el.className = 'marker';
        new mapboxgl.Marker(el).setLngLat(center).addTo(map);
    }

    ['map', 'map2', 'map3'].forEach(initMap);
})();
