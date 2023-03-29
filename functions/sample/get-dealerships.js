const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);
    
    let { state, id } = params;
    var dealershipList;
    var dealershipListPromise;
    
    if (state) {
        dealershipListPromise = await getMatchingRecords(cloudant, "dealerships", {state: state})
        // dealershipList = formatEntriesMatch(dealershipListPromise);
    } else if (id) {
        id = parseInt(id)
        dealershipListPromise = await getMatchingRecords(cloudant, "dealerships", {id: id})
    } else {
        dealershipListPromise = await getAllRecords(cloudant, "dealerships");
        // dealershipList = formatEntries(dealershipListPromise);
    }

    return {
        'headers': {'Content-Type':'application/json'},
        'body': dealershipListPromise
    };
}
 
function getAllRecords(cloudant,dbname) {
    return new Promise((resolve, reject) => {
        cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
        .then((result)=>{
            resolve({rows: result.result.rows});
        })
        .catch(err => {
            console.log(err);
            reject({ err: err });
        });
    })
}

function getMatchingRecords(cloudant,dbname, selector) {
    return new Promise((resolve, reject) => {
        cloudant.postFind({db:dbname,selector:selector})
        .then((result)=>{
            resolve({rows: result.result.docs});
        })
        .catch(err => {
            console.log(err);
            reject({ err: err });
        });
    })
}

function formatEntries(entries) {
  let result = entries.result.map((row) => { return {
      id: row.doc.id,
      city: row.doc.city,
      state: row.doc.state,
      st: row.doc.st,
      address: row.doc.address,
      zip: row.doc.zip,
      lat: row.doc.lat,
      long: row.doc.long,
    }});
    
    return {dealerships: result};
}

function formatEntriesMatch(entries) {
  let result = entries.result.map((row) => { return {
      id: row.id,
      city: row.city,
      state: row.state,
      st: row.st,
      address: row.address,
      zip: row.zip,
      lat: row.lat,
      long: row.long,
    }});
    
    return {dealerships: result};
}
