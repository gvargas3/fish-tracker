$(document).ready(function () 
{
console.log('Called fish-tracker');
/******************************* Nav Bar functionality **************************************************************/
$('#home-nav').click(function()
{
  if(!$('#home-nav').parent().is('.active'))
  {
    $('.nav-item').removeClass('active');
    $('#alert-div').removeClass('active');
    $('#home-nav').parent().addClass('active');

    $('#content-holder').load('html/home.html', function(){
      $('#content-holder').trigger('home-load');
    });
  }
});

$('#connections-nav').click(function()
{
  if(!$('#connections-nav').parent().is('.active'))
  {
    $('.nav-item').removeClass('active');
    $('#alert-div').removeClass('active');
    $('#connections-nav').parent().addClass('active');

    $('#content-holder').load('html/connections.html', function(){
      $('#content-holder').trigger('connections-load');
    });
  }
});

$('#alert-div').click(function()
{
  if(!$('#alert-div').is('.active'))
  {
    $('.nav-item').removeClass('active');
    $('#alert-div').addClass('active');

    $('#content-holder').load('html/connections.html', function(){
      $('#content-holder').trigger('connections-load');
    });

    removeAlerts();
  }
});

var addAlert = function()
{
  $('#alert-num').show();
  var alerts = Number($('#alert-num').text());
  alerts = alerts + 1;
  $('#alert-num').text(alerts);
}

var removeAlerts = function()
{
  $('#alert-num').text('0');
  $('#alert-num').hide();
}
/******************************* Home Page functionality **************************************************************/
$('#content-holder').on('home-load', function(){
  console.log('In home javscript event')
  let formula = $('#formula');
  let result = $('#result');

  formula.on('input', () => {
    client.invoke("calc", formula.val(), (error, res) => {
      if(error) {
        console.error(error);
      } else {
        result.text(res);
      }
    });
  });
  
  formula.trigger('input');
});

/******************************* Connections Page functionality **************************************************************/
$('#content-holder').on('connections-load', function(){
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

});
