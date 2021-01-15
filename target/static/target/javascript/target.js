// BELIEVE IN YOURSELF

// allow the drop
function allowDrop(ev) {
  ev.preventDefault();
}

// drag the item and set the data
// item is of type text and pass the id
function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}

// function to get csrf token (from django)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
// set csrftoken as global variable for fetch POST requests
const csrftoken = getCookie('csrftoken');

// drop the item, get the data, and append to new list
function drop(ev) {
  const URL = 'http://localhost:8000/target/api/';

  ev.preventDefault();
  const itemId = ev.dataTransfer.getData("text");
  ev.target.appendChild(document.getElementById(itemId));

  // switch on the id of the target list and perform post request,
  // to change the item's listing
  switch(ev.target.id) {
    case 'nomovelist':
      console.log('no move');
      break;
    case 'targetlist':
      fetch(URL, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(
          {
          'listing_data': 1,
          'item_id': itemId,
          }
        )
      })
      .then(response => {
        console.log(response);
        // return response.json()
      })
      .then(data => {
        // perform actions with the response data from the view.
        console.log(data);
      })

      break;
    case 'completedlist':
      console.log('completed');
      break;
    default:
      alert('Please move the item into one of the three columns.')
  }

}
