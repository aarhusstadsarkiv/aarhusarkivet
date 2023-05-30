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

function decodeSerieUrl(url) { 
    var decodedUrl = decodeURIComponent(url.replace(/\+/g, ' '));
    return decodedUrl
}

let id = 0;
/**
 * Add 'id', 'newLink', 'init', and 'active' to each item in series
 * 
 * 'id' is used to find the item in the tree
 * 'newLink' is used to create the link in the tree
 * 'init' is used is shown on page load
 * 'active' indicates if the item is active
 * 
 * @param {Array} children
 * 
 */
function addDataToSeries(children) {
    for (let i = 0; i < children.length; i++) {
        let child = children[i];
        child.id = id++;
        child.expanded = false;

        let newLinkCompare = `collection=${collectionId}&series=${child.path}`;
        let newLink = `/search?collection=${collectionId}&series=${encodeURIComponent(child.path)}`;
        child.newLink = newLink;

        for (let j = 0; j < seriesInit.length; j++) {
            const seriesInitItem = seriesInit[j];
            if (decodeSerieUrl(seriesInitItem.new_link) === newLinkCompare) {
                child.active = true;
                child.init = true;
                child.expanded = false;
                seriesInitItem.id = child.id;
                break;
            } else {
                child.active = false;
            }
        }

        if (child.children) {
            addDataToSeries(child.children);
        }
    }
}

function collectionDataAsUL(collectionData) {
    // Recursively create UL. If children then create LI and call function again
    let html = '<ul>';
    for (let i = 0; i < collectionData.length; i++) {
        const item = collectionData[i];
        
        let initClass = '';
        if (item.init) initClass = 'init';
        if (!item.active && !item.init) continue;

        let link = `<a class="serie-link ${initClass}" href="${item.newLink}">${item.label}</a>`;
        if (item.children) {
            let expandedClass = 'far fa-folder';
            if (item.expanded) expandedClass = 'expanded far fa-folder-open ';
            link += `<span style="padding-left:10px"><i data-id="${item.id}" class="serie-toogle ${expandedClass}"></i></span>`;
        }

        html += `<li>${link}</li>`;
        if (item.children) {
            html += collectionDataAsUL(item.children);
        }
    }
    html += '</ul>';
    return html; 
}

// collectionDataArray contains the app state
const collectionDataArray = []
const seriesApp = document.querySelector('#series-app');
document.addEventListener('DOMContentLoaded', async function () {

    let series = await loadSeries();
    addDataToSeries(series);

    let collectionData = series[collectionId]
    collectionDataArray.push(collectionData)

    let appHTML = collectionDataAsUL(collectionDataArray);
    seriesApp.innerHTML = appHTML;
});

function findById(tree, nodeId) {
    for (let node of tree) {
      if (node.id === nodeId) return node
  
      if (node.children) {
        let desiredNode = findById(node.children, nodeId)
        if (desiredNode) return desiredNode
      }
    }
    return false
  }

document.addEventListener('click', async function (event) {

    event.preventDefault();
    try {

        if (event.target.matches('i.serie-toogle')) {
            elem = event.target;
            let id = event.target.dataset.id;

            let expanded = true;
            if (elem.classList.contains('expanded')) {
                expanded = false;
            }

            let node = findById(collectionDataArray, parseInt(id));
            node.expanded = expanded;

            if (node.children) {
                node.children.forEach(function (child) {
                    if (expanded) {
                        child.active = true
                    } else {
                        child.active = false
                    }

                })

                let appHTML = collectionDataAsUL(collectionDataArray);
                seriesApp.innerHTML = appHTML;
            }
        }
    } catch (error) {
        console.log(error);
    }
}, false);
