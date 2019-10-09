$(document).ready(function () 
{
  
  var getConBtn = $('#getConnectionsTest-btn');
  var connectBtn = $('#connectTest-btn');
  var connectionArray;

  getConBtn.on('click', function() {
    $('#calculator').hide();
    connectBtn.show();
    console.log(connectBtn);
    client.invoke("getConnections", (error, connectionString) => {
      if(error) 
      {
        console.error(error)
      } 
      else 
      {
        $.each(connectionString, function(i, connection)
        {
          $('#connection-holder').append('<li><input type="radio" name="connection-radio-button" string="' + connection + '">' + connection + '</li>')
        });
        console.log(connectionString)
      }
    });
  });

  connectBtn.on('click', function()
  {
    var selection = $("input[name='connection-radio-button']:checked");
    
    if(selection.length > 0)
    {
      client.invoke("connectToBoard", selection.attr('string'), (error, message) => {
        if(error) 
        {
          console.error(error)
        } 
        else 
        {
          console.log(message)
        }
      });
    }
    else
    {
      console.log('You must select a connection');
    }
  });
});

