import React, { Component } from 'react';
import { render } from 'react-dom';
import MyMap from './mapcomponents/map';
import './style.css';
import '@maplibre/maplibre-gl-geocoder/dist/maplibre-gl-geocoder.css';
import maplibregl, { Marker } from 'maplibre-gl';
import MaplibreGeocoder from '@maplibre/maplibre-gl-geocoder';


// Render a line on the map, used to display the calculated path
function addLinestoMap(map, points){
    const geojson = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'properties': {},
                    'coordinates': points
                }
            }
        ]
    };
    map.addSource('LineString', {
        'type': 'geojson',
        'data': geojson
    });
    map.addLayer({
        'id': 'LineString',
        'type': 'line',
        'source': 'LineString',
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': '#BF93E4',
            'line-width': 5
        }
    });
}

// Remove existing line on the map
function removeLine(map){
    if (map.getSource('LineString') && map.getLayer('LineString'))
    {
        map.removeLayer('LineString');
        map.removeSource('LineString');
    }
}

// Add a searchbar on the map, users can search and fly to the desired location
function addSearchbar(map){
    var geocoder_api = {
        forwardGeocode: async (config) => {
            const features = [];
            try {
                let request =
                'https://nominatim.openstreetmap.org/search?q=' +
                config.query +
                '&format=geojson&polygon_geojson=1&addressdetails=1';
                const response = await fetch(request);
                const geojson = await response.json();
                for (let feature of geojson.features) {
                    let center = [
                        feature.bbox[0] +
                        (feature.bbox[2] - feature.bbox[0]) / 2,
                        feature.bbox[1] +
                        (feature.bbox[3] - feature.bbox[1]) / 2
                    ];
                    let point = {
                        type: 'Feature',
                        geometry: {
                            type: 'Point',
                            coordinates: center
                        },
                        place_name: feature.properties.display_name,
                        properties: feature.properties,
                        text: feature.properties.display_name,
                        place_type: ['place'],
                        center: center
                    };
                    features.push(point);
                }
            } catch (e) {
                console.error(`Failed to forwardGeocode with error: ${e}`);
            }

            return {
                features: features
            };
        }
    };
    map.addControl(
            new MaplibreGeocoder(geocoder_api, {marker: false})
    );
}


class App extends Component {
    mapIsReadyCallback(map) {
        var result = null;
        var src = null;
        var goal = null;
        var percent = null;
        var dest = null;
        var markerHeight = 50, markerRadius = 10, linearOffset = 25;
        // Set popup style
        var popupOffsets = {
            'top': [0, 0],
            'top-left': [0,0],
            'top-right': [0,0],
            'bottom': [0, -markerHeight],
            'bottom-left': [linearOffset, (markerHeight - markerRadius + linearOffset) * -1],
            'bottom-right': [-linearOffset, (markerHeight - markerRadius + linearOffset) * -1],
            'left': [markerRadius, (markerHeight - markerRadius) * -1],
            'right': [-markerRadius, (markerHeight - markerRadius) * -1]
        };
        // Disable double click zoom and drag rotate
        map.doubleClickZoom.disable();
        map.dragRotate.disable();
        // Create makers to show the startpoint and destination
        const startpoint = new Marker().setLngLat([0,0]).addTo(map);
        const destination = new Marker({color: " #fed766"}).setLngLat([0,0]).addTo(map);
        // Create readonly inputfields to show the position of startpoint and destination
        const beginning_inputfield = document.getElementById('Beginning');
        const destination_inputfield = document.getElementById('Destination');
        // Create a button to start calculation
        const Btn1 = document.getElementById('StartBtn');
        var points = [[-72.49733, 42.36881], [-72.49733, 42.36781]];
        // Create popups to show the positions of selected points
        var popup1 = new maplibregl.Popup({offset: popupOffsets, closeButton: false, closeOnClick:false});
        var popup2 = new maplibregl.Popup({offset: popupOffsets, closeButton: false, closeOnClick:false});
        // Create maker and popup when left click on the map
        map.on("click", function(e) {
            popup1.setLngLat(e.lngLat).setText("Beginning: " + e.lngLat.toString().slice(6)).setMaxWidth("300px").addTo(map);
            removeLine(map);
            beginning_inputfield.value = e.lngLat.toString().slice(6);
            startpoint.setLngLat(e.lngLat);
            points[0] = [e.lngLat.lng, e.lngLat.lat];
        });
        // Create maker and popup when right click on the map
        map.on("contextmenu", function(e) {
            popup2.setLngLat(e.lngLat).setText("Destination: " + e.lngLat.toString().slice(6)).setMaxWidth("300px").addTo(map);
            removeLine(map);
            destination_inputfield.value = e.lngLat.toString().slice(6);
            destination.setLngLat(e.lngLat);
            points[1] = [e.lngLat.lng, e.lngLat.lat];
        });
        // Send data to backend and display the result received
        Btn1.addEventListener('click', function() {
            removeLine(map);
            src = [startpoint.getLngLat().lng, startpoint.getLngLat().lat];
            dest =  [destination.getLngLat().lng, destination.getLngLat().lat];
            goal = document.querySelector('#goals input:checked').value;
            percent = document.getElementById("percentage").value;
            fetch("http://localhost:8080/get_route", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                body: JSON.stringify({
                    Source: src,
                    Destination: dest,
                    Is_max: goal,
                    Percentage: percent,
                }),
            })
            .then((res) => res.json())
            .then((json) => {
                removeLine(map);
                result = json["Route"];
                addLinestoMap(map, result);
             });
        });
        addSearchbar(map);
    }

    render() {
        return (
            <MyMap mapIsReadyCallback={this.mapIsReadyCallback} />
        );
    }
}
render(<App />, document.getElementById('root'));