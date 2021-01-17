// BELIEVE IN YOURSELF

// display the bootstrap modal for setting reduction quantity

// set csrftoken as global variable for fetch POST requests
const csrftoken = getCookie('csrftoken');

// allow the drop
function allowDrop(ev) {
  ev.preventDefault();
}

// drag the item and set the data
// item is of type text and pass the id
function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}

// drop the item, get the data, and append to new list
function drop(ev) {
  ev.preventDefault();
  const itemId = ev.dataTransfer.getData("text");
  ev.target.appendChild(document.getElementById(itemId));
  const URL = 'http://127.0.0.1:8000/target/api/listing/';

  // switch on the id of the target list and perform post request,
  // to change the item's listing
  switch(ev.target.id) {
    // 1. Drop into first list
    case 'nomovelist':
      const itemData1 = {
        'listing_data': 1,
        'item_id': itemId
      };
      sendHttpRequest(URL, 'POST', itemData1);
      break;

    // 2. Drop into second list
    case 'targetlist':
      const itemData2 = {
        'listing_data': 2,
        'item_id': itemId
      };
      // send django item info and update listing
      sendHttpRequest(URL, 'POST', itemData2);
      break;

    // 3. Drop into third list
    case 'completedlist':
      const itemData3 = {
        'listing_data': 3,
        'item_id': itemId
      };
      sendHttpRequest(URL, 'POST', itemData3);
      break;

    default:
      alert('Please move the item into one of the three columns.')
  }

  
}

// function to get csrf token (from django)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


// Helper fetch function
async function sendHttpRequest(sendurl, sendmethod, senddata) {
  const response = await fetch(sendurl, {
    method: sendmethod,
    credentials: 'include',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify(senddata)
  });
  return await response.json(); 
}


// Select reduction text in html and listen when double clicked.
$('.rex').dblclick(e => {
  // open reduction modal.
  $("#myModal").modal({backdrop: "static"});
  // async function to update reduce qty.
  updateReductionQty(e.currentTarget);
  // console.log(e.currentTarget);
})


function updateReductionQty(item) {

  // on submit reduction qty form
  $('#reduction-qty-form').on('submit', function(event) {
    event.preventDefault();
    // get user input value
    const userReductionInput = $('#reduction-qty-input').val();
    // send http request to update quantity
    sendHttpRequest(
      'http://127.0.0.1:8000/target/api/reduction/', 
      'POST', 
      {
        'reduction_data': userReductionInput,
        'item_id': item.closest('li').id
      }
    )
    .then(item.innerHTML = `Units to Reduce: ${userReductionInput}`);

    // close the modal after updating the qty.
    $('#myModal').modal('hide');
  });
}