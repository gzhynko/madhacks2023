const convertToDateTimeLocalString = (date) => {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, "0");
    const day = date.getDate().toString().padStart(2, "0");
    const hours = date.getHours().toString().padStart(2, "0");
    const minutes = date.getMinutes().toString().padStart(2, "0");

    return `${year}-${month}-${day}T${hours}:${minutes}`;
};
const currentTime = new Date();
document.getElementById("date-from").value = convertToDateTimeLocalString(currentTime);
currentTime.setHours(23, 59);
document.getElementById("date-to").value = convertToDateTimeLocalString(currentTime);

function levenshteinDistance(s1, s2) {
    if (s1.length < s2.length) {
        return levenshteinDistance(s2, s1);
    }

    if (s2.length === 0) {
        return s1.length;
    }

    let previousRow = Array.from({ length: s2.length + 1 }, (_, i) => i);
    for (let i = 0; i < s1.length; i++) {
        let currentRow = [i + 1];
        for (let j = 0; j < s2.length; j++) {
            let insertions = previousRow[j + 1] + 1;
            let deletions = currentRow[j] + 1;
            let substitutions = previousRow[j] + (s1[i] !== s2[j]);
            currentRow.push(Math.min(insertions, deletions, substitutions));
        }
        previousRow = currentRow;
    }

    return previousRow[previousRow.length - 1];
}

function findMostSimilarByDistance(inputBuilding, buildingList, threshold = 5) {
    let mostSimilarBuilding = null;
    let minDistance = 99999999;

    for (const building of buildingList) {
        const distance = levenshteinDistance(inputBuilding.toLowerCase(), building.properties.name.toLowerCase());

        if (distance <= threshold && distance < minDistance) {
            minDistance = distance;
            mostSimilarBuilding = building;
        }
    }

    return mostSimilarBuilding;
}

function findMostSimilarByLeadingChars(inputBuilding, buildingList) {
    let mostSimilarBuilding = null;
    let maxMatchingChars = 0;

    const inputLowerCase = inputBuilding.toLowerCase();

    for (const building of buildingList) {
        const buildingNameLowerCase = building.properties.name.toLowerCase();
        let matchingChars = 0;
        for (let i = 0; i < Math.min(inputLowerCase.length, buildingNameLowerCase.length); i++) {
            if (inputLowerCase[i] === buildingNameLowerCase[i]) {
                matchingChars++;
            } else {
                break; // Stop counting if a mismatch is found
            }
        }

        if (matchingChars > 3 && matchingChars > maxMatchingChars) {
            maxMatchingChars = matchingChars;
            mostSimilarBuilding = building;
        }
    }

    return mostSimilarBuilding;
}

function padZero(number) {
    // Helper function to pad single-digit numbers with a leading zero
    return number < 10 ? "0" + number : number;
}

function convertTime(inputDate) {
    // Create a Date object from the input string
    var dateObject = new Date(inputDate);

    // Format the date as per "YYYY-MM-DD_HH:MM:SS"
    var formattedDate =
        dateObject.getFullYear() +
        "-" +
        padZero(dateObject.getMonth() + 1) +
        "-" +
        padZero(dateObject.getDate()) +
        "_" +
        padZero(dateObject.getHours()) +
        ":" +
        padZero(dateObject.getMinutes()) +
        ":" +
        padZero(dateObject.getSeconds());

    return formattedDate;
}

function addEventsToOverlay(pointsToAdd) {
    console.log("add: ", pointsToAdd);
    const element = document.getElementById("events-list");

    let eventsListHTML = "";
    pointsToAdd.forEach((point) => {
        point.properties.events.forEach((event) => {
            eventsListHTML += `
            <div style="margin-top: 10px">
                <div class="event-container">
                    <div>
                        <div class="event-name">${event.name}</div>
                    </div>
                    <div class="event-detail">${event.description}</div>      
                    <div class="event-detail"></div>      
                </div>
            </div>
            `;
        });
    });

    element.innerHTML = eventsListHTML;
}

