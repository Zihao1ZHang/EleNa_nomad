import React, { useEffect, useRef } from 'react';
import './myMap.css';
import { Map } from 'maplibre-gl';
import { Marker } from 'maplibre-gl';

const MyMap = ({
    mapIsReadyCallback /* To be triggered when a map object is created */,
}) => {
    const mapContainer = useRef(null);

    useEffect(() => {
        const map = new Map({
            container: mapContainer.current,
//            style: 'https://api.maptiler.com/maps/streets/style.json?key=get_your_own_OpIi9ZULNHzrESv6T2vL',
            style: {
                'version': 8,
                'name': 'Blank',
                'center': [0, 0],
                'zoom': 0,
                'sources': {
                    'raster-tiles': {
                        'type': 'raster',
                        'tiles': ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
                        'tileSize': 256,
                        'minzoom': 0,
                        'maxzoom': 19
                    }
                },
                'layers': [
                    {
                        'id': 'background',
                        'type': 'background',
                        'paint': {
                            'background-color': '#e0dfdf'
                        }
                    },
                    {
                        'id': 'simple-tiles',
                        'type': 'raster',
                        'source': 'raster-tiles'
                    }
                ],
                'id': 'blank'
            },
            center: [-72.49733, 42.36881],
            zoom: 18,
//            pitch: 40,
//            bearing: 20,
            antialias: true
        });

        new Marker().setLngLat([-72.49733, 42.36881]).addTo(map);

        mapIsReadyCallback(map);
        }, [mapContainer.current]);

    return <div className="map-container" ref={mapContainer}></div>;
};

export default MyMap;
