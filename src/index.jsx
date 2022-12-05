import React, { Component } from 'react';
import { render } from 'react-dom';
import MyMap from './mapcomponents/map';
import './style.css';
import { Marker, LngLatBounds } from 'maplibre-gl';

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
    map.on('load', function () {
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
    });
}

function removeLine(map){
    if (map.getSource('LineString') && map.getLayer('LineString'))
    {
        map.removeLayer('LineString');
        map.removeSource('LineString');
    }
}

class App extends Component {
    mapIsReadyCallback(map) {
        map.doubleClickZoom.disable();
        map.dragRotate.disable();
        const startpoint = new Marker().setLngLat([0,0]).addTo(map);
        const destination = new Marker({color: " #fed766"}).setLngLat([0,0]).addTo(map);
        var points = [[-72.49733, 42.36881], [-72.49733, 42.36781]];
        map.on("click", function(e) {
            startpoint.setLngLat(e.lngLat);
            points[0] = e.lngLat;
        });
        map.on("contextmenu", function(e) {
            destination.setLngLat(e.lngLat);
            points[1] = e.lngLat;
        });
        addLinestoMap(map, points);
        console.log(map);
    }

    render() {
        return (
            <MyMap mapIsReadyCallback={this.mapIsReadyCallback} />
        );
    }
}
//
render(<App />, document.getElementById('root'));