async function findEvents() {
    const from = convertTime(document.getElementById("date-from").value);
    const to = convertTime(document.getElementById("date-to").value);

    const GET_EVENTS_ENDPOINT = "https://us-central1-madhacks-2023-404820.cloudfunctions.net/get-events";
    try {
        const serverResponse = await fetch(GET_EVENTS_ENDPOINT, {
            method: "POST", // *GET, POST, PUT, DELETE, etc.
            mode: "cors", // no-cors, *cors, same-origin
            cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
            credentials: "same-origin", // include, *same-origin, omit
            headers: {
                "Content-Type": "application/json",
                // 'Content-Type': 'application/x-www-form-urlencoded',
            },
            redirect: "follow", // manual, *follow, error
            referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
            body: JSON.stringify({ start_time: from, end_time: to }), // body data type must match "Content-Type" header
        });

        const eventsToAdd = [];
        const events = await serverResponse.json();
        // const buildingNamesFromServer = [
        //     "204 Educational Sciences",
        //     "Ebling Library, third floor galleries, Health Sciences Learning Center",
        //     "Class of 1925 Gallery (Second Floor), Memorial Union",
        //     "Main Gallery (Second Floor), Memorial Union",
        //     "Art Lofts Gallery",
        //     "Gallery 7",
        //     "Memorial Union",
        //     "Main Gallery, Memorial Union",
        //     "MYArts | 1055 E. Mifflin Street",
        //     "Chazen Museum of Art",
        //     "Lynn Mecklenburg Textile Gallery, Nancy Nicholas Hall",
        //     "Ruth Davis Design Gallery, Nancy Nicholas Hall",
        //     "Meet at Visitor Center, UW–Madison Arboretum",
        //     "11345 N Cedarburg Rd, Mequon, WI 53092",
        //     "Mitchell, Vilas Hall",
        //     "MYArts | Starlight Theater",
        //     "The Sett, Union South",
        //     "Order Online, Virtual/Online",
        //     "9th floor Vision Gallery, Wisconsin Institutes for Medical Research",
        //     "Hillel Foundation, 611 Langdon St.",
        // ];

        events.forEach((event) => {
            if (!event.building_name) {
                return;
            }

            similarBuilding = findMostSimilarByLeadingChars(event.building_name, madisonMapData["features"]);
            if (similarBuilding) {
                // console.log(">" + buildingName + " --- by leading chars --> " + similarBuilding.properties.name);
                similarBuilding = structuredClone(similarBuilding);
                similarBuilding.properties.events = [event];
                eventsToAdd.push(similarBuilding);
            } else {
                similarBuilding = findMostSimilarByDistance(event.building_name, madisonMapData["features"]);
                if (similarBuilding) {
                    // console.log(">" + buildingName + " -- by distance --> " + similarBuilding.properties.name);
                    similarBuilding = structuredClone(similarBuilding);
                    similarBuilding.properties.events = [event];
                    eventsToAdd.push(similarBuilding);
                } else {
                    // console.warn(">" + buildingName + " NO MATCH");
                }
            }
        });

        // Add together events that are at the same location
        const seenEvents = {};
        const pointsToAdd = [];

        eventsToAdd.forEach((featureWithEvent, index) => {
            const eventName = featureWithEvent.properties.name;

            if (seenEvents[eventName]) {
                // Duplicate found
                let result = null;
                for (let i = 0; i < pointsToAdd.length; i++) {
                    if (pointsToAdd[i].properties.name == eventName) {
                        result = pointsToAdd[i];
                    }
                }
                result.properties.num_of_events += 1;
                result.properties.events.push(featureWithEvent.properties.events[0]);
            } else {
                // First occurrence
                seenEvents[eventName] = true;
                featureWithEvent.properties.num_of_events = 1;
                pointsToAdd.push(featureWithEvent);
            }
        });
        console.log("pointstoadd: ", pointsToAdd);

        // Add events to overlay
        addEventsToOverlay(pointsToAdd);

        // Add events to map
        const data = {
            type: "FeatureCollection",
            features: pointsToAdd,
        };

        if (map.getLayer("clustered")) map.removeLayer("clustered");
        if (map.getLayer("cluster-count")) map.removeLayer("cluster-count");
        if (map.getLayer("event")) map.removeLayer("event");
        if (map.getLayer("circle-count")) map.removeLayer("circle-count");
        if (map.getSource("points")) map.removeSource("points");

        map.addSource("points", {
            type: "geojson",
            data: data,
            cluster: true,
            clusterMaxZoom: 16, // Max zoom to cluster points on
            clusterRadius: 40, // Radius of each cluster when clustering points (defaults to 50)
            clusterProperties: {
                sum: ["+", ["get", "num_of_events"]],
            },
        });

        // Cluster circles
        map.addLayer({
            id: "clustered",
            type: "circle",
            source: "points",
            filter: ["has", "point_count"],
            paint: {
                "circle-color": "#E32424",
                "circle-radius": 12,
                "circle-stroke-width": 2,
                "circle-stroke-color": "black",
            },
        });
        map.addLayer({
            id: "cluster-count",
            type: "symbol",
            source: "points",
            filter: ["has", "point_count"],
            layout: {
                "text-field": ["get", "sum"],
                "text-font": ["Open Sans Bold"],
                "text-size": 18,
                "text-justify": "center",
            },
            paint: {
                "text-color": "white",
            },
        });

        // Regular non clustered circles
        map.addLayer({
            id: "event",
            type: "circle",
            source: "points",
            filter: ["!", ["has", "point_count"]],
            paint: {
                "circle-color": "#E32424",
                "circle-radius": 12,
                "circle-stroke-width": 2,
                "circle-stroke-color": "black",
            },
        });
        map.addLayer({
            id: "circle-count",
            type: "symbol",
            source: "points",
            filter: ["!", ["has", "point_count"]],
            layout: {
                "text-field": ["get", "num_of_events"],
                "text-font": ["Open Sans Bold"],
                "text-size": 18,
                "text-justify": "center",
            },
            paint: {
                "text-color": "white",
            },
        });
    } catch (err) {
        console.error("Error: ", err);
    }
}

