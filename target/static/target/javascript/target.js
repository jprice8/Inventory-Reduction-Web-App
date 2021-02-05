const csrftoken = getCookie('csrftoken');

$("input[type='checkbox']").change(function() {
  // If target item is checked...
  const selectedCheckbox = $(this).closest('input');
  const selectedId = $(this).attr('data-id');

  if (selectedCheckbox.is(":checked")) {
    const urlTrue = `https://reductiontoolkit.com/target/${selectedId}/settrue/`;
    $.ajax({
      url: urlTrue,
      method: 'POST',
      headers: {'X-CSRFToken': csrftoken},
      data: {'setIsTarget': true}
    })
    .done(function(response) {
      console.log(response);
    })
    .fail(function(error) {
      console.log(error);
    });

    // If target item is unchecked...
  } else {
    const urlFalse = `https://reductiontoolkit.com/target/${selectedId}/setfalse/`;
    $.ajax({
      url: urlFalse,
      method: 'POST',
      headers: {'X-CSRFToken': csrftoken},
      data: {'setIsTarget': false}
    })
    .done(function(response) {
      console.log(response);
    })
    .fail(function(error) {
      console.log(error);
    });
  }
});

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
