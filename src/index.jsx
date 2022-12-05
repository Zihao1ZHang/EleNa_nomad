import React, { Component } from 'react';
import { render } from 'react-dom';
import MyMap from './mapcomponents/map';
import SideBar from "./mapcomponents/sidebar";
import './style.css';
import '@maplibre/maplibre-gl-geocoder/dist/maplibre-gl-geocoder.css';
import { Marker, LngLatBounds } from 'maplibre-gl';
import MaplibreGeocoder from '@maplibre/maplibre-gl-geocoder';

function addMarkertoMap(map, point){
    const mk = new Marker().setLngLat(point).addTo(map);
    return mk;
}

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

function removeLine(map){
    if (map.getSource('LineString') && map.getLayer('LineString'))
    {
        map.removeLayer('LineString');
        map.removeSource('LineString');
    }
}

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
        map.doubleClickZoom.disable();
        map.dragRotate.disable();
        const startpoint = new Marker().setLngLat([0,0]).addTo(map);
        const destination = new Marker({color: " #fed766"}).setLngLat([0,0]).addTo(map);
        const beginning_inputfield = document.getElementById('Beginning');
        const destination_inputfield = document.getElementById('Destination');
        const Btn1 = document.getElementById('StartBtn');
        var points = [[-72.49733, 42.36881], [-72.49733, 42.36781]];
        map.on("click", function(e) {
            removeLine(map);
            beginning_inputfield.value = e.lngLat.toString().slice(6);
            startpoint.setLngLat(e.lngLat);
            points[0] = [e.lngLat.lng, e.lngLat.lat];
        });
        map.on("contextmenu", function(e) {
            removeLine(map);
            destination_inputfield.value = e.lngLat.toString().slice(6);
            destination.setLngLat(e.lngLat);
            points[1] = [e.lngLat.lng, e.lngLat.lat];
        });
        Btn1.addEventListener('click', function() {
            removeLine(map);
            addLinestoMap(map, points);
        });
        addSearchbar(map);
//        addLinestoMap(map, points);
    }

    render() {
        return (
            <MyMap mapIsReadyCallback={this.mapIsReadyCallback} />
        );
    }
}
//
render(<App />, document.getElementById('root'));