import React, { useEffect, useRef } from 'react';
import './map.css';
import { Map } from 'maplibre-gl';

const MyMap = ({
    mapIsReadyCallback /* To be triggered when a map object is created */,
}) => {
    const mapContainer = useRef(null);

    useEffect(() => {
        const map = new Map({
            container: mapContainer.current,
            style:
            {
                'version': 8,
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
            zoom: 15,
//            pitch: 40,
//            bearing: 20,
            antialias: true
        });

        mapIsReadyCallback(map);
        }, [mapContainer.current]);

    return <div className="map-container" ref={mapContainer}></div>;
};

export default MyMap;