mapboxgl.accessToken = "pk.eyJ1Ijoiam1hdGhlc2l1cyIsImEiOiJjbG91aHRzczMwZ2JiMmpuemY4YTNtbGYwIn0.pbpfNj8Wp-AwvGqxophXng";
const map = new mapboxgl.Map({
    container: "map", // container ID
    // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
    style: "mapbox://styles/jmathesius/cloupit5m00fa01nw7imodc8q", // style URL
    center: [-89.404499, 43.076242], // starting position [lng, lat]
    zoom: 15, // starting zoom
});

map.on("load", () => {
    // Center the map on the coordinates of any clicked circle from the 'circle' layer.
    map.on("click", "event", (e) => {
        map.flyTo({
            center: e.features[0].geometry.coordinates,
            zoom: 17,
        });

        // Copy coordinates array.
        const coordinates = e.features[0].geometry.coordinates.slice();

        let eventsHTML = "";
        JSON.parse(e.features[0].properties.events).forEach((event) => {
            eventsHTML += `
            <div style="margin-top: 10px">
                <div class="event-container">
                    <div>
                        <div class="event-name">${event.name}</div>
                    </div>
                    <div class="event-detail">${event.description}</div>      
                    <div class="event-detail"></div>      
                </div>
            </div>
            `;
        });

        const description = `
        <strong>${e.features[0].properties.name}</strong>
        <i>${e.features[0].properties.num_of_events} event${e.features[0].properties.num_of_events == 1 ? "" : "s"}</i>
        <div class="events">
            ${eventsHTML}
        </div>
        `;

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        new mapboxgl.Popup({
            anchor: "bottom",
        })
            .setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
    });

    // Change the cursor to a pointer when the it enters a feature in the 'circle' layer.
    map.on("mouseenter", "event", () => {
        map.getCanvas().style.cursor = "pointer";
    });

    // Change the cursor to a pointer when the it enters a feature in the 'circle' layer.
    map.on("mouseenter", "event", () => {
        map.getCanvas().style.cursor = "pointer";
    });

    // Change it back to a pointer when it leaves.
    map.on("mouseleave", "event", () => {
        map.getCanvas().style.cursor = "";
    });

    // Center the map on the coordinates of any clicked circle from the 'circle' layer.
    map.on("click", "clustered", (e) => {
        map.flyTo({
            center: e.features[0].geometry.coordinates,
            zoom: 17,
        });
    });

    // Change the cursor to a pointer when the it enters a feature in the 'circle' layer.
    map.on("mouseenter", "clustered", () => {
        map.getCanvas().style.cursor = "pointer";
    });

    // Change the cursor to a pointer when the it enters a feature in the 'circle' layer.
    map.on("mouseenter", "clustered", () => {
        map.getCanvas().style.cursor = "pointer";
    });

    // Change it back to a pointer when it leaves.
    map.on("mouseleave", "clustered", () => {
        map.getCanvas().style.cursor = "";
    });
});
