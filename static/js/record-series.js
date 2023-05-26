let oneDay = 60 * 60 * 24;
const writeToCache = function (url, data) {
    const expiration = Date.now() + oneDay * 1000;
    const cacheData = { data, expiration };
    localStorage.setItem(url, JSON.stringify(cacheData));
};

const readFromCache = function (url) {
    const cacheData = JSON.parse(localStorage.getItem(url));

    if (cacheData && cacheData.expiration >= Date.now()) {
        return cacheData.data;
    } else {
        localStorage.removeItem(url);
        return null;
    }
};

/**
 * This function will return the siblings of an array of searchTerms
 * `json` : /collections/2?fmt=json
 * `SearchTerms`: 
 * ['Danmark, negativsamlingen 1930-1970'] will return all siblings of 'Danmark, negativsamlingen 1930-1970'
 * ['Danmark, negativsamlingen 1930-1970', 'Undervisning'] will return all siblings of 'Undervisning' in 'Danmark, negativsamlingen 1930-1970'
 */
function findSiblings(json, searchTerms) {

    // Get and remove last element
    // let lastElem = searchTerms.pop();
    for (let i = 0; i < searchTerms.length; i++) {
        const searchTerm = searchTerms[i];
        let result = json.filter(item => item.label === searchTerm);
        if (result.length > 0) {
            json = result[0].children;
        }
    }

    // If last element is in json then remove it
    // json = json.filter(item => item.label !== lastElem);
    return json;
}

function getSeriesArray(event) {
    let search = event.target.dataset.search;
    let urlParams = new URLSearchParams(search);
    let seriesValue = urlParams.get('series');
    let seriesArray = seriesValue.split('/');

    return seriesArray;
}

function getSiblingsHTML(siblings) {
    let html = '';
    for (let i = 0; i < siblings.length; i++) {
        const sibling = siblings[i];
        let encodedPath = encodeURIComponent(sibling.path);
        let link = `/search?collection=${collectionId}&series=${encodedPath}`;
        html += `<div><a class="resource-link" href="${link}">${sibling.label}</a></div>`;
    }
    return html;
}

async function loadSeries() {

    let json = readFromCache(collectionJsonPath);
    if (json) return json

    let data = await fetch(collectionJsonPath)
        .then(response => response.json())
        .then(data => {
            return data;
        });

    if (data.series) {
        writeToCache(collectionJsonPath, data.series);
    } else {
        throw new Error('No series found');
    }
    return data.series
}

document.addEventListener('click', async function (event) {

    try {

        let series = await loadSeries();
        if (event.target.matches('.toogle i')) {

            let elem = event.target;
            let expandLevel = elem.dataset.level;

            event.preventDefault();
            event.target.classList.toggle('fa-folder-open');

            let childrenDiv = event.target.parentElement.parentElement.querySelector('.siblings');
            if (event.target.classList.contains('fa-folder-open')) {
                let search = getSeriesArray(event)
                let siblings = findSiblings(series, search);

                let html = getSiblingsHTML(siblings);
                if (html === '') {
                    html = '<div>Der er ingen søskende</div>';
                }
                childrenDiv.innerHTML = html;
            } else {
                childrenDiv.innerHTML = '';
            }
        }
    } catch (error) {
        console.log(error);
    }
}, false);