$(document).ready(function () 
{
  console.log(client)
  let button = $('#test-btn')
  var connectionArray;
  button.on('click', function() {
    client.invoke("getConnections", (error, connectionString) => {
      if(error) 
      {
        console.error(error)
      } 
      else 
      {
        $.each(connectionString, function(i, connection)
        {
          $('#connection-holder').append('<li><input type="radio" name="this-radio-button">' + connection + '</li>')
        });
        console.log(connectionString)
      }
    })
  });
});

